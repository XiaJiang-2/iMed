import os
import webbrowser

import numpy as np
from chatbot import chatbot
from flask import Flask,render_template, request, url_for, redirect, send_file, flash
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
import joblib

from utils.retrieve_columns import expand_parameters_stored_in_one_column,sort_data_based_on_target_columns
from utils.retrieve_columns import read_file,retrieve_target_columns_based_on_values
from utils.retrieve_columns import find_columns_to_be_expanded, find_available_filters
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict


application = Flask(__name__)
application.static_folder = 'static'
bootstrap = Bootstrap(application)
class_button_json = json.loads(open('training_data/classes_button.json').read())
list_of_classes = class_button_json['classes_button']
model_15 = load_model('imedbot_model_five_input_15.h5')
model_10 = load_model('model10.h5')
model_5 = load_model('model5.h5')


@application.route("/")
def index_imed():
    return render_template("index_imed.html")

@application.route("/imedbot")
def imedbot():
    return render_template("imedbot.html")

@application.route('/download/<path:data_path>')
def download(data_path):
    return send_file("../"+data_path, as_attachment=True)

@application.route('/upload_dataset/<flag>', methods =['POST','GET'])
def upload_dataset(flag):
    file_dir = "dataset/"
    files = os.listdir(file_dir)
    data, data_path, head = None, None, None
    if request.method == "POST":
        if request.files:
            f = request.files['dataset']
            if str(secure_filename(f.filename)) != "":
                data_path = 'dataset/' + secure_filename(f.filename)
                f.save(data_path)
                print('file uploaded successfully')
                dataset_name= f.filename
                data = read_file(data_path)
            if not data_path:
                flash("please upload a dataset in suitable format('.csv .xlsx .txt')")
                return render_template('upload_dataset.html',flag=0,data=None, files=files)
            else:
                file_size = os.path.getsize(data_path)
                if file_size >= 500000000:
                    flash(f"the maximum file size limit is 500M! Your file is {file_size/1024/1024}M! Please upload another dataset")
                    return render_template('upload_dataset.html',flag=0,data=None, files=files)
        else:
            print('existing dataset')
            dataset_name = request.form.get("dataset_name", None)
            data_path = 'dataset/' + str(dataset_name)

            if not dataset_name:
                flash("the dataset you chose is not in a suitable format('.csv .xlsx .txt')")
                return render_template('upload_dataset.html',flag=0,data=None, files=files)
            else:
                data = read_file(data_path)
                file_size = os.path.getsize(data_path)
                if file_size >= 300000000:
                    flash(
                        f"the maximum file size limit is 500M! Your file is {file_size / 1000000}M! Please upload another dataset")
                    return render_template('upload_dataset.html', flag=0,data=None, files=files)
        if int(flag) == 1:
            print(data.columns,'dddddddd')
            return render_template('retrieve_subsets.html',data_path=data_path,data=data.head(10),heads=data.columns)
        return render_template('upload_dataset.html',flag=0, data=data.head(10), heads=data.columns, data_path = data_path, files = files)

    return render_template('upload_dataset.html', flag=0,data=None, files=files)
@application.route('/retrieve_subsets/<path:data_path>',methods=['POST','GET'])
def retrieve_subsets(data_path):
    data = read_file(data_path)
    if request.method =='POST':
        pass
    return render_template('retrieve_subsets.html',data=data.head(10),data_path=data_path,heads=data.columns)
@application.route('/expand_data/<path:data_path>', methods=['POST','GET'])
def expand_data(data_path):
    data = read_file(data_path)
    try:
        candidate_columns = find_columns_to_be_expanded(data)
        if not candidate_columns:
            flash("the dataset doesn't need to be expanded!")
            return render_template('retrieve_subsets.html', data=data.head(10),data_path=data_path,heads=data.columns)
        if request.method == 'POST':
            check_columns = request.form.getlist('checkbox', None)
            if check_columns:
                new_df, sub_parameters = expand_parameters_stored_in_one_column(data_path, check_columns)
                data_path_expand = data_path[:-4] +'_expand'+data_path[-4:]
                new_df.to_csv(data_path_expand,index=False)
                print(new_df.head(3))
                heads = new_df.columns
                return render_template('expand_data.html', new_data=new_df.head(10), data_path = data_path_expand, heads = heads,sub_parameters=sub_parameters)
    except:
        flash("please recheck your dataset")
        return render_template('retrieve_subsets.html', data=data.head(10),data_path=data_path, heads=data.columns)
    return render_template('expand_data.html',data_path=data_path, candidate_columns=candidate_columns, new_data = None)

