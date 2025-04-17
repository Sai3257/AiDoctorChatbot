import speech_recognition as sr
import os
from groq import Groq

# Record and save voice as WAV
def get_voice_input():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎙️ Please speak your query...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Save voice to file
        with open("patient_voice.wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("💾 Voice saved as patient_voice.wav")

        return "patient_voice.wav"

    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"🔌 Could not request results; {e}")

# Transcribe audio using Groq API
def transcribe_audio(audio_file_path):
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    if not GROQ_API_KEY:
        print("❗ GROQ_API_KEY not set in environment.")
        return

    client = Groq(api_key=GROQ_API_KEY)

    stt_model = "distil-whisper-large-v3-en"

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file
        )
    
    print("📝 Transcribed Text:", transcription.text)

    return transcription.text

    # Save to a file
    # with open("patient_query.txt", "w", encoding="utf-8") as f:
    #     f.write(transcription.text)

# if __name__ == "__main__":
#     audio_path = get_voice_input()
#     if audio_path:
#         transcribe_audio(audio_path)
