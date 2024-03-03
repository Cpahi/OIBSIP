import tkinter as tk
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
from cryptography.fernet import Fernet
import spacy

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_sm")

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Encrypt sensitive data (email credentials)
def encrypt_credentials(email, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(email.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_email, encrypted_password

# Decrypt sensitive data (email credentials)
def decrypt_credentials(encrypted_email, encrypted_password):
    key = b''  # Your encryption key
    cipher_suite = Fernet(key)
    email = cipher_suite.decrypt(encrypted_email).decode()
    password = cipher_suite.decrypt(encrypted_password).decode()
    return email, password

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("User said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

# Function to send email
def send_email(recipient, subject, body, encrypted_email, encrypted_password):
    decrypted_email, decrypted_password = decrypt_credentials(encrypted_email, encrypted_password)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(decrypted_email, decrypted_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(decrypted_email, recipient, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email at the moment.")

# Function to execute custom commands
def execute_custom_command(command):
    webbrowser.open(f"https://www.google.com/search?q={command}")

# Function to process user command using NLP
def process_command(command):
    doc = nlp(command)
    for token in doc:
        if token.pos_ == 'VERB':
            if token.text == 'send':
                return 'send_email'
    return None

# Function to start the voice assistant
def start_voice_assistant():
    speak(greet() + " How can I assist you today?")
    while True:
        command = listen()

        if command:
            action = process_command(command)
            if action == 'send_email':
                speak("Who is the recipient?")
                recipient = listen()
                speak("What is the subject?")
                subject = listen()
                speak("What should I say?")
                body = listen()
                send_email(recipient, subject, body, encrypted_email, encrypted_password)
            elif 'exit' in command:
                speak("Exiting Voice Assistant.")
                break
            else:
                execute_custom_command(command)

# Function to display the user guide
def display_user_guide():
    guide_text = """
    User Manual: Voice Assistant

Welcome to the Voice Assistant user manual. This document will guide you through the process of using the voice assistant effectively for performing various tasks using voice commands.

1. Getting Started:

Make sure you have Python installed on your system. You can download and install Python from the official website: Python.org.
Install the required Python libraries: speech_recognition, pyttsx3, spacy.
You can install these libraries using the following pip commands:
Copy code
pip install SpeechRecognition
pip install pyttsx3
pip install spacy
Download and install the English language model for spaCy by running:
Copy code
python -m spacy download en_core_web_sm
Set up a Gmail account if you want to use the email feature of the voice assistant.
2. Using the Voice Assistant:

Launch the Voice Assistant application by running the provided Python script.
You will be presented with a graphical user interface (GUI) containing several buttons:
Start Voice Assistant: Click this button to activate the voice assistant and start giving voice commands.
User Guide: This button provides information on how to use the voice assistant effectively.
About: Click this button to learn more about the voice assistant and its development.
Exit: Click this button to exit the Voice Assistant application.
To activate the voice assistant, click the "Start Voice Assistant" button. The assistant will greet you and wait for your voice commands.
Speak clearly and command the assistant to perform various tasks. You can use commands such as:
"Send an email" to compose and send an email to a recipient.
Any search query to perform a Google search. The assistant will open the browser and display search results.
You can also interact with the assistant to perform custom actions or open specific websites.
3. User Guide:

The User Guide provides detailed instructions on how to use the voice assistant effectively. It covers the following topics:

The capabilities of the voice assistant, including sending emails and performing Google searches.
Instructions for speaking commands clearly and effectively to ensure accurate recognition.
Recommendations for installing required libraries and setting up a Gmail account for email functionality.
4. About:

The About section provides information about the voice assistant, including:

Background information on the development of the assistant.
Acknowledgment that the assistant uses Google for searching queries.
Contact information for inquiries or feedback about the assistant.
5. Exiting the Application:

To exit the Voice Assistant application, simply click the "Exit" button on the GUI.
    """

    user_guide_window = tk.Toplevel(root)
    user_guide_window.title("User Guide")
    user_guide_text = tk.Text(user_guide_window, wrap=tk.WORD)
    user_guide_text.insert(tk.END, guide_text)
    user_guide_text.pack()

# Function to display information about the assistant
def display_about():
    about_text = """
    About:
    Hi my name is Hardik Tiwari and this is my custom built voice assistant
    This voice assistant was built as part of my internship project.
    It is capable of performing various tasks using voice commands.
    This assistant uses Google for searching queries.
    For any inquiries or feedback, please contact me on my Github or issue a pull request.
    """

    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_text_widget = tk.Text(about_window, wrap=tk.WORD)
    about_text_widget.insert(tk.END, about_text)
    about_text_widget.pack()

# Function to greet user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    return greeting

# Main function
if __name__ == "__main__":
    # Encrypt email credentials
    email = 'your_email@gmail.com'
    password = 'your_password'
    encrypted_email, encrypted_password = encrypt_credentials(email, password)

    # Create the GUI
    root = tk.Tk()
    root.title("Voice Assistant Menu")

    label = tk.Label(root, text="Welcome to the Voice Assistant Menu")
    label.pack(pady=10)

    start_button = tk.Button(root, text="Start Voice Assistant", command=start_voice_assistant)
    start_button.pack(pady=5)

    user_guide_button = tk.Button(root, text="User Guide", command=display_user_guide)
    user_guide_button.pack(pady=5)

    about_button = tk.Button(root, text="About", command=display_about)
    about_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=5)

    root.mainloop()