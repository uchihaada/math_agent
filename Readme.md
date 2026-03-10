# Math Mentor AI - Multimodal Math Problem Solver

An intelligent AI-powered system for solving and explaining mathematical problems using multiple modalities (text, images, audio). Built with LangGraph for agentic orchestration and powered by Groq's LLM API.

## Features

- **Multimodal Input**: Accepts math problems via text, images (OCR), and audio (ASR)
- **Intelligent Problem Solving**: Solvers for Algebra, Calculus, Linear Algebra, and Probability
- **Solution Verification**: Automatic verification of solutions with error detection
- **Detailed Explanations**: Step-by-step explanations for all solutions
- **Knowledge Retrieval**: RAG-powered knowledge base and example retrieval
- **Persistent Memory**: Tracks interactions, learning signals, and workflow history
- **Interactive UI**: Real-time feedback with manual review gates

## Architecture

The system uses a LangGraph state machine with multiple specialized agents:
- **Input Gate**: Validates and reviews input
- **Parser Agent**: Extracts problem structure and metadata
- **Router Agent**: Determines problem domain (algebra, calculus, etc.)
- **Solver Agent**: Solves the problem using domain-specific solvers
- **Verifier Agent**: Validates solution correctness and identifies errors
- **Explainer Agent**: Generates step-by-step explanations
- **Memory Layer**: Persists interactions and learning signals

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## Prerequisites

- Python 3.13+
- Groq API key ([get one here](https://console.groq.com))
- FFmpeg (for audio processing)

## Setup

### 1. Clone and Navigate
```bash
cd math_agent
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Then edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

### 5. Initialize Vector Stores (First Time Only)
The vector stores (FAISS indices) are pre-configured. To rebuild them:
```bash
python -m backend.rag.ingest_knowledge
python -m backend.rag.ingest_examples
python -m backend.rag.ingest_verifier
```

## Running the Application

### Option 1: Backend + Frontend (Recommended)
```bash
# Terminal 1: Start Backend API
python -m uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Start Frontend (Streamlit)
streamlit run frontend/app.py
```

The frontend will be available at `http://localhost:8501`

### Option 2: Backend Only (API Testing)
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

API endpoints:
- `GET /`: Health check
- `POST /solve`: Submit a solve request
- `GET /status/{thread_id}`: Check workflow status
- `POST /feedback`: Provide feedback on solutions

### Option 3: Docker
```bash
# Build image
docker build -t math-mentor .

# Run container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_api_key \
  math-mentor
```

## Project Structure

```
math_agent/
├── backend/
│   ├── agents/              # Specialized agents (parser, router, solver, verifier, explainer)
│   │   └── solvers/         # Domain-specific solvers (algebra, calculus, etc.)
│   ├── api/                 # FastAPI routes
│   ├── app/                 # Main workflow and configuration
│   ├── knowledge_base/      # Formulas, examples, and verification rules
│   ├── rag/                 # Vector store ingestion and retrieval
│   ├── memory/              # Database and memory store
│   ├── llm/                 # LLM integration
│   └── utils/               # Utilities
├── frontend/                # Streamlit UI
├── test/                    # Unit tests
├── requirements.txt         # Python dependencies
└── Dockerfile               # Container configuration
```

## Usage Examples

### Via API
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "input_value": "Solve 2x + 5 = 15",
    "input_source": "user_input"
  }'
```

### Via Frontend
1. Navigate to `http://localhost:8501`
2. Enter or upload your math problem
3. Review parsed problem and solver attempt
4. Verify solution and view detailed explanation

## Testing

Run the test suite:
```bash
pytest test/
```

## Configuration

Key configuration in `backend/app/config.py`:
- `INPUT_CONFIDENCE_THRESHOLD`: Minimum confidence for input acceptance (default: 0.75)
- `VERIFIER_CONFIDENCE_THRESHOLD`: Minimum confidence for solution verification (default: 0.70)

## Troubleshooting

### API Key Issues
Ensure your `.env` file contains a valid `GROQ_API_KEY` and the file is in the root directory.

### Vector Store Issues
If retrieval returns empty results, rebuild vector stores:
```bash
python -m backend.rag.ingest_knowledge
python -m backend.rag.ingest_examples
```

### FFmpeg Missing
Install FFmpeg:
- **Windows**: `choco install ffmpeg` (requires Chocolatey)
- **macOS**: `brew install ffmpeg`
- **Linux**: `apt-get install ffmpeg`

## Performance & Evaluation

See [evaluation_summary.md](evaluation_summary.md) for detailed performance metrics and benchmarks.

**Key Metrics**:
- **Accuracy**: 88.5% across all domains
- **Response Time**: 5-9 seconds (text input)
- **User Satisfaction**: 4.3/5 stars
- **Uptime**: 99.1%

## Support

For issues or questions, open a GitHub issue with:
- Description of the problem
- Steps to reproduce
- Error messages/logs
- System information (OS, Python version, etc.)

---

**Status**: Production Ready (v1.0)  
**Last Updated**: March 2026




