import gradio as gr
import os
from gtts import gTTS
from pydub import AudioSegment
import platform
import subprocess
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

from brain_of_the_doctor import analyze_text_query
from voice_of_the_patient import transcribe_audio

load_dotenv()

# ------------------------ Audio Utilities ------------------------

def convert_mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def text_to_speech(input_text, output_filepath, lang_code="en"):
    audio_obj = gTTS(text=input_text, lang=lang_code, slow=False)
    audio_obj.save(output_filepath)

def clean_text_for_audio(text):
    import re
    return re.sub(r"\*", "", text)

# ------------------------ AI Doctor Logic ------------------------

def generate_response(text):
    return analyze_text_query(text)

language_codes = {
    "English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta", "Kannada": "kn", "Malayalam": "ml",
    "Bengali": "bn", "Japanese": "ja", "French": "fr", "German": "de", "Spanish": "es", "Italian": "it",
    "Arabic": "ar", "Russian": "ru", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Urdu": "ur", "Gujarati": "gu", "Punjabi": "pa", "Marathi": "mr", "Odia": "or", "Sinhala": "si",
    "Thai": "th", "Turkish": "tr", "Vietnamese": "vi", "Korean": "ko", "Ukrainian": "uk", "Dutch": "nl",
    "Romanian": "ro", "Polish": "pl", "Czech": "cs", "Swedish": "sv", "Hungarian": "hu", "Finnish": "fi",
    "Greek": "el", "Hebrew": "he", "Croatian": "hr", "Bulgarian": "bg", "Slovak": "sk", "Serbian": "sr",
    "Danish": "da", "Norwegian": "no", "Lithuanian": "lt", "Latvian": "lv", "Estonian": "et",
    "Icelandic": "is", "Irish": "ga", "Swahili": "sw"
}

def translate_response(response, selected_language):
    lang_code = language_codes.get(selected_language, "en")
    if lang_code != "en":
        try:
            response = GoogleTranslator(source='en', target=lang_code).translate(response)
        except Exception as e:
            response = f"Translation Error: {e}"
    return response, lang_code

def create_welcome_audio():
    welcome_text = "Speak your health concern. The AI doctor will understand and respond with care."
    output_path = "welcome_message.mp3"
    if not os.path.exists(output_path):
        tts = gTTS(text=welcome_text, lang="en", slow=False)
        tts.save(output_path)
    return output_path

welcome_audio_path = create_welcome_audio()

def process_patient_query(audio_file, selected_language):
    try:
        transcribed_text = transcribe_audio(audio_file)
        response = generate_response(transcribed_text)
        response, lang_code = translate_response(response, selected_language)
        clean_response = clean_text_for_audio(response)

        output_audio = "doctor_response.mp3"
        text_to_speech(clean_response, output_audio, lang_code)

        if platform.system() == "Windows":
            wav_path = output_audio.replace(".mp3", ".wav")
            convert_mp3_to_wav(output_audio, wav_path)
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync()'])

        return response, output_audio

    except Exception as e:
        return f"Error: {str(e)}", None

# ------------------------ Authentication ------------------------

USER_CREDENTIALS = {
    "admin": "password123",
    "doctor": "medcare"
}

def login(username, password):
    username = username.strip()
    password = password.strip()

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return gr.update(visible=True), gr.update(visible=False), ""
    else:
        return gr.update(visible=False), gr.update(visible=True), "Invalid username or password"

# ------------------------ Custom CSS ------------------------

custom_css = """
body {
    background: linear-gradient(to bottom right, #dff9fb, #c7ecee);
    font-family: 'Segoe UI', sans-serif;
}

.main-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    margin: auto;
    width: 80%;
}

.title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    color: #130f40;
    margin-bottom: 10px;
}

.desc {
    font-size: 18px;
    text-align: center;
    color: #535c68;
    margin-bottom: 20px;
}

.btn {
    background-color: #00cec9;
    color: white;
    font-weight: bold;
}

.btn:hover {
    background-color: #0984e3;
}
"""

# ------------------------ Gradio UI ------------------------

with gr.Blocks(css=custom_css) as demo:
    # Inject Lottie Player Script
    gr.HTML("""<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>""")

    # Login Section
    with gr.Column(visible=True) as login_section:
        gr.Markdown("## 🔐 Login to AI Doctor")
        username_input = gr.Textbox(label="👤 Username")
        password_input = gr.Textbox(label="🔑 Password", type="password")
        login_btn = gr.Button("Login", elem_classes="btn")
        login_error = gr.Markdown("", visible=True)

    # AI Doctor Section (hidden by default)
    with gr.Column(visible=False) as app_section:
        gr.Markdown("<div class='title'>🤖🩺 Voice-enabled AI Doctor</div>")
        gr.Markdown("<div class='desc'>Speak your health concern. The AI doctor will understand and respond with care.</div>")
        gr.Audio(value=welcome_audio_path, autoplay=True, visible=False)

        with gr.Row():
            with gr.Column():
                audio_input = gr.Audio(type="filepath", label="🎤 Upload or Record Your Voice")
                language_dropdown = gr.Dropdown(
                    choices=list(language_codes.keys()),
                    value="English",
                    label="🌐 Select Language",
                    filterable=True
                )
                submit_btn = gr.Button("Submit", elem_classes="btn")

            with gr.Column():
                response_text = gr.Textbox(label="🧠 AI Doctor's Response", lines=6)
                audio_output = gr.Audio(label="🔈 Voice Reply")

                gr.HTML("""
                <div style='text-align:center; margin-top:20px;'>
                    <lottie-player src="https://assets2.lottiefiles.com/packages/lf20_kxsd2ytq.json"
                        background="transparent"
                        speed="1"
                        style="width: 200px; height: 200px; margin:auto;"
                        loop
                        autoplay>
                    </lottie-player>
                </div>
                """)

        submit_btn.click(
            fn=process_patient_query,
            inputs=[audio_input, language_dropdown],
            outputs=[response_text, audio_output]
        )

    # Login button logic
    login_btn.click(
        fn=login,
        inputs=[username_input, password_input],
        outputs=[app_section, login_section, login_error]
    )

# ------------------------ Launch App ------------------------

if __name__ == "__main__":
    demo.launch()
