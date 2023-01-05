import os

# get from environment or use a set key for development
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", default="dev_key")

# Use a mysql server if available
try:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://"
        + os.environ["RDS_USERNAME"]
        + ":"
        + os.environ["RDS_PASSWORD"]
        + "@"
        + os.environ["RDS_HOSTNAME"]
        + "/"
        + os.environ["RDS_DB_NAME"]
    )
# Use development sqlite server
except KeyError:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "db.sqlite3"
    )
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_SALT = SECRET_KEY

# TODO set up mail server
SECURITY_EMAIL_SENDER = "app@mjf106-dt.dbmi.pitt.edu"
# this stops errors on registration if no email server
SECURITY_SEND_REGISTER_EMAIL = False
# MAIL_SERVER = "mjf106-dt.dbmi.pitt.edu"

# TODO remove upload folder for S3 replacement
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads")
