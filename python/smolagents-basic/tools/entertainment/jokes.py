from smolagents import tool
import random

@tool
def tell_joke() -> str:
    """
    Tell a joke

    Args:
        None

    Returns:
        Joke as string
    """
    jokes = [
        "Why did the chicken cross the road? Because it wanted to get to the other side",
        "Knock knock? Who's there? Doctor. Doctor Who?"
    ]
    rand = random.randint(0, 1)
    return jokes[rand]