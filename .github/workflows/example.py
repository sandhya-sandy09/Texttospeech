from flask import Flask, request, render_template, Response, send_file
from gtts import gTTS
from langdetect import detect
import io

app = Flask(__name__)

def text_to_speech(text):
    # Detect the language
    language = detect(text)
    print(f"Detected language: {language}")
    
    # Use gTTS to convert text to speech
    tts = gTTS(text=text, lang=language)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    
    # Convert the text to speech and get the audio stream
    audio_fp = text_to_speech(text)
    
    # Return the audio stream as a response
    return Response(audio_fp, mimetype="audio/mp3")

@app.route('/download', methods=['POST'])
def download():
    text = request.form['text']
    
    # Convert the text to speech and get the audio stream
    audio_fp = text_to_speech(text)
    
    # Save the audio to a temporary file
    with open("output.mp3", "wb") as f:
        f.write(audio_fp.read())
    
    # Send the file to the user
    return send_file("output.mp3", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
