import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os

import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

def initialize_model():
    model_preferences = [
        'gemini-2.0-flash',
        'gemini-2.0-flash-lite'
    ]
    for model_name in model_preferences:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("Test connection")
            return model
        except Exception:
            continue
    raise Exception("Could not initialize any of the preferred models")

try:
    model = initialize_model()
    chat = model.start_chat(history=[])
except Exception as e:
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'status': 'error', 'response': "Please enter a message"})
    try:
        response = chat.send_message(
            user_message,
            generation_config={"max_output_tokens": 1000, "temperature": 0.7}
        )
        return jsonify({'status': 'success', 'response': response.text})
    except Exception as e:
        return jsonify({'status': 'error', 'response': f"An error occurred: {str(e)}"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
