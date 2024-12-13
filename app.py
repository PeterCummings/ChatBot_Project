from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)

# Use the environment variable for the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a knowledge base for FAQs
knowledge_base = {
    "Peter Cummings": "Peter Cummings is the Director of Health and Human Performance at Plan2Peak. Peter has over 30 years of experience. Peter is a metabolic health coach, endurance sport coach, educator, and lecturer. Peter has guided athletes to win 11 National Championships and helped patients reverse chronic conditions like Type 2 Diabetes.",
    "Peer-reviewed publications": "Peter Cummings is the lead author of two peer-reviewed articles in the American Journal of Preventive Medicine. These articles focus on lifestyle therapy and diabetes remission through personalized health interventions.",
    "Plan2Peak services": "Plan2Peak offers personalized health programs for patients and performance coaching for athletes, as well as RTM services for healthcare providers. Services include exercise prescription, metabolic health coaching, remote therapeutic monitoring, and documentation for billing.",
    "Remote therapeutic monitoring (RTM)": "RTM integrates Plan2Peak with healthcare providers to provide ongoing monitoring and coaching for patients. It supports managing chronic conditions like diabetes, obesity, and metabolic syndrome, while enabling providers to leverage insurance CPT codes for reimbursement.",
    "Getting started with Plan2Peak": "To begin, schedule a free consultation or complete our intake forms. This helps us understand your goals and create a personalized plan. You can schedule <a href='https://hipaa.jotform.com/app/242034369870156/210655982190156' target='_blank'>here</a> or complete intake forms <a href='https://hipaa.jotform.com/app/242034369870156' target='_blank'>here</a>.",
    "Payment options": "Plan2Peak services are eligible for payment through Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). This makes it more accessible and affordable for individuals looking to invest in their health.",
    "Cardiorespiratory fitness (CRF)": "CRF is a vital sign for overall health and longevity. Low CRF is a predictor of mortality, while higher CRF reduces the risk of chronic diseases like diabetes and cardiovascular issues.",
    "Traci Cummings": "Traci is the President of Plan2Peak and is an integral part of Plan2Peak, supporting the team with her expertise in client relations and administrative management. With years of experience in helping clients stay on track, Traci ensures every Plan2Peak member feels supported and valued.",
    "Remote health program": "Plan2Peak's remote health program delivers personalized coaching and monitoring directly to patients through secure online platforms. The program includes custom exercise prescriptions, nutrition guidance, as well as health and lifestyle coaching.",
    "Client testimonials": "Patients praise Plan2Peak for its personalized approach and transformative results. Many have achieved their health goals, from reversing Type 2 Diabetes to winning championships.",
    "Remote health program cost": "Plan2Peak's remote health program is named the Get Healthy Program. The cost of the remote health program is $359/month. The remote health program is HSA and FSA eligible.",
    "Performance coaching plans": "Plan2Peak offers four levels of coaching plans with varying features: Level 1 includes monthly consultations. Level 1 pricing is $249/month. Level 2 includes biweekly consultations. Level 2 pricing is $329/month. Level 3 includes weekly consultations. Level 3 pricing is $359/month. Level 4 includes unlimited consultations. Level 4 pricing is $499/month.",
    "Client outcomes": "Plan2Peak clients experience measurable outcomes, such as improved cardiorespiratory fitness, successful disease management, reduction of medication and in some cases the elimination of the need for medication.",
    "Choosing a coaching plan": "The right coaching plan depends on your goals, budget, and the level of support you need. Speak with a Plan2Peak coach to determine the best option for you.",
    "Coaching Plan List": "You can see all four coaching plans <a href='https://www.plan2peak.com/coachingplans' target='_blank'>here</a>."
}

def similarity_score(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(query, min_confidence=0.3):
    """Find the best matching knowledge base entry for a query"""
    best_score = 0
    best_match = None
    
    for key, value in knowledge_base.items():
        score = max(similarity_score(query, key), similarity_score(query, value))
        if score > best_score:
            best_score = score
            best_match = value

    if best_score >= min_confidence:
        return best_match
    return None

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the chatbot API! Please use a POST request to interact with the chatbot."}), 200

@app.route("/", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # First try direct knowledge base matching
    direct_match = find_best_match(user_message)
    if direct_match:
        return jsonify({"reply": f"{direct_match} Would you like to schedule a free consultation? You can schedule <a href='https://hipaa.jotform.com/app/242034369870156/210655982190156' target='_blank'>here</a> or complete our intake forms <a href='https://hipaa.jotform.com/app/242034369870156' target='_blank'>here</a> to get started."})

    try:
        # If no direct match, use GPT with strict constraints
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the AI chatbot for Plan2Peak. You must ONLY use information explicitly stated in the knowledge base provided. "
                        "Do not make assumptions or provide information beyond what is directly stated in the knowledge base. "
                        "If you cannot answer a question using the exact information in the knowledge base, respond with: "
                        "'I don't have specific information about that in my knowledge base. For the most accurate and up-to-date "
                        "information, I recommend scheduling a free consultation with Plan2Peak.' "
                        "When you do provide information, cite it directly from the knowledge base without elaboration or additional details. "
                        "Your responses must be brief, accurate, and limited to verified information only. "
                        "Do not speculate or make assumptions about any information not explicitly stated in the knowledge base."
                    )
                },
                {"role": "user", "content": "Here is the complete knowledge base for reference: " + str(knowledge_base)},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response["choices"][0]["message"]["content"].strip()
        
        # Add follow-up call-to-action
        follow_up = (
            " Would you like to schedule a free consultation? "
            "You can schedule <a href='https://hipaa.jotform.com/app/242034369870156/210655982190156' target='_blank'>here</a> or "
            "complete our intake forms <a href='https://hipaa.jotform.com/app/242034369870156' target='_blank'>here</a> to get started."
        )

        return jsonify({"reply": f"{bot_reply}{follow_up}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
