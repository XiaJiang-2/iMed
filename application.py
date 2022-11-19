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
import shap
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, StratifiedShuffleSplit
import matplotlib.pyplot as plt
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
    usertext = request.args.get('msg')
    response = str(chatbot.get_response(usertext))
    if "can you do" in usertext:
        response = "I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset, or I can train a model for you if you can provide your own dataset, so how do you want to proceed? Please enter 1 for the first choice, or 2 for the second choice"
    result["response"] = response
    for item in list_of_classes:
        print(item["responses"])
        if response in item["responses"]:
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

@application.route("/patientform",methods=['GET','POST'])
def get_model_patientform():

    if request.method == "POST":
        dataset_name = request.form.get('dataset_name')
        shap_check = request.form.get("shap_check")
        print(shap_check)
        dataset_name_str = json.loads(dataset_name)
        print(dataset_name_str)
        filename = os.path.join("dataset/",dataset_name_str)
        predset, target,X_columns = modelTraining.loadandprocess(filename, predtype=1, scaled=False)
        print(X_columns)
        # ['race', 'ethnicity', 'smoking', 'alcohol_useage', 'family_history', 'age_at_diagnosis', 'menopause_status',
        #  'side', 'TNEG', 'ER', 'ER_percent', 'PR', 'PR_percent',
        #  'P53', 'HER2', 't_tnm_stage', 'n_tnm_stage', 'stage', 'lymph_node_removed', 'lymph_node_positive',
        #  'lymph_node_status', 'Histology', 'size', 'grade', 'invasive', 'hi
        #  stology2', 'invasive_tumor_Location', 'DCIS_level', 're_excision', 'surgical_margins', 'MRIs_60_surgery']
        strat_shuf = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=123)
        for CV_index, val_index in strat_shuf.split(predset, target):
            X_CV, X_val = predset[CV_index], predset[val_index]
            Y_CV, Y_val = target[CV_index], target[val_index]

        category_list = []
        patient_dic = request.form.get('patient_dic')
        patient_input_list = json.loads(patient_dic)

        patient_input_list = patient_input_list[:-1]
        print(patient_input_list)
        for item in patient_input_list:
            category_list.append(int(item['value']))
        print(np.array([category_list]))
        #[[2 0 1 1 2 1 1 0 0 1 1 1 1 1 0 1 1 2 1 1 1 1 2 1 1 0 2 3 1 1 1]]
        user_training_model = load_model('user_training_model.h5')

        if shap_check == "true":
            def f(X):
                # return best_model.predict(X).flatten()
                #print("++++++++++++++++++++++++")
                result = []
                for item in X:
                    prob = user_training_model.predict_proba(item.reshape(1,len(predset[0])))
                    # print(prob)
                    # print(prob[0][0])
                    result.append(prob[0][0])
                print(np.array(result))
                # the reason why we have 5 results is because we use kmeans to shrink the x_cv(background dataset) dataset to only 5 samples
                #[0.4565038  0.3262849  0.3953898  0.23958007 0.3785722]

                print(type(result))
                return np.array(result)

            #shap.kmeans(data, K) to summarize the background as K samples, in our case it transfer
            X_train_summary = shap.kmeans(X_CV, 1)
            print(X_train_summary)
            # < shap.utils._legacy.DenseData object at 0x0000024682E412B0 >
            print("111111111111111111111111111111111111111")
            explainer = shap.KernelExplainer(f, X_train_summary)
            print("222222222222222222222222222222222222222")
            shap_values = explainer.shap_values(np.array([category_list]))
            print("333333333333333333333333333333333333333")
            print(shap_values)
            print(explainer.expected_value)
            #shap.waterfall_plot(shap.Explanation(values=shap_values, base_values=explainer.expected_value, data=np.array([category_list]),feature_names=X_columns))
            shap.waterfall_plot(shap.Explanation(values=shap_values[0], base_values=explainer.expected_value, data=np.array([category_list])[0],feature_names=X_columns))
            plt.savefig('static/img/shap/shap.png')

        res = user_training_model.predict_proba(np.array([category_list]))
        res = str(res).replace('[','').replace(']','')
        print(res)
    return res

