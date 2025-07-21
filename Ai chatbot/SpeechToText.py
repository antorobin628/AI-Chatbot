# speech.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import time


# Load language from .env
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# HTML code for voice recognition
HtmlCode = f'''
<!DOCTYPE html>
<html lang="en">
<head><title>Speech Recognition</title></head>
<body>
    <button onclick="startRecognition()">Start</button>
    <p id="output"></p>
    <script>
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!window.SpeechRecognition) {{
            document.title = "SpeechRecognition not supported";
        }} else {{
            let recognition;
            function startRecognition() {{
                recognition = new SpeechRecognition();
                recognition.lang = "{InputLanguage}";
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.onresult = function(event) {{
                    let transcript = event.results[0][0].transcript;
                    document.getElementById("output").innerText = transcript;
                    document.title = transcript;
                }};

                recognition.onerror = function(event) {{
                    document.title = "Recognition error: " + event.error;
                }};

                recognition.onnomatch = function(event) {{
                    document.title = "No match found";
                }};

                recognition.start();
            }}
        }}
    </script>
</body>
</html>
'''

# Save HTML to Data/Voice.html
voice_file = "Data/Voice.html"
os.makedirs("Data", exist_ok=True)
with open(voice_file, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")  # Required for Chrome 109+
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Main function to extract speech
def get_speech_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Request failed: {e}"

# Test independently
if __name__ == "__main__":
    print("Speak now...")
    print("Result:", get_speech_text())
