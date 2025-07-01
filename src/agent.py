from openai_api import get_openai_response, generate_prompt
import uuid
from pickledb import PickleDB

db = PickleDB("data/conversations.json")


class DebateAgent:
    """  An AI agent designed to participate in a debate, holding a specific stance
         and attempting to persuade its opponent.
    """

    def __init__(self, topic: str, stance: str):
        """ Initializes the DebateAgent Args:
                topic (str): The topic of the debate.
                stance (str): The agent's position ("For the topic" | "Against the topic").
        """
        self.topic = topic
        self.stance = stance
        self.conversation_id = str(uuid.uuid4())
        self.conversation_history = []
        self.save_conversation(None, initial=True)

    def get_state(self, conversation_id: str) -> bool:
        """ Retrieve the DebateAgent from conversation_id Args:
                conversation_id (str): id of the conversation.
        """
        conversation = db.get(self.conversation_id)
        if conversation:
            self.topic = conversation['topic']
            self.stance = conversation['stance']
            self.conversation_history = conversation["history"]
            return True
        else:
            return False

    def save_conversation(self, message, initial=False):
        """  Append a message to the history and save full conversation state.  """
        conversation = db.get(self.conversation_id) or {}
        conversation["topic"] = self.topic
        conversation["stance"] = self.stance
        if initial:
            conversation["history"] = []
        else:
            conversation["history"] = self.conversation_history

        if message:
            conversation["history"].append(message)
            self.conversation_history.append(message)

        db.set(self.conversation_id, conversation)

    def get_conversation(self):
        """  Returns the conversation object from db for this agent.    """
        return db.get(self.conversation_id) or {
            "topic": self.topic,
            "stance": self.stance,
            "history": []
        }

    def get_history(self):
        """   Returns history array for this conversation.    """
        conv = db.get(self.conversation_id)
        self.conversation_history = conv["history"]
        return conv["history"] if conv and "history" in conv else []

    def generate_argument(self) -> str:
        """  Generates the next argument in the debate and updates conversation.
                Returns str: The generated argument as a string.
        """
        prompt = generate_prompt(self.topic, self.stance)
        response = get_openai_response(prompt, self.conversation_history)
        self.update_history("assistant", response)
        return response

    def update_history(self, role: str, text: str):
        """  Updates the conversation history for this agent, and persists to PickleDB.
                Args:
                    role (str): The role of the speaker ('user' for opponent, 'assistant' for self).
                    text (str): The text of the statement.
        """
        self.save_conversation({"role": role, "content": text})


async def get_response(conversation):
    chat_messages = [
        ChatMessage(role=msg["role"], content=msg["message"])
        for msg in conversation
    ]
    response = await agent.chat_async(chat_messages)
    return response.content
