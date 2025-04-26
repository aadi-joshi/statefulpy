"""
Basic example demonstrating the use of the stateful decorator.
"""
from statefulpy import stateful

# The key change needed is to use state.value instead of direct attribute
@stateful(backend="sqlite", db_path="counter.db")
def counter():
    """A simple counter function with persistent state."""
    # Access state via the state dictionary
    if "value" not in counter.state:
        counter.state["value"] = 0
    
    # Increment counter
    counter.state["value"] += 1
    
    # Return current value
    return counter.state["value"]


if __name__ == "__main__":
    print(f"Counter value: {counter()}")
    print(f"Counter value: {counter()}")
    print(f"Counter value: {counter()}")
    print("Run the script again to see that the counter continues from where it left off!")
