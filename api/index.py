from flask import Flask, request, jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.agent import DebateAgent
 
app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"instructions": " POST a JSON to /chat endpoint with conversation_id & message fields, leave conversation_id in null to start a new conversation Define the topic of the conversation and what side of the conversation your bot should take "})



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    conversation_id = data["conversation_id"]
    message = data["message"]

    print(message)

    if conversation_id is None: # new conversation
        agent = DebateAgent()
        if agent.detect_topic(message):
            argument = agent.generate_argument()
            return jsonify({"conversation_id": agent.conversation_id, "message": agent.conversation_history})
        else: ## Unable to detect Topic
            return jsonify({"conversation_id": "", "message": [], "error": "The topic & the stance for the conversation can't be determined"})

    else: # existing conversation
        agent = DebateAgent()
        if agent.get_state(conversation_id):
            agent.update_history("user", message)
            argument = agent.generate_argument()

            return jsonify({"conversation_id": conversation_id, "message": agent.conversation_history})
        else:
            return jsonify({"conversation_id": conversation_id, "message": [], "error": "conversation_id not found"})
