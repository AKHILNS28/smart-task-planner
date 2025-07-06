from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import requests
import os

app = Flask(__name__, static_folder='client')
CORS(app)

# Simulated DB file
TASKS_FILE = "tasks.json"

# OpenWeather API Key
API_KEY = "40f5f3a8eb7683389fbce7f33084bedd"

# Load tasks from JSON file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

# API endpoint to get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

# API endpoint to add a task
@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.get_json()
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return jsonify({"message": "Task added!"}), 201

# API endpoint to get weather info
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Bangalore")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"]
    }
    return jsonify(weather)

# Serve frontend index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
