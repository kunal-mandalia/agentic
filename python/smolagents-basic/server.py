from flask import Flask, request, jsonify
import time
from agents import create_basic_agent

# Initialize once at startup
print("Loading model... (this will take ~30 seconds on first run)")
start_time = time.time()
agent = create_basic_agent()
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
    return jsonify({'status': 'ready', 'model': 'gpt-5-nano'})

if __name__ == '__main__':
    print("Server ready! Test with:")
    print("curl -X POST http://localhost:5000/run -H 'Content-Type: application/json' -d '{\"task\": \"Please calculate 7 + 4\"}'")
    app.run(host='0.0.0.0', port=5000, debug=False)