import speech_recognition as sr
import pyttsx3
import requests


def get_response(prompt):
    # Replace with your actual API endpoint
    url = "http://127.0.0.1:11434/api/generate"
    data = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}
    try:
        # Sending a POST request to the API
        response = requests.post(url, json=data)
        # Checking if the response is successful
        if response.status_code == 200:
            return response.json().get("response", "No response found")
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's recognizer
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, the speech service is unavailable.")
            return ""


def main():
    print("Hello! I’m your voice assistant.")
    speak("Hello! I’m your voice assistant. You can start talking to me.")

    while True:
        # Listen for the user input
        user_text = listen()

        if user_text.lower() == "exit":
            print("Pulse: Goodbye!")
            speak("Goodbye!")
            break
        elif user_text:

            response = get_response(user_text)
            print("Pulse:", response)
            speak(response)


if __name__ == "__main__":
    main()
