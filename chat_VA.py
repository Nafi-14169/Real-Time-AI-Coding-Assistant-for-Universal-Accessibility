import speech_recognition as sr
import pyautogui
import pyttsx3
import re

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 0.9)

def respond(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for code...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout — no speech detected.")
            return None

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return None

def convert_to_code(text):
    """Convert natural speech into Python code syntax."""

    # Replace some common spoken patterns
    text = re.sub(r"define function (\w+) with parameters (.+)", r"def \1(\2):", text)
    text = re.sub(r"return (.+)", r"return \1", text)
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("divided by", "/")
    text = text.replace("equal to", "==")
    text = text.replace("greater than", ">")
    text = text.replace("less than", "<")
    text = text.replace("comma", ",")

    return text

def main():
    respond("Code assistant ready. Say 'start coding' to begin.")
    activated = False

    while True:
        command = listen_for_command()
        if not command:
            continue

        if "start coding" in command:
            activated = True
            respond("Coding mode activated. Speak your code.")
            continue

        if "stop coding" in command:
            respond("Exiting coding mode.")
            break

        if activated:
            code_line = convert_to_code(command)
            respond(f"Typing: {code_line}")
            pyautogui.typewrite(code_line + "\n", interval=0.05)
        else:
            print("Say 'start coding' to activate code mode.")

if __name__ == "__main__":
    main()
