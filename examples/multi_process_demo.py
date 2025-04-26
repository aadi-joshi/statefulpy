"""
Multi-Process Demo for StatefulPy

This example demonstrates how StatefulPy can share state across multiple
processes using the Redis backend. This is a common use case for distributed
applications, web servers, or worker processes that need to share state.
"""
import os
import time
import random
import multiprocessing
from statefulpy import stateful, set_backend

# Configure Redis as the backend with a fixed, distinct key prefix
# This ensures all processes use the same state storage
set_backend("redis", redis_url="redis://localhost:6379/0")

# Use a fixed function ID to ensure all processes access the same state
SHARED_STATE_KEY = "demo:shared_worker_counter"

@stateful(backend="redis", function_id=SHARED_STATE_KEY)
def worker_counter(worker_id, reset=False):
    """
    Track work done by different worker processes.
    Each process will increment its counter and see others' counts as well.
    """
    # Initialize state dict if needed - simplified initialization with better error handling
    if "workers" not in worker_counter.state or reset:
        worker_counter.state = {
            "total_work": 0,
            "workers": {},
            "last_update": time.time()
        }
    
    # Register this worker if first time
    if worker_id not in worker_counter.state["workers"]:
        worker_counter.state["workers"][worker_id] = 0
    
    # Do some "work" (if not just resetting)
    if not reset:
        work_units = random.randint(1, 5)
        
        # Update worker's progress and total
        worker_counter.state["workers"][worker_id] += work_units
        worker_counter.state["total_work"] += work_units
        worker_counter.state["last_update"] = time.time()
    
    return {
        "worker_id": worker_id,
        "my_work": worker_counter.state["workers"][worker_id],
        "total_work": worker_counter.state["total_work"],
        "all_workers": worker_counter.state["workers"].copy()
    }

def worker_process(worker_id, iterations):
    """Function that will run in a separate process"""
    print(f"Worker {worker_id} starting ({os.getpid()})")
    
    # Add a small delay to stagger process starts
    time.sleep(random.random() * 0.5)
    
    for i in range(iterations):
        # Get state with a fresh connection in each process
        result = worker_counter(worker_id)
        print(f"Worker {worker_id} - Iteration {i+1}: contributed {result['my_work']} units")
        print(f"  All workers: {result['all_workers']}, Total: {result['total_work']}")
        time.sleep(random.uniform(0.5, 1.5))  # Random sleep to simulate work
    
    # One final read to get latest state
    result = worker_counter(worker_id)
    print(f"Worker {worker_id} finished with final status: {result}")
    return result

def initialize_state(reset=False):
    """Pre-initialize the state before spawning processes"""
    try:
        # Clear existing state if requested
        if reset:
            worker_counter.state = {
                "total_work": 0,
                "workers": {},
                "last_update": time.time()
            }
            print("⚠️ Previous state has been reset")
        
        # Read current state
        result = worker_counter("init")
        print(f"State initialized in Redis: {result}")
    except Exception as e:
        print(f"State initialization error: {e}")

if __name__ == "__main__":
    print("Starting multi-process demo with Redis backend")
    print("This demo requires Redis to be running locally")
    print(f"Using shared state key: {SHARED_STATE_KEY}")
    print("----------------------------------------------")
    
    # Check if we should reset state
    reset_state = False  # Set to True to clear previous state
    
    try:
        # Initialize state before creating processes
        initialize_state(reset=reset_state)
        
        # Number of worker processes
        num_workers = 3
        iterations = 5
        
        # Create and start processes
        processes = []
        for i in range(num_workers):
            p = multiprocessing.Process(
                target=worker_process, 
                args=(f"worker-{i+1}", iterations)
            )
            processes.append(p)
            p.start()
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
        
        # Get final state to display
        final_state = worker_counter("main")
        
        print("\nAll workers completed!")
        print(f"Final state: {final_state}")
        print(f"Total work done: {final_state['total_work']}")
        print(f"Worker contributions: {final_state['all_workers']}")
        print("State is automatically persisted in Redis")
        print("You can restart this script to see that the counters continue")
        print("from where they left off.")
        print("\nTo reset counters to zero, change reset_state=True")
        
    except Exception as e:
        print(f"Error running multi-process demo: {e}")
        print("Make sure Redis is running locally on the default port")
