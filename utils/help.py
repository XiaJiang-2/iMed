import io
import os
import pandas as pd
from flask import render_template
from application import ResultDownload
from uuid import uuid4
from application import db
import boto3
import sys

BUCKET_NAME = "odpac-data"
sys.path.append("../")

client = boto3.session.Session().client(
    service_name="s3",
    aws_access_key_id='AKIATENOK5FRVOS55G7K',
    aws_secret_access_key='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',
    endpoint_url=os.environ.get("AWS_ENDPOINT", None),
)

BUCKET = os.environ.get("S3_BUCKET", BUCKET_NAME)

def upload_filepath(file_path, uuid=None, text="", score=""):
    """Uploads a file, and returns UUID for later retrieval"""
    print(file_path,'file_path')
    print(uuid,'uuid')
    if uuid is None:
        uuid = uuid4().hex
    if isinstance(file_path, io.BytesIO):
        file_path.seek(0)
        client.upload_fileobj(file_path, BUCKET, uuid)
    else:
        client.upload_file(file_path, BUCKET, uuid)
    db.session.add(
        ResultDownload(uuid=uuid, file_path=uuid, html_table=text, score=score)
    )
    db.session.commit()
    return uuid


def result_text_by_uuid(uuid):
    return ResultDownload.query.filter_by(uuid=uuid).first().html_table


def result_score_by_uuid(uuid):
    return ResultDownload.query.filter_by(uuid=uuid).first().score


def read_result_file_by_uuid(uuid):
    fileobj = io.BytesIO()
    client.download_fileobj(BUCKET, uuid, fileobj)
    fileobj.seek(0)
    return fileobj


def view_data(form):
    form.input_file.data.seek(0)
    # read_csv can read a BytesIO
    data = io.BytesIO()
    form.input_file.data.save(data)
    data.seek(0)
    df = pd.read_csv(data, sep=None, engine="python")
    text = df.to_html()
    return render_template("odpac_blurb.html", text=text, title="Data View")

