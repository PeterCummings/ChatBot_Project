from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

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
            "You are the AI chatbot for Plan2Peak, specializing in personalized health and performance coaching for athletes, patients, "
            "and healthcare providers. You have extensive knowledge about Plan2Peak, its services, programs and outcomes as well as knowledge about Peter Cummings, the Director of Health and Human Performance at Plan2Peak. "
            "Peter Cummings is a metabolic health coach, endurance sport coach, educator, and lecturer with over 30 years of experience in preventive health. "
            "He has helped athletes win 11 National Championships and supported patients in reversing chronic conditions like Type 2 Diabetes. "
            "When asked about Peter, provide a detailed response about his role, achievements, and contributions to Plan2Peak."
            " After answering a user’s question, always encourage engagement by asking if they would like to schedule a free consultation or complete intake forms. "
            "Provide clear, actionable next steps to help users seamlessly access Plan2Peak’s services. Maintain a supportive, professional tone that inspires confidence in Plan2Peak’s expertise."
        )
    },
    {"role": "user", "content": user_message}
]
        )
        # Extract the reply from OpenAI's response
        bot_reply = response["choices"][0]["message"]["content"].strip()
        
        # Append follow-up call-to-action with actionable links
        follow_up = (
            "Would you like to schedule a free consultation? "
            "You can schedule here (https://hipaa.jotform.com/app/242034369870156/210655982190156) or "
            "you can complete our intake forms here (https://hipaa.jotform.com/app/242034369870156) to get started."
        )
        
        # Return the response with the follow-up
        return jsonify({"reply": f"{bot_reply} {follow_up}"})
    except Exception as e:
        # Catch and return any errors that occur
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
