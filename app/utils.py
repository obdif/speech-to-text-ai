import os
from pydub import AudioSegment
import speech_recognition as sr
from docx import Document
import pyttsx3
from django.conf import settings



# AudioSegment.ffmpeg = r"C:\Program Files\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"

def convert_to_wav(audio_file_path):
    """Convert audio file to WAV format using pydub"""
    try:
        audio = AudioSegment.from_file(audio_file_path)
        wav_path = audio_file_path.replace(os.path.splitext(audio_file_path)[1], ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error in convert_to_wav: {e}")
        return None

# Speech to Text function
def speech_to_text(audio_file):
    """Convert speech to text using Google Speech Recognition"""
    try:
        if not audio_file.name.endswith('.wav'):
            audio_file_path = f"temp_{audio_file.name}"
            with open(audio_file_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            wav_file_path = convert_to_wav(audio_file_path)
            if wav_file_path:  
                audio_file_path = wav_file_path  
            else:
                return "Error converting file to WAV"
        else:
            audio_file_path = audio_file

        # Use SpeechRecognition to transcribe the audio
        with sr.AudioFile(audio_file_path) as source:
            recognizer = sr.Recognizer()
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return "Sorry, I couldn't understand the audio."
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            


def text_to_speech(text):
    """Convert text to speech and save as an audio file."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.save_to_file(text, 'output_audio.mp3')  
        engine.runAndWait()
        return 'output_audio.mp3'
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None
    
    

def text_to_doc(text):
    """Convert text to a .docx file and save it in a media directory."""
    try:
        # Define the directory to save the .docx file
        media_path = settings.MEDIA_ROOT  # The base path defined in your settings
        
        # Ensure the media directory exists
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        
        filename = "converted_text.docx"
        file_path = os.path.join(media_path, filename)

        # Create the docx file
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)

        return file_path  # Return the full path to the file
    except Exception as e:
        print(f"Error in text_to_doc: {e}")
        return None