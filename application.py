import os
import webbrowser

import numpy as np
from chatbot import chatbot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyttsx3 as tts
import json
import datetime
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename, redirect
from utils import modelTraining

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

@application.route("/dataset",methods=['GET','POST'])
def get_model_dataset():
    if request.method == "POST":
        dataset = request.form.get('dataset')
        name = request.form.get('name')
    print(name)
    # dataset = request.args.get('dataset')
    # name = request.args.get('name')
    upload_path = "dataset/" + str(name)
    dataset = dataset.split('\n')
    validation_auc = train_mode(name)
    with open(upload_path, 'wb') as file:
        for l in dataset:
            file.write(l.strip().encode("utf-8"))
            file.write('\n'.encode("utf-8"))
    return str(validation_auc)
    # if request.method == "POST":
    #     if request.files:
    #         dataset = request.files['dataset']
    #         if str(secure_filename(dataset.filename)) != "":
    #             upload_path = "dataset/" + str(secure_filename(dataset.filename))
    #             dataset.save(upload_path)
    #             dataset_name = str(secure_filename(dataset.filename))

def train_mode(datasetname):
    seed = 123
    nsplits = 5
    scores = "roc_auc"
    filename = os.path.join("dataset/", datasetname)
    if datasetname[-3:] == "txt":
        predset, target = modelTraining.loadandprocess(filename, predtype=1, scaled=False)

    cur_params = {
        'mstruct': [(50, 1)],
        'idim': [31],
        'drate': [0.2],
        'kinit': ['glorot_normal'],
        'iacti': ['relu'],
        'hacti': ['relu'],
        'oacti': ['sigmoid'],
        'opti': ['Adagrad'],
        'lrate': [0.01],
        'momen': [0.4],
        'dec': [0.0005],
        'ls': ['binary_crossentropy'],
        'batch_size': [40],
        'epochs': [85],
        'L1': [0.005],
        'L2': [0.005],
        'ltype': [3]
    }
    results, score_val, score_man = modelTraining.model_gsearch_val(predset, target, cur_params, nsplits, seed, scores)
    return score_val



if __name__ == "__main__":
    application.run(debug=True)



