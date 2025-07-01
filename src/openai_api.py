import os
import openai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Fetch the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in a .env file or your system environment.")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def get_openai_response(prompt: str, conversation_history: list) -> str:
    try:
        # Combine the system prompt with the conversation history
        messages = [
            {"role": "system", "content": prompt},
        ] + conversation_history

        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",   
            messages=messages,
            temperature=0.8,  # Higher temperature for more creative/less predictable responses
            max_tokens=250,
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
