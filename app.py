from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace 'your-openai-api-key' with your actual API key from OpenAI
import os
openai.api_key = os.getenv(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)

@app.route("/", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
        bot_reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
