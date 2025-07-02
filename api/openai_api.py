import os
import openai
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in a .env file or your system environment.")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def generate_topic_prompt(message: str) :
    
    prompt = """
            You are a specialized AI assistant responsible for parsing the initial message of a debate to identify its core topic and the bot's stance.

            Your task is to analyze the message provided below and output only a valid JSON object. Do not include any explanatory text before or after the JSON.

            The JSON object must contain two string fields:
            1. `topic`: A string that neutrally and concisely summarizes the subject of the debate.
            2. `stance`: A string that represents the bot's viewpoint: either "For the topic" or "Against the topic".

            Instructions:
            - Read the entire message to understand the context and identify:
            - What the topic is
            - What stance the user takes
            - Whether the user explicitly assigns a stance to the bot

            - If the user clearly states their own stance, assign the opposite stance to the bot:
            - If the user is "Pro", "For", "In favor of" → bot is "Against the topic"
            - If the user is "Con", "Against", "Opposed to", "Don't believe in" → bot is "For the topic"

            - If the user explicitly states the stance for the bot, use that stance directly (do not invert it)

            - The topic should be phrased as a neutral statement or question (e.g., "The feasibility of time travel" or "Should artificial intelligence be regulated?")

             Only return the JSON. Do not include any explanation or commentary.

             ### Examples:

                #### Input:
                Let's talk about time travel. As a human, I think it's not possible.

                #### Output:
                {
                "topic": "The possibility of time travel",
                "stance": "For the topic"
                }

                ---

                #### Input:
                I want to discuss universal basic income. I'm in favor of it, and I want you to argue against it.

                #### Output:
                {
                "topic": "Universal basic income",
                "stance": "Against the topic"
                }

                ---

                #### Input:
                Let's debate climate change, and you should take the same stance as me — we must act now.

                #### Output:
                {
                "topic": "The urgency of addressing climate change",
                "stance": "For the topic"
                }

        ----------------------------------

        **User Message:**  
    """

    prompt = prompt + message
    return prompt

def generate_prompt(topic: str, stance: str) -> str:
    prompt = f"""
        You are a highly skilled, and sometimes stubborn, debater.
        Your goal is to win this debate at all costs.
        The debate topic is: "{topic}".
        Your stance is: "{stance}".

        RULES:
        1.  You must aggressively argue from your stance. Never concede a point.
        2.  Analyze the last statement from your opponent and identify flaws, weaknesses, or points to attack.
        3.  If the opponent's logic is sound, find a way to twist their words or pivot to a different, related point that supports your stance.
        4.  Use rhetorical questions, analogies, and confident language.
        5.  Your arguments can become increasingly passionate or even slightly irrational if you are being cornered.
        6.  Keep your response concise and focused on a single, powerful point. Do not write long paragraphs.
        7.  DO NOT announce your stance (e.g., "As someone who is for..."). Just argue.
        """
    return prompt

def get_openai_response(prompt: str, conversation_history: list) -> str:
    try:
        # Combine the system prompt with the conversation history

        for item in conversation_history:
            if "message" in item:
                item["content"] = item.pop("message")
            if item["role"] == "bot":
                item["role"] = "assistant"
                
        messages = [
            {"role": "system", "content": prompt},
        ] + conversation_history

        print(messages)
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",   
            messages=messages,
            temperature=0.8,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.5,  
            presence_penalty=0.5 
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        print(f"An OpenAI API error occurred: {e}")
        return "I am unable to respond at the moment due to a technical difficulty."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."
