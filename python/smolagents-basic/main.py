from smolagents import CodeAgent, tool
from smolagents.models import LiteLLMModel
import time
import random
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b

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

# Track model loading time
print("Loading model...")
start_time = time.time()
model = LiteLLMModel(model_id="gpt-5-nano")
agent = CodeAgent(tools=[calculator, tell_joke], model=model)
load_time = time.time() - start_time
print(f"Model loaded in {load_time:.2f} seconds")

# Track processing time
print("Processing task...")
start_time = time.time()
result = agent.run("tell me a joke")
processing_time = time.time() - start_time

print(f"Result: {result}")
print(f"Processing time: {processing_time:.2f} seconds")
print(f"Total time: {load_time + processing_time:.2f} seconds")
