from openai_api import get_openai_response, generate_prompt, generate_topic_prompt
import uuid
from pickledb import PickleDB
import json

db = PickleDB("conversations.json")


class DebateAgent:
    """  An AI agent designed to participate in a debate, holding a specific stance
         and attempting to persuade its opponent.
    """

    def __init__(self, topic="", stance=""):
        """ Initializes the DebateAgent Args:
                topic (str): The topic of the debate.
                stance (str): The agent's position ("For the topic" | "Against the topic").
        """
        self.topic = topic
        self.stance = stance
        self.conversation_id = str(uuid.uuid4())
        self.conversation_history = []

    def get_state(self, conversation_id: str) -> bool:
        """ Retrieve the DebateAgent from conversation_id Args:
                conversation_id (str): id of the conversation.
        """
        conversation = db.get(conversation_id)
        if conversation:
            self.topic = conversation['topic']
            self.conversation_id = conversation_id
            self.stance = conversation['stance']
            self.conversation_history = conversation["history"]
            return True
        else:
            return False

    def save_conversation(self, message):
        """  Append a message to the history and save full conversation state.  """
        conversation = db.get(self.conversation_id)
        if conversation is None:
            conversation = {}
            conversation["topic"] = self.topic
            conversation["stance"] = self.stance
            conversation["history"] = []

        self.conversation_history.append(message)
        #conversation["history"].append(message)
        db.set(self.conversation_id, conversation)
        db.save()

    def detect_topic(self, message) -> bool:
        """  Detect Topic & Stance from the first message in the conversation.
        """
        try:
            prompt =  generate_topic_prompt(message)
            response = get_openai_response(prompt, [])
            print(response)
            response_json = json.loads(response)
            if response_json['topic'] and response_json['stance']:
                self.topic = response_json['topic']
                self.stance = response_json['stance']
                self.conversation_id = str(uuid.uuid4())
                self.conversation_history = []
                return True
            else:
                return False
        except Exception as e:
            print(f"An unexpected error occurred 1: {e}")
            return False

    def generate_argument(self) -> str:
        """  Generates the next argument in the debate and updates conversation.
                Returns str: The generated argument as a string.
        """
        try:
            prompt = generate_prompt(self.topic, self.stance)
            response = get_openai_response(prompt, self.conversation_history)
            self.update_history("bot", response)
            return response
        except Exception as e:
            print(f"An unexpected error occurred 2: {e}")
            return "An unexpected error occurred."

    def update_history(self, role: str, text: str):
        """  Updates the conversation history for this agent, and persists to PickleDB.
                Args:
                    role (str): The role of the speaker ('user' or 'bot' ).
                    text (str): The text of the statement.
        """
        self.save_conversation({"role": role, "message": text})
