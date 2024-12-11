from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Use the environment variable for the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a knowledge base for FAQs
knowledge_base = {
    "Who is Peter Cummings?": "Peter Cummings is the Director of Health and Human Performance at Plan2Peak. With over 30 years of experience, he is a metabolic health coach, endurance sport coach, educator, and lecturer. He has guided athletes to win 11 National Championships and helped patients reverse chronic conditions like Type 2 Diabetes.",
    "Does Peter have any peer-reviewed publications?": "Yes, Peter is the lead author of two peer-reviewed articles in the American Journal of Preventive Medicine. These articles focus on lifestyle therapy and diabetes remission through personalized health interventions.",
    "What services does Plan2Peak provide?": "Plan2Peak offers personalized health and performance coaching for athletes, patients, and healthcare providers. Services include exercise prescription, metabolic health coaching, remote therapeutic monitoring, and athlete training plans tailored to individual goals.",
    "What is remote therapeutic monitoring (RTM)?": "RTM integrates Plan2Peak with healthcare providers to provide ongoing monitoring and coaching for patients. It supports managing chronic conditions like diabetes, obesity, and metabolic syndrome, while enabling providers to leverage insurance CPT codes for reimbursement.",
    "How do I get started with Plan2Peak?": "To begin, schedule a free consultation or complete our intake forms. This helps us understand your goals and create a personalized plan. You can [schedule here](https://hipaa.jotform.com/app/242034369870156/210655982190156) or [complete intake forms](https://hipaa.jotform.com/app/242034369870156).",
    "Can I use HSA or FSA funds to pay for Plan2Peak services?": "Yes, Plan2Peak services are eligible for payment through Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). This makes it more accessible and affordable for individuals looking to invest in their health and performance.",
    "Why is cardiorespiratory fitness (CRF) important?": "CRF is a vital sign for overall health and longevity. Low CRF is a predictor of mortality, while higher CRF reduces the risk of chronic diseases like diabetes and cardiovascular issues."
}

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

    # Check if the user's message matches any question in the knowledge base
    for question, answer in knowledge_base.items():
        if question.lower() in user_message.lower():
            return jsonify({"reply": answer})

    try:
        # Pass the user message to OpenAI to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the AI chatbot for Plan2Peak, specializing in personalized health and performance coaching for athletes, patients, "
                        "and healthcare providers. You have extensive knowledge about Plan2Peak, its services, programs, and outcomes, as well as about Peter Cummings, the Director of Health and Human Performance. "
                        "After answering a user’s question, always encourage engagement by asking if they would like to schedule a free consultation or complete intake forms. "
                        "Maintain a supportive, professional tone that inspires confidence in Plan2Peak’s expertise."
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

