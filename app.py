from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Use the environment variable for the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    # Responds to GET requests with a welcome message
    return jsonify({"message": "Welcome to the chatbot API! Please use a POST request to interact with the chatbot."}), 200

@app.route("/", methods=["POST"])
def chatbot():
    # Get the user's message from the POST request JSON
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Pass the user message to OpenAI to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}  # Use the user's message dynamically
            ]
        )
        # Extract the reply from OpenAI's response
        bot_reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        # Catch and return any errors that occur
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
