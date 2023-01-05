from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore
from application import db


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

