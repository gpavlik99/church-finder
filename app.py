from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = "enter api key here"

@app.route('/api/find-churches', methods=['POST'])
def find_churches():
    data = request.json
    age = data.get('age')
    denomination = data.get('denomination', 'any')
    location = data.get('location')

    # ChatGPT prompt
    prompt = f"""
    Suggest churches within 20 miles of {location} for a person aged {age}, preferring {denomination} denomination.
    Return each church with a name, a brief summary, size, and why it might fit.
    """
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=3,  # Return 3 results
            stop=None
        )
        results = []
        for choice in response.choices:
            results.append({
                "name": choice.text.split("\n")[0],
                "summary": choice.text.split("\n")[1],
                "size": "Large",  # Mock size; real data can vary
                "reason": "Good community fit and values."
            })
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
