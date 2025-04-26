"""
Example demonstrating how to use the CLI tools with StatefulPy.
"""
import subprocess
import sys
import os
import time

def run_command(cmd):
    """Run a command and print the output."""
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode

def main():
    """Run a demo of the CLI commands."""
    # Create temporary paths for this demo
    sqlite_path = "cli_demo_sqlite.db"
    redis_url = "redis://localhost:6379/0"
    
    print("=== StatefulPy CLI Demo ===\n")
    
    # Initialize SQLite backend
    print("1. Initializing SQLite backend...")
    run_command(f"statefulpy init --backend sqlite --path {sqlite_path}")
    
    # Create a simple script that uses the backend
    script_path = "temp_stateful_script.py"
    with open(script_path, "w") as f:
        f.write("""
from statefulpy import stateful

@stateful(backend="sqlite", db_path="cli_demo_sqlite.db")
def counter():
    if "count" not in counter.state:
        counter.state["count"] = 0
    counter.state["count"] += 1
    return counter.state["count"]

if __name__ == "__main__":
    print(f"Counter value: {counter()}")
""")
    
    # Run the script a few times to create state
    print("\n2. Running a script that uses the SQLite backend...")
    run_command(f"{sys.executable} {script_path}")
    run_command(f"{sys.executable} {script_path}")
    
    # List functions in the SQLite backend
    print("\n3. Listing functions in the SQLite backend...")
    run_command(f"statefulpy list --backend sqlite --path {sqlite_path}")
    
    # Check health of the SQLite backend
    print("\n4. Checking health of the SQLite backend...")
    run_command(f"statefulpy healthcheck --backend sqlite --path {sqlite_path}")
    
    # Try to migrate to Redis (this will fail if Redis is not running)
    print("\n5. Trying to migrate from SQLite to Redis...")
    print("   Note: This will fail if Redis is not running locally.")
    redis_result = run_command(f"statefulpy migrate --from sqlite --to redis --from-path {sqlite_path} --to-path {redis_url}")
    
    # Clean up
    print("\n6. Cleaning up...")
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)
    if os.path.exists(script_path):
        os.remove(script_path)
    
    print("\nDemo completed!")
    if redis_result != 0:
        print("\nNote: Redis migration failed. Make sure Redis is running if you want to test this feature.")

if __name__ == "__main__":
    main()
