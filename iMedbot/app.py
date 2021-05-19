from chatbot import chatbot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyttsx3 as tts

app = Flask(__name__)
app.static_folder = 'static'
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(chatbot.get_response(userText))
    speak(response)
    return response

def speak(response):
    speaker = tts.init()
    speaker.setProperty('rate', 150)
    speaker.say(response)
    #speaker.startLoop(False)
    speaker.runAndWait()
    if speaker._inLoop:
        speaker.endLoop()
    print("speak")



if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
