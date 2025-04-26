"""
StatefulPy Complete Demo
========================

This file demonstrates the key features of StatefulPy through practical examples.
StatefulPy provides transparent persistent state management for Python functions.

Key concepts demonstrated:
1. Basic stateful functions with SQLite backend
2. Persistent counters and caches
3. Complex state with dictionaries and lists
4. Redis backend for distributed applications
5. Global configuration
6. Error handling and best practices
"""

import time
import random
import os
from datetime import datetime
from statefulpy import stateful, set_backend

# -----------------------------------------------------------------------------
# PART 1: Basic Usage - SQLite Backend (Default)
# -----------------------------------------------------------------------------
print("\n=== PART 1: Basic Usage with SQLite Backend ===\n")

@stateful(backend="sqlite", db_path="demo.db")
def simple_counter():
    """
    A basic counter function demonstrating stateful operation.
    
    Each call to this function will increment the counter and return the value.
    The counter value persists between runs of the program.
    """
    # Initialize state if this is the first run (or after DB was deleted)
    if "value" not in simple_counter.state:
        simple_counter.state["value"] = 0
    
    # Increment the counter
    simple_counter.state["value"] += 1
    
    return simple_counter.state["value"]

# Let's call our counter function multiple times
print(f"Counter: {simple_counter()}")  # 1 on first run, but increases on subsequent runs
print(f"Counter: {simple_counter()}")  # 2 on first run
print(f"Counter: {simple_counter()}")  # 3 on first run

print("\nNow restart this script to see that the counter continues from where it left off!")
print("The state is automatically saved to demo.db in the current directory.")


# -----------------------------------------------------------------------------
# PART 2: Memoization/Caching with Stateful Functions
# -----------------------------------------------------------------------------
print("\n=== PART 2: Function Caching/Memoization ===\n")

@stateful(backend="sqlite", db_path="demo.db")
def fibonacci(n):
    """
    Calculate the nth Fibonacci number with persistent caching.
    
    This function demonstrates how stateful functions can be used
    for memoization/caching, with the cache persisting between runs.
    
    This version uses an iterative approach to avoid recursion lock issues.
    """
    # Initialize the cache if it doesn't exist
    if "cache" not in fibonacci.state:
        print("Initializing fibonacci cache...")
        fibonacci.state["cache"] = {0: 0, 1: 1}
    
    # Check if we've already calculated this value
    if n in fibonacci.state["cache"]:
        print(f"Cache hit for fibonacci({n})")
        return fibonacci.state["cache"][n]
    
    # Calculate iteratively to avoid recursive locking issues
    print(f"Cache miss for fibonacci({n}), calculating iteratively...")
    
    # Find the highest number we've already cached
    highest_cached = max(fibonacci.state["cache"].keys())
    if highest_cached < n:
        # Start from our highest cached value
        a = fibonacci.state["cache"][highest_cached-1] if highest_cached > 0 else 0
        b = fibonacci.state["cache"][highest_cached]
        
        # Fill in all missing values in sequence
        for i in range(highest_cached + 1, n + 1):
            a, b = b, a + b
            fibonacci.state["cache"][i] = b
            print(f"Cached fibonacci({i}) = {b}")
    
    return fibonacci.state["cache"][n]

# Calculate some Fibonacci numbers
print(f"Fibonacci(10): {fibonacci(10)}")
print(f"Fibonacci(15): {fibonacci(15)}")

# Run these again - they should be instant cache hits on subsequent runs
print("\nCalculating again (should be cached):")
print(f"Fibonacci(10): {fibonacci(10)}")
print(f"Fibonacci(15): {fibonacci(15)}")


# -----------------------------------------------------------------------------
# PART 3: Complex State with Dictionary Tracking
# -----------------------------------------------------------------------------
print("\n=== PART 3: Complex State Management ===\n")

@stateful(backend="sqlite", db_path="demo.db", serializer="json")
def word_counter(text=None):
    """
    Count word occurrences across multiple calls with persistent state.
    This demonstrates handling complex nested dictionary state.
    
    Note: Using JSON serializer to make the DB human-readable.
    """
    # Initialize state if needed
    if "stats" not in word_counter.state:
        word_counter.state["stats"] = {
            "total_calls": 0,
            "total_words": 0,
            "word_counts": {},
            "last_updated": None
        }
    
    # Update call count
    word_counter.state["stats"]["total_calls"] += 1
    word_counter.state["stats"]["last_updated"] = str(datetime.now())
    
    # Process new text if provided
    if text:
        # Simple word splitting (in a real app, you'd use better tokenization)
        words = text.lower().split()
        word_counter.state["stats"]["total_words"] += len(words)
        
        # Count words
        for word in words:
            # Clean punctuation (simple approach)
            word = word.strip('.,!?;:()"\'')
            if word:
                word_counter.state["stats"]["word_counts"][word] = \
                    word_counter.state["stats"]["word_counts"].get(word, 0) + 1
    
    return word_counter.state["stats"]

# Process some text
print("Adding text to our word counter...")
word_counter("StatefulPy makes functions remember their state between calls.")
word_counter("This state persists even when you restart your application.")
word_counter("StatefulPy uses SQLite or Redis to store the state securely.")

# Get current statistics
stats = word_counter()
print(f"\nTotal calls: {stats['total_calls']}")
print(f"Total words processed: {stats['total_words']}")
print(f"Unique words: {len(stats['word_counts'])}")
print(f"Top 5 words: {sorted(stats['word_counts'].items(), key=lambda x: x[1], reverse=True)[:5]}")
print(f"Last updated: {stats['last_updated']}")

print("\nTry adding more text when you run this script again!")


