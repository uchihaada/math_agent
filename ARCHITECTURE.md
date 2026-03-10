# Math Agent - High-Level Architecture

## System Overview

The Math Agent is a **Human-in-the-Loop (HITL) workflow engine** built on LangGraph that intelligently solves complex mathematical problems through a series of specialized agents with multiple review gates for quality assurance.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Math Agent Workflow                          │
│              (LangGraph-based State Machine)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **Workflow State Management**

The `WorkflowGraphState` TypedDict manages the complete state of a problem-solving session:

#### Input Processing
- `input_type`: Type of input (text, OCR, ASR, etc.)
- `original_input`: Raw user input
- `working_input`: Processed input used for solving
- `ocr_confidence` / `asr_confidence`: Confidence scores for automatic input extraction
- `input_reviewed`: Flag indicating human input review

#### Problem Analysis
- `parsed_problem`: Structured representation of the math problem
- `route`: Router's decision on which solver to use
- `topics`: Mathematical topics identified in the problem

#### Solution Processing
- `solver_output`: Generated solution with retrieved context
- `solver_feedback`: Human feedback for solution refinement
- `verification`: Verifier agent's assessment of solution correctness
- `explanation`: Student-friendly explanation of the solution

#### Workflow State
- `status`: Current workflow status (running, success, error, rejected)
- `next_step`: Next node to execute
- `review_stage`: Current review gate
- `final_action`: Final human action taken
- `recheck_requested`: Flag for manual solution re-check

#### Learning & Tracing
- `learning_signals`: Corrections and feedback for continuous learning
- `trace`: Agent execution trace for debugging and transparency
- `interaction_id`: Reference to saved interaction in memory store

---

## Workflow Architecture

### **Node Flow**

```
START
  ↓
1. INPUT_GATE (Confidence Check)
  ├─→ Needs Review? → HUMAN INTERRUPT
  │    ├─ Approve → Parse
  │    ├─ Edit → Parse
  │    └─ Reject → END
  └─→ OK? → 2. PARSE
     ↓
2. PARSE (Parker Agent)
  ├─ Converts raw input to structured problem
  └─→ 3. PARSER_GATE
     ↓
3. PARSER_GATE (Ambiguity Check)
  ├─→ Needs Clarification? → HUMAN INTERRUPT
  │    ├─ Approve → Route
  │    ├─ Edit → Parse (restart)
  │    └─ Reject → END
  └─→ OK? → 4. ROUTE
     ↓
4. ROUTE (Router Agent)
  ├─ Analyzes topics
  ├─ Selects appropriate solver
  └─→ 5. SOLVE
     ↓
5. SOLVE (Solver Agent)
  ├─ Retrieves relevant examples/formulas from RAG
  ├─ Generates solution with reasoning
  └─→ 6. VERIFY
     ↓
6. VERIFY (Verifier Agent)
  ├─ Checks solution correctness
  ├─ Identifies potential issues
  ├─ Provides confidence score
  └─→ 7. SOLVER_GATE
     ↓
7. SOLVER_GATE (Solution Review)
  ├─→ Correct & High Confidence? → Explain
  └─→ Incorrect/Low Confidence? → HUMAN INTERRUPT
       ├─ Approve → Explain
       ├─ Edit → Solve (with solver feedback)
       ├─ Recheck → Solve (with recheck flag)
       └─ Reject → END
     ↓
8. EXPLAIN (Explainer Agent)
  ├─ Creates student-friendly explanation
  └─→ 9. FINAL_GATE
     ↓
9. FINAL_GATE (Human Final Review)
  ├─→ HUMAN INTERRUPT
  │    ├─ Approve → Persist
  │    ├─ Edit → Explain (with corrected solution)
  │    ├─ Recheck → Solve (with human feedback)
  │    └─ Reject → END
  └─→
     ↓
10. PERSIST (Memory Layer)
   ├─ Save interaction
   ├─ Save retrieval context
   ├─ Save verification outcome
   ├─ Save learning signals
   └─→ END
```

---

## Workflow Nodes (10 Nodes)

| Node | Agent | Purpose | Key Decision |
|------|-------|---------|--------------|
| **input_gate** | Input Gate | Validates OCR/ASR confidence | Confidence > 75%? |
| **parse** | Parser Agent | Converts input to structured problem | - |
| **parser_gate** | Parser Gate | Checks for ambiguity | Needs clarification? |
| **route** | Router Agent | Selects appropriate solver based on topics | Algebra/Calculus/Linear Algebra/Probability? |
| **solve** | Solver Agent | Generates solution with RAG retrieval | - |
| **verify** | Verifier Agent | Validates solution correctness | Correct & Confident? |
| **solver_gate** | Solver Gate | Human review of solution quality | Needs retry/edit/approval? |
| **explain** | Explainer Agent | Creates student explanation | - |
| **final_gate** | Final Review | Human final approval | Approve/Edit/Recheck/Reject? |
| **persist** | Memory Layer | Saves all interaction data | - |

---

## Key Decision Points (6 Gates)

### 1. **Input Gate** (Confidence Threshold: 75%)
- **When triggered**: OCR/ASR confidence score is low
- **Human interrupts**: Reviews raw text and can approve, edit, or reject
- **Outcome**: Proceed to parsing or end workflow

