from chatbot import chatbot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyttsx3 as tts
import json
import datetime

app = Flask(__name__)
app.static_folder = 'static'
bootstrap = Bootstrap(app)
class_button_json = json.loads(open('training_data/classes_button.json').read())
list_of_classes = class_button_json['classes_button']
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    result = {}
    button_group = ""
    userText = request.args.get('msg')
    print(userText)
    print(datetime.datetime.now())
    response = str(chatbot.get_response(userText))
    print(datetime.datetime.now())
    result["response"] = response
    speak(response)

    print(list_of_classes)
    for item in list_of_classes:
        if response in item["responses"]:
            button_group = item["patterns"]
    result["button_group"] = button_group
    return result

def speak(response):
    speaker = tts.init()
    speaker.setProperty('rate', 150)
    speaker.say(response)
    #speaker.startLoop(False)
    speaker.runAndWait()
    if speaker._inLoop:
        speaker.endLoop()
    print("speak")

@app.route("/getInput")
def get_model_inputdata():
    input = request.args.get('msg')
    print("hello")
    print(input)
    data = 'happy'
    return data


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