# -----------------------------------------------------------------------------
# PART 4: API Rate Limiter Simulation
# -----------------------------------------------------------------------------
print("\n=== PART 4: API Rate Limiter Simulation ===\n")

@stateful(backend="sqlite", db_path="demo.db")
def api_request(endpoint):
    # Initialize state if needed
    if not hasattr(api_request, 'calls'):
        api_request.calls = {}
    
    # Get current time
    now = time.time()
    
    # Initialize counter for this endpoint if needed
    if endpoint not in api_request.calls:
        api_request.calls[endpoint] = []
    
    # Remove requests older than 60 seconds
    api_request.calls[endpoint] = [t for t in api_request.calls[endpoint] if now - t < 60]
    
    # Add current request time
    api_request.calls[endpoint].append(now)
    
    # Check if rate limit exceeded
    if len(api_request.calls[endpoint]) > 5:
        return "Rate limit exceeded"
    
    return f"Success - {len(api_request.calls[endpoint])} calls in the last minute"

# Make several API requests
endpoints = ["/users", "/products", "/orders"]

print("Making API requests with rate limiting...")
for i in range(7):  # Intentionally go over the limit
    endpoint = random.choice(endpoints)
    response = api_request(endpoint)
    print(f"Request {i+1} to {endpoint}: {response}")
    time.sleep(0.5)  # Small delay between requests


# -----------------------------------------------------------------------------
# PART 5: Redis Backend for Distributed Applications
# -----------------------------------------------------------------------------
print("\n=== PART 5: Redis Backend (Distributed State) ===\n")
print("Note: This requires a Redis server. If not available, this will error.")
print("If Redis isn't running, you can comment out this section.\n")

try:
    # Global configuration to use Redis
    set_backend("redis", redis_url="redis://localhost:6379/0")
    
    @stateful  # No backend specified, uses the global config (Redis)
    def distributed_counter():
        """
        A counter function using Redis as the backend.
        
        This demonstrates using StatefulPy in distributed environments
        where multiple processes or servers need to share state.
        """
        if "count" not in distributed_counter.state:
            distributed_counter.state["count"] = 0
        
        distributed_counter.state["count"] += 1
        return distributed_counter.state["count"]
    
    # Call the distributed counter
    print(f"Distributed counter: {distributed_counter()}")
    print(f"Distributed counter: {distributed_counter()}")
    
    print("\nThis counter's state is stored in Redis and can be accessed by multiple processes")
    print("or even different machines with access to the same Redis instance.")
    
except Exception as e:
    print(f"Redis example error: {e}")
    print("Make sure Redis is running or comment out this section.")


# -----------------------------------------------------------------------------
# PART 6: Custom Behavior and Best Practices
# -----------------------------------------------------------------------------
print("\n=== PART 6: Advanced Usage and Best Practices ===\n")

@stateful(backend="sqlite", db_path="demo.db")
def analytics_tracker(event=None, metadata=None):
    """
    Track analytics events with persistent storage.
    
    This demonstrates patterns for:
    - Initializing complex state
    - Handling different types of input
    - Managing growing collections
    """
    # Initialize with a more complex structure
    if "data" not in analytics_tracker.state:
        analytics_tracker.state["data"] = {
            "events": [],
            "event_counts": {},
            "first_seen": str(datetime.now()),
            "last_seen": None,
        }
    
    # Update last seen timestamp
    analytics_tracker.state["data"]["last_seen"] = str(datetime.now())
    
    # Process new event if provided
    if event:
        # Store event with metadata and timestamp
        event_data = {
            "event": event,
            "metadata": metadata or {},
            "timestamp": str(datetime.now())
        }
        
        # Add to events list (keep only the last 100 events to prevent unbounded growth)
        analytics_tracker.state["data"]["events"].append(event_data)
        analytics_tracker.state["data"]["events"] = analytics_tracker.state["data"]["events"][-100:]
        
        # Update event counts
        analytics_tracker.state["data"]["event_counts"][event] = \
            analytics_tracker.state["data"]["event_counts"].get(event, 0) + 1
    
    return analytics_tracker.state["data"]

# Track some events
print("Tracking analytics events...")
analytics_tracker("page_view", {"page": "home"})
analytics_tracker("button_click", {"button_id": "sign_up", "position": "header"})
analytics_tracker("form_submit", {"form_id": "contact", "fields": 4})

# Get analytics data
data = analytics_tracker()
print(f"\nEvent statistics:")
print(f"First seen: {data['first_seen']}")
print(f"Last seen: {data['last_seen']}")
print(f"Event counts: {data['event_counts']}")
print(f"Last event: {data['events'][-1]}")

# -----------------------------------------------------------------------------
# Cleanup & Summary
# -----------------------------------------------------------------------------
print("\n=== Summary and Next Steps ===\n")
print("This demo showcased how StatefulPy provides persistent state for functions.")
print("Key aspects demonstrated:")
print("1. Basic stateful functions with automatic persistence")
print("2. Memoization and caching across program runs")
print("3. Complex state management with nested structures")
print("4. Stateful patterns like rate limiting")
print("5. Redis backend for distributed applications")
print("6. Best practices for stateful function design")

print("\nTo explore further:")
print("- Try uncommenting the cleanup code below to reset all examples")
print("- Check the CLI tools: 'python -m statefulpy healthcheck --backend sqlite --path demo.db'")
print("- Look at the source code to understand the implementation")

# Uncomment to reset all examples by deleting the database
"""
if os.path.exists("demo.db"):
    print("\nCleaning up demo.db...")
    os.remove("demo.db")
    print("Database deleted. Next run will start fresh.")
"""
