import numpy as np
import pyaudio
import wave
import os
import speech_recognition as sr
import pygame
from gtts import gTTS
import pyttsx3
import boto3
from faster_whisper import WhisperModel
from openai import OpenAI
import time





chat_model = OpenAI(api_key="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")

def transcribe_with_faster_whisper(audio_data):

    model = WhisperModel("tiny", device="cpu", compute_type="float32")

    with open("temp.wav", "wb") as temp_file:
        temp_file.write(audio_data.get_wav_data())


    segments, info = model.transcribe(
        "temp.wav", 
        beam_size=5, 
        word_timestamps=True
    )

    transcribed_text = " ".join([segment.text for segment in segments])

    print("Transcription complete.")
    print(f"Transcribed text: {transcribed_text}")
    os.remove("temp.wav")
    return transcribed_text

def send_to_chatgpt(transcribed_text):
    """
    Send transcribed text to ChatGPT and get a response.
    """
    response = chat_model.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": transcribed_text}]
    )

    text = response.choices[0].message.content

    print(text)

    return text

def text_to_speech(text, filename="output.mp3"):

    tts = gTTS(text=text, lang='en')
    tts.save(filename)


    
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    
def detect_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice input...")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
        print("Voice input detected.  Transcribing...")
        return audio

answer = input("Enter phone number: ")

# phone_numbers = ["925-293-2932", "408-938-4938", "408-765-2331"]

phone_numbers = ["1"]


if answer in phone_numbers:
    print("Calling")

    while True:

        audio_data = detect_and_transcribe()


        transcribed_text = transcribe_with_faster_whisper(audio_data)

        response_text = send_to_chatgpt(transcribed_text)

        text_to_speech(response_text)

        os.remove("output.mp3")

        time.sleep(2)
        