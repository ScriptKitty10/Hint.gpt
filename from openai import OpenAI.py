import os
import speech_recognition as sr
import pygame
import uuid
from faster_whisper import WhisperModel
from openai import OpenAI
import time
from elevenlabs import ElevenLabs



client = ElevenLabs(
)


messages_spot=[
    {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the Spot the Difference Puzzle, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hint: There are 3 words.  
          Medium Hint: Watch carefully for room letter.  
          Hard Hint: Number of differences per room creates a distinct word.
          Additional info for you to know: we are going to have 5 different differences within the room and we will provide a hint for each object. 
          When the 3D room is complete, we will let you guys know with the "X" information.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]

messages_blueprint=[
    {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the UV Blueprint Puzzle,
          and only this puzzle.  Your knowledge and hints include: 
          Easy hints: The map holds the key--look closely at them; The X marks something, but it is not always visible.
          Medium Hint: Shine a special light to see where to go; Go to the X and use the special light.
          Hard Hints: Shine a UV light on the map to find the X, that is where you need to go; Use the found numbers to open the lock.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]

messages_password=[
     {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the Christmas Password Game, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hint: The letter "O" is in the middle. (_ _ O _ _)  
          Medium Hint: The letter "Y" is at the end. ( _ _ _ _ Y); The remaining letters are 'C', 'H', 'R', and 'T'.
          Hard Hint: How the Grinch Stole Christmas is a _ _ _ _ _ by Dr. Seuss.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
]

messages_checkers=[
     {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the checkers, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hint: There are 3 words.  
          Medium Hint: Watch carefully for room letter.  
          Hard Hint: Number of differences per room creates a distinct word.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]

messages_clock=[
     {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the Binary and LED Matrix puzzle, guess a number also using a crossword, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hints: use the papers provided; how do computers represent data?
          Medium Hints: Look at the crossword; 1's and 0's 
          Hard Hint: Take a look at the crossword and look for a month and year; Use the binary system to enter in the number (up 1, down 0, right enter, left clear) 
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]

messages_morse=[
     {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the morse puzzle, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hint: How do computers read?.  
          Medium Hint: 0s and 1s.  
          Hard Hint: Binary Syste.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]

messages_amongus=[
     {
        "role": "system",
        "content": '''
        The GPT is a helpful assistant designed to provide hints 
        for people participating in escape rooms. 
        It carefully provides concise, encouraging nudges to help 
        players solve puzzles themselves, without ever directly 
        revealing the answer. The assistant tailors hints based 
        on the user's progress or specific challenges they 
        mention, maintaining a light, fun, and thematic tone.
          It is programmed to assist with the AmongUs wire turn on lights puzzle, 
          and only this puzzle.  Your knowledge and hints include: 
          Easy hints: Among Us; I like to read
          Medium Hint: Look at the bookshelf; Take note of the colors of the books
          Hard Hint: The bookshelf has colored books; Match the colored books with the wires 
          Additional info for you to know: Basically our project involves the wire puzzle from among us except the wires are the same color and the combination is determined from the colored books found on the bookshelf. 
          For example if the top left book is red and the bottom right book is red then the players should connect the top left wire and bottom right wire.
          It can list puzzles if asked and respond 
          to specific inquiries with concise, relevant hints 
          while keeping the experience engaging and immersive. 
          If users ask about unrelated topics or 
          puzzles that don’t exist, it will respond with a 
          relaxed clarification such as, 'Hmm, I’m not sure 
          about that one! Let me know if you’d like help with 
          one of the puzzles here!' to gently redirect them.'''
    }
    
]


messages_police=[
    {
        "role": "system",
        "content": "You are a police, who is responding to a person who is trying to escape an escape room.  You are supposed to give the final code to unlock the door out, only when the escapist tells you the correct password.  Do not tell the code untill they do that.  The password they are supposed to tell you is this phrase: [If I'm alone in this story, make sure the wet bandits never get a chance to steal my pizza that I ordered in november 1990.] The police (you) will then say, 'I am sorry about that situation, we will be coming to help you shortly.  Anyways, The final code is: 9/11'"
    }
]

CONFIG = {
    "spot": {"voice_id": "pqHfZKP75CvOlQylNhV4", "gpt_model": messages_spot},
    "blueprint": {"voice_id": "dfZGXKiIzjizWtJ0NgPy", "gpt_model": messages_blueprint},
     "password": {"voice_id": "kotMqBwiG8fDyRKPYAhp", "gpt_model": messages_password},
    "checkers": {"voice_id": "FF7KdobWPaiR0vkcALHF", "gpt_model": messages_checkers},
     "clock": {"voice_id": "Gqe8GJJLg3haJkTwYj2L", "gpt_model": messages_clock},
    "morse": {"voice_id": "BSu2YLy3De6fuI4uxLRg", "gpt_model": messages_morse},
     "amongus": {"voice_id": "h061KGyOtpLYDxcoi8E3", "gpt_model": messages_amongus},
    "police": {"voice_id": "fCxG8OHm4STbIsWe4aT9", "gpt_model": messages_police}
}


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




def text_to_speech(text, person):
    voice_id = CONFIG[person]["voice_id"]
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2_5",
        text=text
    )

    save_file_path = "output.mp3"
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    
        
    pygame.mixer.init()
    pygame.mixer.music.load(save_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()



def send_to_chatgpt(transcribed_text, person):
    messages = CONFIG[person]["gpt_model"]
    messages.append({"role": "user", "content": transcribed_text})
    
    response = chat_model.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    text = response.choices[0].message.content
    messages.append({"role": "assistant", "content": text})
    print(text)
    return text
 


        
    
def detect():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice input...")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
        print("Voice input detected.  Transcribing...")
        return audio

answer = input("Enter phone number: ")

phone_numbers = {
    "408-534-3829": "spot",
    "925-434-7463": "blueprint",
    "455-368-3489": "password",
    "889-343-4242": "checkers",
    "101-110-1101": "clock",
    "152-858-2222": "morse",
    "123-456-7890": "amongus",
    "911": "police"
}



if answer not in phone_numbers:
    print("Invalid phone number")
    exit()


end_call = ["bye", "bye bye", "see ya", "shut up"]


while True:
        
        person = phone_numbers[answer]

        audio_data = detect()

        text_to_speech("Hello", person)


        transcribed_text = transcribe_with_faster_whisper(audio_data)

        if not transcribed_text:
            text_to_speech("I didn't get that", person)
            continue

        for word in end_call:

            if word in transcribed_text.lower():
                text_to_speech("Bye!", person)
                exit()

        
        response_text = send_to_chatgpt(transcribed_text, person)

        text_to_speech(response_text, person)

        os.remove("output.mp3")

        time.sleep(2)
        
