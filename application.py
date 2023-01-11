import os
import webbrowser
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from flask import Flask,render_template, request, url_for, redirect, send_file, flash,abort
from flask_mail import Mail
from flask_security import Security, login_required
from uuid import uuid4
from utils.forms import DataForm
from io import BytesIO
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

from sklearn.metrics import roc_curve, auc

application = Flask(__name__)
application.config.from_object("config")
db = SQLAlchemy(application)
bootstrap = Bootstrap(application)
application.static_folder = 'static'
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'
application.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

from functools import wraps
"""
models
"""
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore
class ResultDownload(db.Model):
    # uuid is always 32 chars
    uuid = db.Column(db.String(32), primary_key=True, unique=True)
    # 260 is possible max file path for windows
    file_path = db.Column(db.String(260), unique=True)
    html_table = db.Column(db.String(21844))
    score = db.Column(db.String(10))
    created = db.Column(db.DateTime(), default=db.func.current_timestamp())

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    submitted_treatment_form = db.Column(db.Boolean(), default=False)
    tneg = db.Column(db.Boolean())
    grade = db.Column(db.Integer())
    p53 = db.Column(db.Boolean())
    er = db.Column(db.Boolean())
    node_status = db.Column(db.Boolean())
    menopause = db.Column(db.Boolean())
    her2 = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class DataSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(255))
    provider = db.Column(db.String(255))
    curator = db.Column(db.String(255))
    original_publication = db.Column(db.String(255))
    dataset_file = db.Column(db.String(260))
    description_file = db.Column(db.String(260))
    data_restriction = db.Column(db.Boolean())
    restriction_text = db.Column(db.String(1000))
    uploaded_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    records = db.Column(db.Integer)
    features = db.Column(db.Integer)


security = Security(application, user_datastore)
mail = Mail()
mail.init_app(application)

with application.app_context():
    db.init_app(application)
    db.create_all()

import sys
sys.path.append("../")



#import prediction, java_prediction  # NOQA



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
        elif int(flag) == 2: #plot trend
            return redirect(url_for('plot_trend',data_path=data_path))
        elif int(flag)==3: #plot roc curve
            return redirect(url_for('plot_roc_curve',data_path=data_path))
        elif int(flag)==4: #box plot
            return redirect(url_for('plot_box',data_path=data_path))
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
    try:
        if request.method == "POST":
            x_label = request.form.get("x_label", None)
            y_label = request.form.get("y_label", None)
            type = request.form.get("type", None)
            title = "Dataset: " + str(data_path)
            if x_label and y_label and type:
                if type == 'scatter':
                    fig1 = px.scatter(x=df[x_label], y=df[y_label], title=title+"-scatter",
                        labels=dict(x=x_label, y=y_label))
                elif type == 'line':
                    fig1 = px.line(x=df[x_label], y=df[y_label], title=title + "-line",
                                      labels=dict(x=x_label, y=y_label))
                graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        if graph1JSON:
            print('success to get figure')
            return render_template('trend.html', graph1JSON=graph1JSON,columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    except:
        flash("Please choose X, Y and type")
        return render_template('trend.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    return render_template('trend.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))

@application.route("/data_analytics/plot_roc_curve/<path:data_path>",methods=['POST','GET'])
def plot_roc_curve(data_path):
    """
    this function aims to plot trend figures
    """
    print(data_path)
    df = read_file(data_path)
    columns = df.columns
    graph1JSON = None
    try:
        if request.method == "POST":
            predicted_column = request.form.get("predicted_values", None)
            true_column = request.form.get("true_values", None)
            title = "Dataset: " + str(data_path) + 'roc_curve'
            if predicted_column and true_column:
                pred_values = np.asarray(df[predicted_column])
                true_values = np.asarray(df[true_column])
                print(pred_values)
                print('1111111111')
                print(true_values)
                fpr, tpr, thresholds = roc_curve(true_values.astype(float),pred_values.astype(float))
                fig = px.area(
                    x=fpr, y=tpr,
                    title=title + f'ROC Curve (AUC={auc(fpr, tpr):.4f})',
                    labels=dict(x='False Positive Rate', y='True Positive Rate'),
                    width=700, height=500
                )
                fig.add_shape(
                    type='line', line=dict(dash='dash'),
                    x0=0, x1=1, y0=0, y1=1
                )

                fig.update_yaxes(scaleanchor="x", scaleratio=1)
                fig.update_xaxes(constrain='domain')
                graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        if graph1JSON:
            print('success to get figure')
            return render_template('roc_curve.html', graph1JSON=graph1JSON,columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    except:
        flash("Please choose true values and predicted values")
        flash("Please make sure the true values are binary labels")
        return render_template('roc_curve.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    return render_template('roc_curve.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))

