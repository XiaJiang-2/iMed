#speech to text
import speech_recognition
# text to speech
import pyttsx3 as tts

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate',150)

#speaker.say("Hello")
speaker.runAndWait()
try:
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=0.5)
        audio = recognizer.listen(mic)

        text = recognizer.recognize_google(audio_data=audio)
        text = text.lower()
        print(text)

except speech_recognition.UnknownValueError:
    recognizer = speech_recognition.Recognizer()

