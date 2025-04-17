# ai_doctor_response.py

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

def analyze_text_query(patient_message, model="llama3-8b-8192"):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)

    # System prompt to give guidance to the AI
    system_prompt = (
        "You are a professional AI doctor. Provide medically accurate and patient-friendly responses. "
        "Keep the language clear and easy to understand. Be helpful and informative."
    )

    # Define the conversation with system prompt and user query
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": patient_message}
    ]

    try:
        # Call the Groq API to get the response
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print(response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error getting AI doctor's response: {e}"