@application.route("/data_analytics/plot_box/<path:data_path>",methods=['POST','GET'])
def plot_box(data_path):
    """
    this function aims to plot trend figures
    """
    print(data_path)
    df = read_file(data_path)
    columns = df.columns
    graph1JSON = None
    try:
        if request.method == "POST":
            x_label = request.form.get("x_label", None)
            y_label = request.form.get("y_label", None)
            color = request.form.get('color',None)
            print(x_label,y_label)
            title = "Dataset: " + str(data_path) + '-box'
            if x_label and y_label:
                fig = px.box(df, x=x_label, y=y_label, color=color,title=title,
                               labels=dict(x=x_label, y=y_label))
                fig.update_traces(quartilemethod="exclusive")
                graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        if graph1JSON:
            print('success to get figure')
            return render_template('box.html', graph1JSON=graph1JSON,columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    except:
        flash("Please choose true values and predicted values")
        flash("Please make sure the true values are binary labels")
        return render_template('box.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))
    return render_template('box.html',columns = columns,data_path=data_path,heads=columns,data=df.head(10))
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

"""
project of ODPAC
"""
@application.route("/odpac")
@application.route("/odpac/learn/")
def learn():
    """Renders the front page."""
    return render_template("odpac_learn.html")

@application.route("/odpac/learn/interaction/")
def learn_interaction():
    return render_template("odpac_learn-interaction.html")

#change the name of function(from download to odpac_download)
@application.route("/odpac/learn/download/<uuid>/")
def odpac_download(uuid):
    """download from the download table"""
    return send_file(
        read_result_file_by_uuid(uuid),
        mimetype="application/octet-stream",
        download_name="result.tar.gz",
        as_attachment=True,
    )

@application.route("/odpac/datasets/available")
@login_required
def datasets_avail():
    records = DataSet.query.all()
    return render_template("odpac_data.html", records=records, title="Datasets")

def get_records(fname):
    df = pd.read_csv(fname, sep=None, engine="python", header=0)
    return len(df)

def get_features(fname):
    df = pd.read_csv(fname, sep=None, engine="python", header=0)
    return len(df.columns)

@application.route("/odpac/datasets/share/", methods=("GET", "POST"))
def datasets_share():
    form = DataForm()
    if form.validate_on_submit():
        data_path = BytesIO()
        form.input_data.data.save(data_path)
        desc_path = BytesIO()
        form.input_description.data.save(desc_path)
        dataset_uuid = upload_filepath(data_path)
        desc_uuid = upload_filepath(desc_path)
        db.session.add(
            DataSet(
                uuid=uuid4().hex,
                name=form.name.data,
                provider=form.provider.data,
                curator=form.curator.data,
                original_publication=form.original_publication.data,
                dataset_file=dataset_uuid,
                description_file=desc_uuid,
                data_restriction=True if form.data_restrict.data == "Yes" else False,
                restriction_text=form.restriction.data,
                records=get_records(read_result_file_by_uuid(dataset_uuid)),
                features=get_features(read_result_file_by_uuid(dataset_uuid)),
            )
        )
        db.session.commit()
        return render_template(
            "odpac_blurb.html", text="Successfully uploaded dataset", title="Success"
        )

    return render_template("odpac_form.html", heading="Upload Dataset", form=form)

@application.route("/odpac/datasets/info/<uuid>/")
@login_required
def dataset_info(uuid):
    record = DataSet.query.filter_by(uuid=uuid).first()
    return render_template(
        "odpac_data_info.html",
        title=record.name,
        data=url_for("download_data", uuid=uuid, t="data"),
        pdf=url_for("download_data", uuid=uuid, t="desc", display="display"),
        pdf_down=url_for("download_data", uuid=uuid, t="desc"),
    )

@application.route("/odpac/datasets/download/<t>/<uuid>/")
@application.route("/odpac/datasets/download/<t>/<uuid>/<display>/")
@login_required
def download_data(t, uuid, display=False):
    if t not in ("data", "desc"):
        abort(404)
    if display == "display":
        display = True
    record = DataSet.query.filter_by(uuid=uuid).first()
    dl_file = (
        read_result_file_by_uuid(record.description_file)
        if t == "desc"
        else read_result_file_by_uuid(record.dataset_file)
    )
    return send_file(
        dl_file,
        mimetype="text/plain" if t == "data" else "application/pdf",
        download_name=f"{record.name}-{t}.{'csv' if t == 'data' else 'pdf'}",
        as_attachment=not display,
    )

@application.route("/odpac/about/us/")
def about_us():
    return (
        render_template(
            "odpac_blurb.html", text="PLACEHOLDER: About us", title="Placeholder"
        ),
        501,
    )

@application.route("/odpac/about/research/")
def about_research():
    return (
        render_template(
            "odpac_blurb.html",
            text="PLACEHOLDER: About relevant research",
            title="Placeholder",
        ),
        501,
    )

from utils.java_prediction import *
from utils.prediction import *

if __name__ == "__main__":
    application.run(debug=True)

