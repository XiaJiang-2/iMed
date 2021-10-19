import numpy as np
from chatbot import chatbot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyttsx3 as tts
import json
import datetime
from tensorflow.keras.models import load_model

application = Flask(__name__)
application.static_folder = 'static'
bootstrap = Bootstrap(application)
class_button_json = json.loads(open('training_data/classes_button.json').read())
list_of_classes = class_button_json['classes_button']
model_15 = load_model('imedbot_model_five_input_15.h5')
@application.route("/")
def index():
    return render_template("index.html")

@application.route("/get")
def get_bot_response():
    #speaker = tts.init()
    #speaker.say("hello")
    result = {}
    button_group = ""
    instruction = ""
    userText = request.args.get('msg')
    response = str(chatbot.get_response(userText))
    result["response"] = response
    print(response)
    # speak(response)
    for item in list_of_classes:
        print(item["responses"])
        if response in item["responses"]:
            print("in")
            button_group = item["patterns"]
            instruction = item["instruction"]
    result["button_group"] = button_group
    result["instruction"] = instruction
    return result

# def speak(response):
#     speaker = tts.init()
#     speaker.setProperty('rate', 150)
#     print(response)
#     speaker.say(response)
#     speaker.startLoop(False)
#     speaker.runAndWait()
#     if speaker._inLoop:
#         speaker.endLoop()
#     print("speak")
# feature_array = ["DCIS_level", "size", "grade","PR_percent","invasive_tumor_Location","distant_recurrence\r"]
@application.route("/getInput")
def get_model_inputdata():
    # only upload 15 year best model
    input = request.args.get('msg')
    input = input.lstrip("[")
    input = input.lstrip("]")
    input = input.split(',')
    input = list(map(int, input))
    if input[0] == 15:
        res = model_15.predict(np.array([input[1:]]))
    else:
        res = "Sorry we only have 15 year model so far"
    return str(res)


if __name__ == "__main__":
    application.run(debug=True)



# from flask import Flask
#
# application = Flask(__name__)
#
#
# @application.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     application.run()
