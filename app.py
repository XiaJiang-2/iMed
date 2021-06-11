import numpy as np
from chatbot import chatbot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyttsx3 as tts
import json
import datetime
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.static_folder = 'static'
bootstrap = Bootstrap(app)
class_button_json = json.loads(open('training_data/classes_button.json').read())
list_of_classes = class_button_json['classes_button']
model_15 = load_model('imedbot_model_five_input_15.h5')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    result = {}
    button_group = ""
    instruction = ""
    userText = request.args.get('msg')
    print(userText)
    print(datetime.datetime.now())
    response = str(chatbot.get_response(userText))
    print(datetime.datetime.now())
    result["response"] = response
    speak(response)

    print(list_of_classes)
    print(response)
    for item in list_of_classes:
        print(item['responses'])
        if response in item["responses"]:
            button_group = item["patterns"]
            instruction = item["instruction"]
    result["button_group"] = button_group
    result["instruction"] = instruction
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
# feature_array = ["DCIS_level", "size", "grade","PR_percent","invasive_tumor_Location","distant_recurrence\r"]
@app.route("/getInput")
def get_model_inputdata():
    input = request.args.get('msg')
    input = input.lstrip("[")
    print(input)
    input = input.lstrip("]")
    print(input)
    input = input.split(',')
    input = list(map(int, input))
    print(input)
    if input[0] == 15:
        print("hello")
        print(input[1:])
        print(np.array(input[1:]))
        res = model_15.predict(np.array([input[1:]]))
        print(res)
    return str(res)


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
