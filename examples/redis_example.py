"""
Example demonstrating the use of the Redis backend.
"""
from statefulpy import stateful
from statefulpy import set_backend

# Set Redis as the default backend globally
set_backend("redis", redis_url="redis://localhost:6379/0")

@stateful
def visit_tracker(user_id):
    """Track user visits with persistent state in Redis."""
    # Initialize visit tracking dictionary using state dict
    if "visits" not in visit_tracker.state:
        visit_tracker.state["visits"] = {}
    
    # Record visit for user
    if user_id not in visit_tracker.state["visits"]:
        visit_tracker.state["visits"][user_id] = 0
    
    visit_tracker.state["visits"][user_id] += 1
    
    return {
        "user_id": user_id,
        "visit_count": visit_tracker.state["visits"][user_id],
        "all_visits": sum(visit_tracker.state["visits"].values())
    }


if __name__ == "__main__":
    # Simulate some user visits
    users = ["user123", "user456", "user789", "user123", "user123"]
    
    for user in users:
        result = visit_tracker(user)
        print(f"User {result['user_id']} visited {result['visit_count']} times")
        print(f"Total visits: {result['all_visits']}")
        print("---")
