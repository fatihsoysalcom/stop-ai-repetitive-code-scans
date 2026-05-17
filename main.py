import time

# Simulate a codebase with multiple files
# In a real scenario, these would be actual files on disk.
CODEBASE = {
    "src/utils.py": """
def helper_function(data):
    # This function uses 'requests' library for HTTP calls.
    # It also interacts with 'database_connector'.
    result = data * 2
    return result

class MyUtility:
    def __init__(self):
        self.config = {"mode": "production"}

def process_data(input_data):
    # This function uses 'pandas' for data manipulation.
    output = helper_function(input_data)
    return output
""",
    "src/main.py": """
from src.utils import process_data, MyUtility
import os
import requests # Main app also uses requests

def main():
    # Main application logic
    data = [1, 2, 3]
    processed = process_data(data)
    print(f"Processed data: {processed}")
    # Configuration from os environment
    env_var = os.getenv("MY_APP_CONFIG", "default")
    print(f"Config: {env_var}")

if __name__ == "__main__":
    main()
""",
    "tests/test_utils.py": """
import unittest
from src.utils import helper_function
# This test file uses 'pytest' for advanced testing features.

class TestUtils(unittest.TestCase):
    def test_helper_function(self):
        self.assertEqual(helper_function(5), 10)
        # Assertions for 'requests' library usage
"""
}

class NaiveAIAgent:
    """
    Simulates an AI agent that scans files as plain text for every query.
    This demonstrates the problem of repetitive scanning, similar to 'grep'.
    """
    def __init__(self):
        self.total_scan_operations = 0 # Tracks how many files were scanned in total

    def find_keyword_in_codebase(self, codebase, keyword):
        """
        Scans every file in the codebase to find a keyword.
        """
        found_in_files = []
        for filepath, content in codebase.items():
            self.total_scan_operations += 1 # Each file read/scan is an operation
            if keyword in content:
                found_in_files.append(filepath)
        return found_in_files

class CodeGraphAIAgent:
    """
    Simulates an AI agent that uses a pre-built 'CodeGraph' (simplified index)
    to answer queries, avoiding repetitive full file scans.
    """
    def __init__(self):
        self.index = {} # Simplified: keyword -> list of files where it appears
        self.initial_index_build_time_ms = 0

    def build_index(self, codebase):
        """
        Simulates the initial 'CodeGraph' building phase.
        This happens once, parsing the codebase into a structured representation.
        """
        start_time = time.perf_counter()
        # In a real CodeGraph, this would involve AST parsing, semantic analysis,
        # and building a graph of code entities and their relationships.
        # For this demo, we'll simulate by creating an inverted index for specific keywords.
        
        # Example keywords an AI agent might look for
        keywords_to_index = ["requests", "pandas", "os", "unittest", "database_connector", "pytest"]

        for filepath, content in codebase.items():
            for keyword in keywords_to_index:
                if keyword in content:
                    if keyword not in self.index:
                        self.index[keyword] = []
                    self.index[keyword].append(filepath)
        end_time = time.perf_counter()
        self.initial_index_build_time_ms = (end_time - start_time) * 1000
        print(f"CodeGraph: Initial index built in {self.initial_index_build_time_ms:.4f} ms.")

    def find_keyword_in_codebase(self, keyword):
        """
        Answers queries using the pre-built index, avoiding full file scans.
        This demonstrates the efficiency of a CodeGraph-like approach.
        """
        start_time = time.perf_counter()
        # With a CodeGraph, queries traverse the graph or lookup in an index.
        # No need to re-read file contents for each query.
        found_in_files = self.index.get(keyword, [])
        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000
        return found_in_files, query_time_ms

# --- Demonstration ---
print("--- Naive AI Agent (Problem: Repetitive Scanning) ---")
naive_agent = NaiveAIAgent()

# Query 1
start_time_naive_q1 = time.perf_counter()
files_using_requests_naive = naive_agent.find_keyword_in_codebase(CODEBASE, "requests")
end_time_naive_q1 = time.perf_counter()
print(f"Query 1 ('requests'): Found in {files_using_requests_naive}")
print(f"  Scan operations for Q1: {len(CODEBASE)} (Time: {(end_time_naive_q1 - start_time_naive_q1)*1000:.4f} ms)")

# Query 2 (another keyword, still scans all files again)
start_time_naive_q2 = time.perf_counter()
files_using_pandas_naive = naive_agent.find_keyword_in_codebase(CODEBASE, "pandas")
end_time_naive_q2 = time.perf_counter()
print(f"Query 2 ('pandas'): Found in {files_using_pandas_naive}")
print(f"  Scan operations for Q2: {len(CODEBASE)} (Time: {(end_time_naive_q2 - start_time_naive_q2)*1000:.4f} ms)")

print(f"\nTotal scan operations by Naive Agent across 2 queries: {naive_agent.total_scan_operations}")

print("\n--- CodeGraph AI Agent (Solution: Indexed Approach) ---")
codegraph_agent = CodeGraphAIAgent()

# Phase 1: Initial indexing (one-time cost)
codegraph_agent.build_index(CODEBASE) # This is where the "CodeGraph" is built

# Phase 2: Subsequent queries leverage the index (very fast)
# Query 1
files_using_requests_cg, time_cg_q1 = codegraph_agent.find_keyword_in_codebase("requests")
print(f"Query 1 ('requests'): Found in {files_using_requests_cg}")
print(f"  CodeGraph agent query time: {time_cg_q1:.4f} ms (no file scans)")

# Query 2
files_using_pandas_cg, time_cg_q2 = codegraph_agent.find_keyword_in_codebase("pandas")
print(f"Query 2 ('pandas'): Found in {files_using_pandas_cg}")
print(f"  CodeGraph agent query time: {time_cg_q2:.4f} ms (no file scans)")

print("\n--- Summary ---")
print("The Naive AI Agent repeatedly scans all files for each query, leading to high 'scan operations'.")
print("The CodeGraph AI Agent performs an initial indexing (one-time cost), then answers subsequent queries almost instantly by leveraging the pre-built index, effectively stopping repetitive file scans.")
