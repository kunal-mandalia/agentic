from flask import Flask, request, jsonify
from smolagents import CodeAgent, tool
from smolagents.models import LiteLLMModel
import time
import random
from dotenv import load_dotenv

load_dotenv()

# Initialize once at startup
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
    rand = random.randint(0 ,1)
    return jokes[rand]

print("Loading model... (this will take ~30 seconds on first run)")
start_time = time.time()
model = LiteLLMModel(model_id="gpt-5-nano")
agent = CodeAgent(tools=[calculator, tell_joke], model=model)
load_time = time.time() - start_time
print(f"Model loaded in {load_time:.2f} seconds")

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_agent():
    start_time = time.time()
    task = request.json.get('task')
    result = agent.run(task)
    processing_time = time.time() - start_time

    return jsonify({
        'result': result,
        'processing_time': f"{processing_time:.2f}s"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ready', 'model': 'ollama/phi3:latest'})

if __name__ == '__main__':
    print("Server ready! Test with:")
    print("curl -X POST http://localhost:5000/run -H 'Content-Type: application/json' -d '{\"task\": \"Please calculate 7 + 4\"}'")
    app.run(host='0.0.0.0', port=5000, debug=False)