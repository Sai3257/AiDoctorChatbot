import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

def analyze_text_query(patient_message, model="gemma2-9b-it"):
    """
    Analyzes the patient's input using the Groq API with the LLaMA 3 model.
    Provides a medically accurate and patient-friendly response.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY is not set in environment variables.")

    # Initialize Groq client
    client = Groq(api_key=api_key)

    # System prompt for doctor behavior
    system_prompt = (
        "You are a professional AI doctor. Provide medically accurate and patient-friendly responses. "
        "Keep the language clear and easy to understand. Be helpful and informative."
    )

    # Format messages properly
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": patient_message}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error getting AI doctor's response: {e}"

# Example usage (can be replaced with transcribed voice input)
if __name__ == "__main__":
    # Simulate patient query
    query = "I feel too severe headache, please suggest me tablets."
    
    print("📝 Patient Query:", query)
    
    # Get AI Doctor's response
    answer = analyze_text_query(query)

    # Output the AI doctor's answer
    print("\n🤖 AI Doctor's Answer:")
    print(answer)
