import os
import webbrowser

import numpy as np
from flask import Flask,render_template, request, url_for, redirect, send_file, flash
from flask_bootstrap import Bootstrap
import json
import datetime
from werkzeug.utils import secure_filename, redirect
import shap
import matplotlib.pyplot as plt
import joblib

from utils.retrieve_columns import expand_parameters_stored_in_one_column,sort_data_based_on_target_columns
from utils.retrieve_columns import read_file,retrieve_target_columns_based_on_values
from utils.retrieve_columns import find_columns_to_be_expanded, find_available_filters
from utils.merge_file import merge
from collections import defaultdict

import plotly
import plotly.express as px

application = Flask(__name__)

@application.route("/")
def index_imed():
    """
    index page
    """
    return render_template("index_imed.html")

@application.route("/imedbot")
def imedbot():
    """
    go to imedbot application
    """
    return redirect(url_for("http://imedbot.odpac.net/"))

@application.route('/data_analytics/download/<path:data_path>')
def download(data_path):
    """
    download the data
    """
    print('data_pathhhhhhhhh',data_path)
    return send_file("../"+data_path, as_attachment=True)

@application.route('/data_analytics/upload_dataset/<flag>', methods =['POST','GET'])
def upload_dataset(flag):
    """
    there are two ways to upload  dataset, one is from the local computer, and the other  is from the application
    """
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
        if int(flag) == 1: #retrieve subsets
            print(data.columns,'dddddddd')
            return render_template('retrieve_subsets.html',data_path=data_path,data=data.head(10),heads=data.columns)
        if int(flag) == 2: #plot trend
            return redirect(url_for('plot_trend',data_path=data_path))
        return render_template('upload_dataset.html',flag=0, data=data.head(10), heads=data.columns, data_path = data_path, files = files)

    return render_template('upload_dataset.html', flag=flag,data=None, files=files)

@application.route('/data_analytics/retrieve_subsets/<path:data_path>',methods=['POST','GET'])
def retrieve_subsets(data_path):
    """
    this function returns to  themain retireve subsets page
    """
    data = read_file(data_path)
    if request.method =='POST':
        pass
    return render_template('retrieve_subsets.html',data=data.head(10),data_path=data_path,heads=data.columns)

@application.route('/data_analytics/expand_data/<path:data_path>', methods=['POST','GET'])
def expand_data(data_path):
    """
    this function aims to check which column needs to be expanded, and then return an expanded dataset
    """
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

@application.route('/data_analytics/return_sorted_results/<path:data_path>', methods=['POST','GET'])
def return_sorted_results(data_path):
    """
    this function aims to return sorted results
    """
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


@application.route('/data_analytics/retrieve_columns/<path:data_path>/', methods = ['POST','GET'])
def retrieve_columns(data_path):
    """
    this function aims to list diversity_columns and continuous_columns separately
    """
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

@application.route("/data_analytics/upload_multiple_dataset",methods=['GET','POST'])
def upload_multiple_dataset():
    """
    this function aims to merge files which share the same format
    """
    file_dir = "dataset/"
    files = os.listdir(file_dir)
    if request.method=='POST':
        files = request.files.getlist("datasets")
        # Iterate for each file in the files List, and Save them
        filenames = []
        for file in files:
            print(file.filename)
            data_path = 'dataset/' + secure_filename(file.filename)
            file.save(data_path)
            filenames.append(data_path)
            print('ddddddddd',data_path)
        if len(filenames)!=0:
            filenames = ",".join(map(str,filenames))
            print(filenames)
            return redirect(url_for('merge_file',filenames=filenames))
    return render_template("upload_multiple_dataset.html",data=None)

@application.route("/data_analytics/merge_file/<path:filenames>",methods=['POST','GET'])
def merge_file(filenames):
    """
    this function aims to merge files which share the same format
    """
    print('ffffffffffffffffffffffffffffffff',filenames)
    filenames=filenames.split(',')
    print('ffff',filenames)
    output_path = 'dataset/'+secure_filename('merge_file.csv')
    keep_index = False
    merge(filenames, keep_index, output_path)
    data =  read_file(output_path).head(10)
    print(data)
    return render_template('merge_file.html',filenames=filenames,data_path =output_path,data=data,heads = data.columns )

@application.route("/data_analytics/trend_plot/<path:data_path>",methods=['POST','GET'])
def plot_trend(data_path):
    """
    this function aims to plot trend figures
    """
    print(data_path)
    df = read_file(data_path)
    columns = df.columns
    graph1JSON = None
    if request.method == "POST":
        x_label = request.form.get("x_label", None)
        y_label = request.form.get("y_label", None)
        title = "Dataset: " + str(data_path)
        if x_label and y_label:
            fig1 = px.scatter(x=df[x_label], y=df[y_label], title=title,
                labels=dict(x=x_label, y=y_label))
            graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    if graph1JSON:
        print('success to get figure')
        return render_template('trend.html', graph1JSON=graph1JSON,columns = columns,data_path=data_path)
    return render_template('trend.html',columns = columns,data_path=data_path)
if __name__ == "__main__":

    application.static_folder = 'static'
    application.secret_key = 'super secret key'
    application.config['SESSION_TYPE'] = 'filesystem'
    application.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
    application.run(debug=True)
