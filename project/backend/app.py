import speech_recognition as sr
import wikipedia
from gtts import gTTS
import pygame
import time
import os

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Dictionary for custom dataset (10 famous monuments)
monuments_info = {
    "Statue of Liberty": "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City, in the United States. It was a gift from France, dedicated on October 28, 1886.",
    "Statue of Unity": "The Statue of Unity is the world's tallest statue of Indian statesman Sardar Vallabhbhai Patel, located in the state of Gujarat, India. It stands 182 meters tall and was inaugurated on 31 October 2018.",
    "Eiffel Tower": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It was constructed from 1887 to 1889 and was named after the engineer Gustave Eiffel, whose company designed and built the tower.",
    "Taj Mahal": "The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in the Indian city of Agra. It was commissioned by Mughal emperor Shah Jahan in memory of his wife Mumtaz Mahal.",
    "Colosseum": "The Colosseum is an ancient amphitheater located in the center of Rome, Italy. It is the largest amphitheater ever built and is considered one of the greatest works of Roman engineering and architecture.",
    "Great Wall of China": "The Great Wall of China is a series of fortifications made of various materials, including stone, brick, tamped earth, and wood, that stretch across northern China. It was built to protect Chinese states from invasions.",
    "Pyramids of Giza": "The Pyramids of Giza are ancient pyramid structures located on the outskirts of Cairo, Egypt. The three main pyramids were built as tombs for the pharaohs of Egypt during the Fourth Dynasty.",
    "Mount Rushmore": "Mount Rushmore is a granite sculpture located in the Black Hills of South Dakota, USA. It features the faces of four U.S. presidents: George Washington, Thomas Jefferson, Theodore Roosevelt, and Abraham Lincoln.",
    "Christ the Redeemer": "Christ the Redeemer is a massive statue of Jesus Christ located in Rio de Janeiro, Brazil. The statue stands 98 feet tall and is an iconic symbol of Christianity in the world.",
    "Big Ben": "Big Ben is the nickname for the Great Bell of the Great Clock of Westminster, located at the north end of the Palace of Westminster in London. The tower is officially known as the Elizabeth Tower."
}

# Initialize the speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Set up for language options
LANGUAGES = {
    "english": "en",
    "hindi": "hi"
}

# Function to recognize speech and process the command
def listen_and_process(language="en"):
    print("Listening...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble with the speech service.")
        return None

# Function to speak text in a given language
def speak_text(text, lang="en"):
    tts = gTTS(text, lang=lang)
    folder_path = r"C:\Users\prath\Desktop\audio_files"  # Specify the path for saving MP3
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = os.path.join(folder_path, "response.mp3")
    tts.save(filename)

    # Play the audio
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Function to fetch information from Wikipedia or custom dataset
def get_information(query, language="en"):
    # First, check in custom dataset
    info = monuments_info.get(query, None)

    if info:
        return info

    # If not found in the custom dataset, try Wikipedia
    try:
        if language == "hi":
            wikipedia.set_lang("hi")
        else:
            wikipedia.set_lang("en")
        info = wikipedia.summary(query, sentences=3)
        return info
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Sorry, I found multiple results. Could you be more specific? {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, I'm having trouble accessing Wikipedia right now."
    except wikipedia.exceptions.RedirectError:
        return "Sorry, the information could not be found."
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"

# Main function to conduct the conversation
def conduct_conversation(language="en"):
    while True:
        print(f"Please ask a question in {language}:")

        user_input = listen_and_process(language)
        if not user_input:
            continue

        if "exit" in user_input.lower():
            print("Exiting...")
            break

        # Fetching information
        if "statue of unity" in user_input.lower():
            info = get_information("Statue of Unity", language)
        elif "statue of liberty" in user_input.lower():
            info = get_information("Statue of Liberty", language)
        elif "taj mahal" in user_input.lower():
            info = get_information("Taj Mahal", language)
        else:
            info = get_information(user_input, language)

        print(f"AI: {info}")

        # Speak the response
        speak_text(info, lang=language)

if __name__ == "__main__":
    print("Welcome to the Voice Assistant and Chatbot!")
    
    # Set the language option (English or Hindi)
    language_choice = input("Choose language (English or Hindi): ").lower()
    language = LANGUAGES.get(language_choice, "en")  # Default to English if invalid input
    
    conduct_conversation(language)
