import time
from agents import create_basic_agent

# Track model loading time
print("Loading model...")
start_time = time.time()
agent = create_basic_agent()
load_time = time.time() - start_time
print(f"Model loaded in {load_time:.2f} seconds")

# Track processing time
print("Processing task...")
start_time = time.time()
result = agent.run("Check my unread emails and give me the exact count number and whether I have any unread emails as true/false")
processing_time = time.time() - start_time

print(f"Result: {result}")
print(f"Processing time: {processing_time:.2f} seconds")
print(f"Total time: {load_time + processing_time:.2f} seconds")
