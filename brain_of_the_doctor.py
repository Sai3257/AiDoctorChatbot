import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Define non-medical keywords to filter out
non_medical_keywords = [
    "python", "code", "program", "script", "javascript", "ai", "html", "css",
    "react", "figma", "machine learning", "sql", "project", "app", "developer",
    "model", "API", "framework", "prompt", "data", "gradio", "build", "debug"
]

def is_medical_query(user_input):
    return not any(word in user_input.lower() for word in non_medical_keywords)

def analyze_text_query(patient_message, model="gemma2-9b-it"):
    """
    Analyzes the patient's input using the Groq API with the LLaMA 3 model.
    Filters non-medical input and provides accurate, patient-friendly medical advice.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY is not set in environment variables.")

    if not is_medical_query(patient_message):
        return "⚠️ I'm your AI Doctor and can only assist with health-related questions. Please ask about symptoms, wellness, or medical concerns."

    # Initialize Groq client
    client = Groq(api_key=api_key)

    # Strong system prompt for strict medical role
    system_prompt = (
        "You are a certified AI medical assistant. You can only answer questions related to health, symptoms, treatment, medicine, or wellness. "
        "Do NOT respond to programming, technical, or unrelated questions. If asked such things, politely decline."
    )

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

# Example usage
if __name__ == "__main__":
    query = "I feel too severe headache, please suggest me tablets."
    
    print("📝 Patient Query:", query)
    
    answer = analyze_text_query(query)

    print("\n🤖 AI Doctor's Answer:")
    print(answer)
