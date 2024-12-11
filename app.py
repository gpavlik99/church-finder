from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with the front end

# Set up OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/api/get-churches', methods=['POST'])
def get_churches():
    # Extract data from the frontend
    data = request.json
    age = data.get('age')
    denomination = data.get('denomination', 'any')
    location = data.get('location')

    # Build the ChatGPT prompt
    prompt = f"""
    Suggest churches within 20 miles of {location} for a person aged {age}, 
    preferring {denomination} denomination. 
    Return each church with a name, a brief summary, size, and why it might fit.
    """

    try:
        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )

        # Return the results to the frontend
        return jsonify({"results": response.choices[0].text.strip()})
    except Exception as e:
        # Handle errors and return a 500 status
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with the front end

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/get-churches', methods=['POST'])
def get_churches():
    data = request.json
    age = data.get('age')
    denomination = data.get('denomination', 'any')
    location = data.get('location')

    prompt = f"""
    Suggest churches within 20 miles of {location} for a person aged {age}, 
    preferring {denomination} denomination. 
    Return each church with a name, a brief summary, size, and why it might fit.
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return jsonify({"results": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)