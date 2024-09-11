from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

def get_ai_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-2.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    try:
        response = requests.post(ANTHROPIC_API_URL, json=data, headers=headers)
        print("Status Code:", response.status_code)
        print("API Response:", response.text)
        response.raise_for_status()
        response_json = response.json()
        print("JSON Response:", response_json)
        response_text = response_json['content'][0]['text']
        return response_text
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return f"An error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fitness', methods=['POST'])
def fitness():
    goals = request.form['goals']
    equipment = request.form['equipment']
    time = request.form['time']
    prompt = f"Create a workout routine for someone with the following goals: {goals}, available equipment: {equipment}, and time constraints: {time}."
    response = get_ai_response(prompt)
    return jsonify({"response": response})

@app.route('/nutrition', methods=['POST'])
def nutrition():
    restrictions = request.form['restrictions']
    preferences = request.form['preferences']
    ingredients = request.form['ingredients']
    prompt = f"Suggest a meal plan and recipe for someone with dietary restrictions: {restrictions}, food preferences: {preferences}, and available ingredients: {ingredients}."
    response = get_ai_response(prompt)
    return jsonify({"response": response})

@app.route('/mental_health', methods=['POST'])
def mental_health():
    mood = request.form['mood']
    stress_level = request.form['stress_level']
    sleep_hours = request.form['sleep_hours']
    prompt = f"Provide mental health tips for someone with the current mood: {mood}, stress level: {stress_level} out of 10, and who sleeps {sleep_hours} hours per night."
    response = get_ai_response(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
