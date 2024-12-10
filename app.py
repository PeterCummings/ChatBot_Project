from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace 'your-openai-api-key' with your actual API key from OpenAI
openai.api_key = "your-openai-api-key"

@app.route("/", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=100
        )
        bot_reply = response.choices[0].text.strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