@application.route('/return_sorted_results/<path:data_path>', methods=['POST','GET'])
def return_sorted_results(data_path):
    data = read_file(data_path)
    ready_to_return=False
    try:
        if find_columns_to_be_expanded(data):
             flash("the dataset you chose has sub-parameters, please go to expand the dataset first!")
             return render_template('retrieve_subsets.html',data_path=data_path,data=data,heads=data.columns)
        print(data.head())
        #find continuous columns
        continuous_columns = find_available_filters(data_path)[1]
        if request.method=='POST':
            target_columns = request.form.getlist('choose_target_column')
            ascending = request.form.get('ascending')
            return_columns = request.form.getlist('check_return_columns', None)  # return columns
            if return_columns: ready_to_return = True
            if ready_to_return:
                unique=False
                expand=False
                k=10
                output_path = data_path[:-4] + f'_sort@{k}' + data_path[-4:]
                ascending = True if ascending=='ascending' else False
                new_df=sort_data_based_on_target_columns(data_path, target_columns, expand, unique, output_path, ascending, k)
                print('sort succesfully!')
                new_df = new_df[return_columns]
                print(new_df.head())
                new_df.to_csv(output_path,index=False)
                return render_template('retrieve_subsets.html',data_path=output_path,data=new_df.head(10),heads=new_df.columns)
    except Exception:
        flash("please recheck your dataset!")
        return render_template('retrieve_subsets.html', data=data.head(10), data_path=data_path)
    return render_template('return_sorted_results.html',continuous_columns=continuous_columns,all_columns=data.columns)



# @application.route('/show_table/<path:data_path>/',methods=['POST','GET'])
# def show_table(data_path):
#     data = read_file(data_path)
#     print(data.head())

@application.route('/retrieve_columns/<path:data_path>/', methods = ['POST','GET'])
def retrieve_columns(data_path):
    data = read_file(data_path)
    try:
        # if find_columns_to_be_expanded(data):
        #     flash("the dataset you chose has sub-parameters, please go to expand the dataset first!")
        #     return render_template('retrieve_subsets.html',data_path=data_path,data=data)
        print(data.head())
        diversity_columns, continuous_columns = find_available_filters(data_path)
        print('continuous_columns',continuous_columns)
        diversity_filters, continuous_filters = {}, defaultdict(list)
        retrieved = False
        if request.method == 'POST':
            #diversity_filters = request.form.getlist('diversity_filters')
            for column in diversity_columns:
                if request.form.get(f"diversity_filters_{column}"):
                    retrieved = True
                    diversity_filters[column] = request.form.getlist(f"diversity_filters_{column}", None)
                    if 'any' in diversity_filters[column]:
                        del diversity_filters[column]
            for column in continuous_columns:
                if request.form.get(f"continuous_filters_minimum_{column}"):
                    retrieved = True
                    continuous_filters[column].append(float(request.form.get(f"continuous_filters_minimum_{column}")))
                    continuous_filters[column].append(float(request.form.get(f"continuous_filters_maximum_{column}")))
            #print(diversity_filters,'diversity_filters')
            #print(continuous_filters,'continuous_filters')
            return_columns = request.form.getlist('check_return_columns', None)  # return columns
            print('all',return_columns)
            if return_columns: retrieved = True
            if retrieved:
                output_path = data_path[:-4] +'_retrieve'+data_path[-4:]
                unique = False
                expand = False
                new_df = retrieve_target_columns_based_on_values(data_path, requirements=diversity_filters, range_requirements=continuous_filters,
                                                        target_columns=return_columns,output_path=output_path, unique=unique, expand=expand)
                print(new_df.head())
                print('retrieve succesfully!')
                return render_template('retrieve_subsets.html',data_path=output_path,data=new_df.head(10),heads=new_df.columns)

    except:
        flash("Please recheck your dataset's format")
        return render_template('retrieve_subsets.html', data=data.head(10), data_path=data_path)
    return render_template('retrieve_columns.html',data_path = data_path, data = data.head(10),df_length=len(data),
                           all_columns = data.columns, i = 0,
                           diversity_columns = diversity_columns, continuous_columns=continuous_columns, new_df = None)

@application.route("/get")
def get_bot_response():
    # speaker = tts.init()
    # speaker.say("hello")
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
    # due to different discrete to digital map,
    # transformation need according .txt in ../docs/informationprovidedfordevelopment/

    if input[0] == 15:
        res = model_15.predict(np.array([input[1:]]))
    elif input[0] == 10:
        dcis = input[1]
        size = input[2]
        grade = input[3]
        pr_percent = input[4]
        location = input[5]

        model_input = [0 for i in range(18)]
        model_input[2] = pr_percent
        model_input[9] = dcis
        model_input[12] = grade

        res = model_10.predict(np.array([model_input]))
    elif input[0] == 5:
        dcis = input[1]
        size = input[2]
        grade = input[3]
        pr_percent = input[4]
        location = input[5]

        model_input = [0 for i in range(20)]
        model_input[8] = pr_percent
        model_input[16] = size
        model_input[17] = location
        model_input[18] = dcis
        res = model_5.predict(np.array([model_input]))
    else:
        res = "Sorry we only have 15 year model so far"
    return str(res)