@application.route("/Examdataset",methods=['GET','POST'])
def get_model_Examdataset():
    if request.method == "POST":
        datasetname = request.form.get('name')
        print("data set name is ",datasetname)
    validation_auc = train_mode(datasetname)
    return str(validation_auc)

@application.route("/dataset",methods=['GET','POST'])
def get_model_dataset():
    if request.method == "POST":
        dataset = request.form.get('dataset')
        datasetname = request.form.get('name')
    upload_path = "dataset/" + str(datasetname)
    dataset = dataset.split('\n')
    with open(upload_path, 'wb') as file:
        print("hello")
        for l in dataset:

            file.write(l.strip().encode("utf-8"))
            file.write('\n'.encode("utf-8"))
    validation_auc = train_mode(datasetname)
    return str(validation_auc)
@application.route("/parameterExam",methods=['GET','POST'])
def get_model_parameter_exam():
    if request.method == "POST":
        datasetname = request.form.get('datasetname')
        learningrate = request.form.get('learningrate')
        batchsize = request.form.get('batchsize')
        epochs = request.form.get('epochs')
        decay = request.form.get('decay')
        dropoutrate = request.form.get('dropoutrate')

    validation_auc = train_mode_parameter(datasetname, learningrate, batchsize, epochs, decay, dropoutrate)
    return str(validation_auc)

@application.route("/parameter",methods=['GET','POST'])
def get_model_parameter():
    if request.method == "POST":
        datasetname = request.form.get('datasetname')
        learningrate = request.form.get('learningrate')
        batchsize = request.form.get('batchsize')
        epochs = request.form.get('epochs')
        decay = request.form.get('decay')
        dropoutrate = request.form.get('dropoutrate')
        dataset = request.form.get('dataset')
    upload_path = "dataset/" + str(datasetname)
    dataset = dataset.split('\n')
    with open(upload_path, 'wb') as file:
        for l in dataset:
            file.write(l.strip().encode("utf-8"))
            file.write('\n'.encode("utf-8"))

    validation_auc = train_mode_parameter(datasetname, learningrate, batchsize, epochs, decay, dropoutrate)
    return str(validation_auc)

def train_mode_parameter(datasetname,learningrate, batchsize, epochs, decay, dropoutrate):
    seed = 123
    nsplits = 5
    scores = "roc_auc"
    filename = os.path.join("dataset/", datasetname)
    if datasetname[-3:] == "txt":
        predset, target,X_columns = modelTraining.loadandprocess(filename, predtype=1, scaled=False)
    elif datasetname[-3:] == "csv":
        predset, target,X_columns = modelTraining.loadandprocess(filename, sep=',', predtype=1, scaled=False)
    cur_params = {
        'mstruct': [(50, 1)],
        'idim': [len(predset[0])],
        'drate': [float(dropoutrate)],
        'kinit': ['glorot_normal'],
        'iacti': ['relu'],
        'hacti': ['relu'],
        'oacti': ['sigmoid'],
        'opti': ['Adagrad'],
        'lrate': [float(learningrate)],
        'momen': [0.4],
        'dec': [float(decay)],
        'ls': ['binary_crossentropy'],
        'batch_size': [int(batchsize)],
        'epochs': [int(epochs)],
        'L1': [0.005],
        'L2': [0.005],
        'ltype': [3]
    }
    results, score_val, score_man = modelTraining.model_gsearch_val(predset, target, cur_params, nsplits, seed, scores)
    return score_val


def train_mode(datasetname):
    seed = 123
    nsplits = 5
    scores = "roc_auc"
    filename = os.path.join("dataset/", datasetname)
    if datasetname[-3:] == "txt":
        predset, target, X_columns = modelTraining.loadandprocess(filename, predtype=1, scaled=False)
    elif datasetname[-3:] == "csv":
        predset, target, X_columns = modelTraining.loadandprocess(filename, sep=',', predtype=1, scaled=False)
    print(target)
    cur_params = {
        'mstruct': [(50, 1)],
        'idim': [len(predset[0])],
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