### 2. **Parser Gate** (Ambiguity Detection)
- **When triggered**: Parser marks problem as needing clarification
- **Human interrupts**: Reviews parsed structure and can approve, edit, or reject
- **Outcome**: If edited, restarts parsing with corrected input

### 3. **Solver Gate** (Verification Threshold: 70%)
- **When triggered**: Solution is incorrect OR confidence < 70%
- **Human interrupts**: Reviews solution and can:
  - Approve (accept low-confidence solution)
  - Edit (provide corrected solution, solver regens)
  - Recheck (solver retries with feedback)
  - Reject (end workflow)
- **Outcome**: Proceed to explanation or restart solving

### 4. **Final Gate** (Manual Review)
- **When triggered**: Always executes before persistence
- **Human interrupts**: Final approval with options to:
  - Approve (save solution as-is)
  - Edit (correct solution, regenerate explanation)
  - Recheck (solver reprocesses with feedback)
  - Reject (discard entire workflow)
- **Outcome**: Save to memory or end

---

## Agent Types & Responsibilities

### **Specialized Solvers** (routing-based selection)
- **Algebra Solver**: Linear equations, polynomials, systems
- **Calculus Solver**: Limits, derivatives, integrals
- **Linear Algebra Solver**: Matrices, vectors, transformations
- **Probability Solver**: Combinatorics, distributions, statistics
- **Hybrid Solver**: Multi-topic problems

### **Cross-Cutting Agents**
- **Parser Agent**: Converts unstructured input to structured problem with topics
- **Router Agent**: Analyzes topics and selects solver strategy
- **Verifier Agent**: Quality assurance, correctness checking, confidence scoring
- **Explainer Agent**: Pedagogical explanation generation
- **Memory Layer**: Persists interactions, retrieval context, and learning signals

---

## Data Flow

### **Input Pipeline**
```
Raw Input (Text/OCR/ASR)
    ↓
Input Gate (Confidence Check)
    ↓
Parsed Problem (topics, text, constraints)
    ↓
Router (topic analysis)
    ↓
Selected Solver
```

### **Solution Generation**
```
Solver + RAG Retrieval
    ↓
Candidate Solution + Retrieved Context
    ↓
Verification (correctness + confidence)
    ↓
[Acceptable?] → Explanation → Final Gate → Persist
     ↓
  [Unacceptable?] → Human Review → Edit/Recheck
```

### **Learning & Memory**
```
Human Feedback & Corrections
    ↓
Learning Signals (transcript corrections, clarifications, solution edits)
    ↓
Saved Interactions + Verification Outcomes + Retrieval Context
    ↓
Vector Store Update (successful examples for RAG)
```

---

## State Transitions & Loops

### **Parse Loop**
- User input → Parser → Parser Gate
- If clarification needed: User edit → Parser → Parser Gate (loop)

### **Solve Loop**
- Route → Solve → Verify → Solver Gate
- If low confidence/incorrect: Solve → Verify → Solver Gate (loop with feedback)

### **Correction Loop**
- Final Gate → Edit action → Verify → Explain → Final Gate (loop)

### **Early Termination**
- Reject at any gate: Input Gate, Parser Gate, Solver Gate, Final Gate → END

---

## Response Status Codes

| Status | Meaning | When Occurs |
|--------|---------|------------|
| `running` | Workflow in progress | During execution |
| `accepted` | Async workflow accepted | After async start |
| `hitl_required` | Human interrupt needed | At any review gate |
| `rejected` | Workflow rejected by human | Human clicks reject |
| `success` | Completed successfully | After persist node |
| `error` | System failure | Exception in workflow |

---

## Threading & Async Execution

### **Synchronous Mode** (`run()`)
- Blocks until workflow completes
- Used for direct API calls

### **Asynchronous Mode** (`run_async()`)
- Returns immediately with `accepted` status
- Workflow runs in background thread
- Client polls status via `get_status(thread_id)`
- Active runs tracked in `_active_runs` dict with thread safety

---

## Memory & Persistence

### **Checkpointing**
- Uses `PersistentInMemorySaver` for workflow state snapshots
- Enables resuming from checkpoints

### **Memory Store Integration**
- Saves interactions (problem, solution, metadata)
- Tracks retrieval context used in solution
- Records verifier outcomes and confidence scores
- Stores feedback and learning signals

### **Vector Store Updates**
- Successfully solved examples added to examples vector store
- Enables RAG to improve over time with human-approved solutions

---

## Configuration & Thresholds

```python
INPUT_CONFIDENCE_THRESHOLD = 0.75      # OCR/ASR confidence required
VERIFIER_CONFIDENCE_THRESHOLD = 0.70   # Solution confidence required
```

---

## Integration Points

### **External Dependencies**
- **LangGraph**: Workflow state machine and graph execution
- **LLM**: Claude (via llm.py) for all agent reasoning
- **RAG System**: FAISS vector stores for knowledge/examples/verifier retrieval
- **Memory Store**: PostgreSQL/SQLite for interaction persistence
- **API**: FastAPI routes for HTTP endpoints

### **Frontend Integration**
- Streamlit app for user interaction
- Real-time status polling via `/api/status/{thread_id}`
- Human interrupt handling via review payloads
- Feedback submission for learning signals

---

## Error Handling & Recovery

- **Workflow-level exceptions**: Caught, logged, return error status
- **Human interrupts**: Suspends execution, awaits user action
- **Verifier low confidence**: Triggers solver_gate for manual review
- **State snapshots**: Preserved at each node for debugging

