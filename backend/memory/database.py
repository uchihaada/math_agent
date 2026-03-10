import json
import sqlite3
import threading

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()
db_lock = threading.RLock()


def serialize_topic(topic):
    if topic is None:
        return None

    if isinstance(topic, (list, tuple)):
        return json.dumps(list(topic))

    return str(topic)

def init_db():
    with db_lock:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT,
            raw_input TEXT,
            parsed_problem TEXT,
            topic TEXT,
            solution TEXT,
            explanation TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS retrieval_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER,
            retrieved_context TEXT,
            FOREIGN KEY(interaction_id) REFERENCES interactions(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER,
            feedback_type TEXT,
            comment TEXT,
            FOREIGN KEY(interaction_id) REFERENCES interactions(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER,
            stage TEXT,
            signal_type TEXT,
            original_value TEXT,
            corrected_value TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(interaction_id) REFERENCES interactions(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS verifier_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER,
            is_correct INTEGER,
            confidence REAL,
            issues TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(interaction_id) REFERENCES interactions(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_threads (
            thread_id TEXT PRIMARY KEY,
            payload BLOB NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_runtime (
            thread_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            current_node TEXT,
            current_agent TEXT,
            message TEXT,
            trace TEXT,
            retrieved_context TEXT,
            response TEXT,
            error TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(thread_id) REFERENCES workflow_threads(thread_id)
        )
        """)

        conn.commit()
