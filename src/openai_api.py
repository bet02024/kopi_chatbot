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

def generate_topic_prompt(message: str )
    prompt = f"""
    You are a specialized AI assistant responsible for parsing the initial message of a debate to identify its core topic and the bot's stance.

        Your task is to analyze the message provided below and output **only a valid JSON object**. Do not include any explanatory text before or after the JSON.

        The JSON object must contain two string fields:
        1.  `topic`: A string that neutrally and concisely summarizes the subject of the debate.
        2.  `stance`: A string that identifies the user's position (e.g., "For", "Against", "Pro", "Con", "In favor of", "Opposed to").

        ### Instructions:
        - Read the entire message to understand the full context.
        - The `topic` should be phrased as a neutral statement or question (e.g., "The viability of colonizing Mars" or "Should pineapple be on pizza?").
        - The `stance` should capture the bot's viewpoint. ("For the topic" | "Against the topic"), opposite to the user's viewpoint
        - If the topic or stance is ambiguous or not present, use "Unclear" for the respective field.

        ---
        ### Example ###

          "I want to talk about universal basic income. you will take be against the UBI."

        ### Expected JSON Output:

        ```json
        {
        "topic": "The implementation of Universal Basic Income (UBI)",
        "stance": "Against the topic"
        }
        ```

        -----------------------------------------------------------------

        **User Message:**  
         
        "{message}".

    """

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
        messages = [
            {"role": "system", "content": prompt},
        ] + conversation_history

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