@application.route("/getTestPatient")
def get_test_patient_list():
    year = request.args.get('msg')
    if int(year) == 5:
        with open('dataset/LSM-5Year-I-240.txt') as f:
            contents = f.readlines()
    if int(year) == 10:
        with open('dataset/LSM-10Year-I-240.txt') as f:
            contents = f.readlines()
    if int(year) == 15:
        with open('dataset/LSM-15Year-I-240.txt') as f:
            contents = f.readlines()
    print(year)
    for i in range(len(contents)):
        contents[i] = contents[i].split()
    labellist = contents[0]
    res = {}
    print(len(labellist), len(contents))
    for i in range(len(labellist)):
        res[str(i)] = []
        for j in range(1, len(contents)):
            if contents[j][i] not in res[str(i)]:
                res[str(i)].append(contents[j][i])
    print(res)
    return {"labellist": labellist, "tableresult": res}


@application.route("/submitsurvey", methods=['POST','GET'])
def get_user_survey():
    if request.method == "POST":
        star = request.args.get('radio')
        text = request.args.get('text')
        print(star, text)

    return "success"


@application.route("/patientform", methods=['GET', 'POST'])
def get_model_patientform():
    if request.method == "POST":
        dataset_name = request.form.get('dataset_name')
        shap_check = request.form.get("shap_check")
        print(shap_check)
        print("dataset_name ", dataset_name)
        dataset_name_str = json.loads(dataset_name)
        print(dataset_name_str)
        filename = os.path.join("dataset/", dataset_name_str)
        predset, target, X_columns = modelTraining.loadandprocess(filename, predtype=1, scaled=False)
        print("147", X_columns)
        print("148", predset[0])
        print("149", target[0])
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
        print("168", np.array([category_list]))
        # [[2 0 1 1 2 1 1 0 0 1 1 1 1 1 0 1 1 2 1 1 1 1 2 1 1 0 2 3 1 1 1]]
        user_training_model = load_model('user_training_model.h5')

        if shap_check == "true":
            def f(X):
                # return best_model.predict(X).flatten()
                # print("++++++++++++++++++++++++")
                result = []
                for item in X:
                    prob = user_training_model.predict_proba(item.reshape(1, len(predset[0])))
                    # print(prob)
                    # print(prob[0][0])
                    result.append(prob[0][0])
                print(np.array(result))
                # the reason why we have 5 results is because we use kmeans to shrink the x_cv(background dataset) dataset to only 5 samples
                # [0.4565038  0.3262849  0.3953898  0.23958007 0.3785722]

                print(type(result))
                return np.array(result)

            # shap.kmeans(data, K) to summarize the background as K samples, in our case it transfer
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
            # shap.waterfall_plot(shap.Explanation(values=shap_values, base_values=explainer.expected_value, data=np.array([category_list]),feature_names=X_columns))
            shap.waterfall_plot(shap.Explanation(values=shap_values[0], base_values=explainer.expected_value,
                                                 data=np.array([category_list])[0], feature_names=X_columns))
            plt.savefig('static/img/shap/shap.png')

        res = user_training_model.predict_proba(np.array([category_list]))
        res = str(res).replace('[', '').replace(']', '')
        print(res)
    return res


@application.route("/Examdataset", methods=['GET', 'POST'])
def get_model_Examdataset():
    if request.method == "POST":
        datasetname = request.form.get('name')
        print("data set name is ", datasetname)
    validation_auc = train_mode(datasetname)
    return str(validation_auc)


@application.route("/dataset", methods=['GET', 'POST'])
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


@application.route("/parameterExam", methods=['GET', 'POST'])
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


@application.route("/parameter", methods=['GET', 'POST'])
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


def train_mode_parameter(datasetname, learningrate, batchsize, epochs, decay, dropoutrate):
    seed = 123
    nsplits = 5
    scores = "roc_auc"
    filename = os.path.join("dataset/", datasetname)
    if datasetname[-3:] == "txt":
        predset, target, X_columns = modelTraining.loadandprocess(filename, predtype=1, scaled=False)
    elif datasetname[-3:] == "csv":
        predset, target, X_columns = modelTraining.loadandprocess(filename, sep=',', predtype=1, scaled=False)
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


