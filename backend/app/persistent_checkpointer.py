from __future__ import annotations

import pickle
from collections import defaultdict
from threading import RLock
from typing import Any, Iterator

from langgraph.checkpoint.memory import InMemorySaver

from backend.memory.database import conn, db_lock, init_db


class PersistentInMemorySaver(InMemorySaver):
    """Persist LangGraph checkpoints in SQLite while keeping InMemorySaver semantics."""

    def __init__(self):
        super().__init__()
        init_db()
        self._lock = RLock()
        self._loaded_threads: set[str] = set()

    def has_thread(self, thread_id: str) -> bool:
        with self._lock:
            if thread_id in self._loaded_threads and thread_id in self.storage:
                return True

            with db_lock:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM workflow_threads WHERE thread_id = ? LIMIT 1",
                    (thread_id,),
                )
                return cursor.fetchone() is not None

    def get_tuple(self, config):
        thread_id = config["configurable"]["thread_id"]
        self._ensure_loaded(thread_id)
        return super().get_tuple(config)

    def list(
        self,
        config,
        *,
        filter: dict[str, Any] | None = None,
        before=None,
        limit: int | None = None,
    ) -> Iterator:
        if config is None:
            self._load_all_threads()
        else:
            self._ensure_loaded(config["configurable"]["thread_id"])

        yield from super().list(config, filter=filter, before=before, limit=limit)

    def put(self, config, checkpoint, metadata, new_versions):
        thread_id = config["configurable"]["thread_id"]
        self._ensure_loaded(thread_id)
        updated_config = super().put(config, checkpoint, metadata, new_versions)
        self._persist_thread(thread_id)
        return updated_config

    def put_writes(self, config, writes, task_id, task_path: str = "") -> None:
        thread_id = config["configurable"]["thread_id"]
        self._ensure_loaded(thread_id)
        super().put_writes(config, writes, task_id, task_path)
        self._persist_thread(thread_id)

    def delete_thread(self, thread_id: str) -> None:
        self._ensure_loaded(thread_id)
        super().delete_thread(thread_id)

        with self._lock:
            with db_lock:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM workflow_threads WHERE thread_id = ?", (thread_id,))
                conn.commit()
            self._loaded_threads.discard(thread_id)

    def _load_all_threads(self) -> None:
        with db_lock:
            cursor = conn.cursor()
            cursor.execute("SELECT thread_id FROM workflow_threads")
            thread_ids = [row[0] for row in cursor.fetchall()]

        for thread_id in thread_ids:
            self._ensure_loaded(thread_id)

    def _ensure_loaded(self, thread_id: str) -> None:
        with self._lock:
            if thread_id in self._loaded_threads:
                return

            with db_lock:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT payload FROM workflow_threads WHERE thread_id = ?",
                    (thread_id,),
                )
                row = cursor.fetchone()
            if row is None:
                self._loaded_threads.add(thread_id)
                return

            payload = pickle.loads(row[0])

            storage = defaultdict(dict)
            for checkpoint_ns, checkpoints in payload.get("storage", {}).items():
                storage[checkpoint_ns] = dict(checkpoints)

            self.storage[thread_id] = storage

            for outer_key, writes in payload.get("writes", {}).items():
                self.writes[tuple(outer_key)] = dict(writes)

            for blob_key, blob_value in payload.get("blobs", {}).items():
                self.blobs[tuple(blob_key)] = blob_value

            self._loaded_threads.add(thread_id)

    def _persist_thread(self, thread_id: str) -> None:
        with self._lock:
            storage = {
                checkpoint_ns: dict(checkpoints)
                for checkpoint_ns, checkpoints in self.storage.get(thread_id, {}).items()
            }
            writes = {
                outer_key: dict(write_map)
                for outer_key, write_map in self.writes.items()
                if outer_key[0] == thread_id
            }
            blobs = {
                blob_key: blob_value
                for blob_key, blob_value in self.blobs.items()
                if blob_key[0] == thread_id
            }

            payload = pickle.dumps(
                {
                    "storage": storage,
                    "writes": writes,
                    "blobs": blobs,
                },
                protocol=pickle.HIGHEST_PROTOCOL,
            )

            with db_lock:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO workflow_threads (thread_id, payload, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(thread_id) DO UPDATE SET
                        payload = excluded.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (thread_id, payload),
                )
                conn.commit()
