import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.retriever import retrieve_context

query = "if y = tan-1(1+x/1-x)  find dy/dx"

result = retrieve_context(query)

print("FORMULAS")
for r in result["formulas"]:
    print(r)

print("\nEXAMPLES")
for r in result["examples"]:
    print(r)