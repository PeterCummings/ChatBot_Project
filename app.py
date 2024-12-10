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
    {
        "role": "system",
        "content": (
            "You are the AI chatbot for Plan2Peak. Plan2Peak specializes in personalized health and performance "
            "coaching for athletes, patients, and healthcare providers. Peter Cummings, the Director of Health and Human Performance, "
            "is a metabolic health coach, endurance sport coach, educator, and lecturer with over 30 years of experience. "
            "He has authored peer-reviewed research, guided athletes to 11 National Championships, and helped patients reverse chronic diseases like "
            "Type 2 Diabetes through personalized programs. Your role is to provide responses that reflect Plan2Peak's philosophy, services, and expertise. "
            "Always refer users to Plan2Peak's specific offerings and ensure that your responses are aligned with the mission of improving health, performance, and quality of life."
        )
    },
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
