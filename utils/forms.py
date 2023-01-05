import pandas as pd
import io
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    StringField,
    FloatField,
    FileField,
    SelectField,
    IntegerField,
    SubmitField,
    RadioField,
    BooleanField,
)
from wtforms.validators import NumberRange, Length, Optional, InputRequired
from wtforms.widgets import TextArea
from flask_wtf.file import FileAllowed


class RunFormHead(FlaskForm):
    input_file = FileField(
        'Input Data&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
    )
    sep = SelectField(
        'Data Column Separator&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[("\\t", "Tab"), (" ", "Space"), (",", "Comma")],
        default="\\t",
       # validators=[Required()],
    )
    target_index = IntegerField(
        'Target Class Index&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
       # validators=[Required()],
        default=-1,
    )


class RunFormTail(FlaskForm):
    show_folds = BooleanField("Show Individual Folds", default=True)
    help_btn = SubmitField("Help")
    view_data = SubmitField("Data View")
    run = SubmitField("Run")


class RunForm(RunFormHead, RunFormTail):
    def __init__(self, *args, **kwargs):
        top_fields = [f for f in self._unbound_fields if f[0] in dir(RunFormHead)]
        bottom_fields = [f for f in self._unbound_fields if f[0] in dir(RunFormTail)]
        new_fields = list(
            set(self._unbound_fields) - set(top_fields) - set(bottom_fields)
        )
        self._unbound_fields = top_fields + new_fields + bottom_fields
        super().__init__(*args, **kwargs)


class MBSForm(RunForm):
    alpha = FloatField(
        'Alpha&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=0),], #Required()],
        default=9,
    )


class LearnParentsForm(FlaskForm):
    input_file = FileField(
        'Input Data&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
    )
    sep = SelectField(
        'Data Column Separator&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[("\\t", "Tab"), (" ", "Space"), (",", "Comma")],
        default="\\t",
       # validators=[Required()],
    )
    target_name = StringField(
        'Target Class Name &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
    )
    alpha_1 = FloatField(
        'Alpha 1 &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=1, max=1000)], #Required()],
        default=1,
    )
    alpha_2 = FloatField(
        'Alpha 2 &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=1, max=1000)], #Required()],
        default=1,
    )
    is_thresh = FloatField(
        'IS Threshold &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=0, max=1)], #Required()],
        default=1,
    )

    show_folds = BooleanField("Show Individual Folds", default=True)
    help_btn = SubmitField("Help")
    view_data = SubmitField("View Input")
    run = SubmitField("Run")


class TestPredictionForm(FlaskForm):
    race = SelectField(
        'race &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "WHITE"),
            (1, "BLACK"),
            (2, "ASIAN"),
            (3, "American Indian or Alaskan Native"),
        ],
       # validators=[Required()],
    )

    ethnicity = SelectField(
        'ethnicity &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "Not Hispanic"), (1, "Hispanic")],
      #  validators=[Required()],
    )

    smoking = SelectField(
        'smoking &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "NON SMOKER"),
            (1, "EX SMOKER"),
            (2, "CIGARETTES"),
            (3, "CHEWING TOBACCO"),
            (4, "CIGAR"),
        ],
      #  validators=[Required()],
    )

    alcohol_useage = SelectField(
        'alcohol_useage &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, '"ALCOHOL USE, NOS"'),
            (1, "MODERATE ALCOHOL USE"),
            (2, "NO ALCOHOL USE"),
            (3, "FORMER ALCOHOL USE"),
        ],
      #  validators=[Required()],
    )

    family_history = SelectField(
        'family_history &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "FAMILY HISTORY OF THIS & OTHER CANCER"),
            (1, '"FAMILY HISTORY OF CANCER , NOS"'),
            (2, "FAMILY HISTORY OF OTHER CANCER"),
            (3, "NO FAMILY HISTORY OF CANCER"),
            (4, "FAMILY HISTORY OF THIS CANCER"),
        ],
       # validators=[Required()],
    )

    age_at_diagnosis = SelectField(
        'age_at_diagnosis &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "3"), (1, "2"), (2, "1")],
      #  validators=[Required()],
    )

    menopause_status = SelectField(
        'menopause_status &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "post"), (1, "pre")],
      #  validators=[Required()],
    )

    side = SelectField(
        'side &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "left"), (1, "right")],
      #  validators=[Required()],
    )

    TNEG = SelectField(
        'TNEG &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "NO"), (1, "YES")],
      #  validators=[Required()],
    )

    ER = SelectField(
        'ER &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "POSITIVE"), (1, "NEGATIVE"), (2, "LOWPOSITIVE")],
      #  validators=[Required()],
    )

    ER_percent = SelectField(
        'ER_percent &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "90 - 100"), (1, "0 - 20"), (2, "20 - 90")],
      #  validators=[Required()],
    )

    PR = SelectField(
        'PR &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "POSITIVE"), (1, "NEGATIVE"), (2, "LOWPOSITIVE")],
      #  validators=[Required()],
    )

    PR_percent = SelectField(
        'PR_percent &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "20 - 90"), (1, "0 - 20"), (2, "90 - 100")],
      #  validators=[Required()],
    )

    P53 = SelectField(
        'P53 &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "NEGATIVE"), (1, "POSITIVE"), (2, "LOWPOSITIVE")],
      #  validators=[Required()],
    )

    HER2 = SelectField(
        'HER2 &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "NEGATIVE"), (1, "POSITIVE")],
      #  validators=[Required()],
    )

    t_tnm_stage = SelectField(
        't_tnm_stage &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "1"),
            (1, "3"),
            (2, "2"),
            (3, "4"),
            (4, "X"),
            (5, "IS"),
            (6, "0"),
            (7, "1mic"),
        ],
      #  validators=[Required()],
    )

    n_tnm_stage = SelectField(
        'n_tnm_stage &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "0"), (1, "2"), (2, "1"), (3, "X"), (4, "3")],
       # validators=[Required()],
    )

    stage = SelectField(
        'stage &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "1"), (1, "3"), (2, "2"), (3, "0")],
       # validators=[Required()],
    )

    lymph_node_removed = SelectField(
        'lymph_node_removed &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "1"), (1, "3"), (2, "2")],
      #  validators=[Required()],
    )

    lymph_node_positive = SelectField(
        'lymph_node_positive &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "0"), (1, "2"), (2, "1")],
      #  validators=[Required()],
    )

    lymph_node_status = SelectField(
        'lymph_node_status &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "NEGATIVE"), (1, "POSITIVE")],
      #  validators=[Required()],
    )

    Histology = SelectField(
        'Histology &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "LOBULAR"), (1, "DUCT"), (2, "MIXED DUCT AND LOBULAR")],
      #  validators=[Required()],
    )

    size = SelectField(
        'size &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "2"), (1, "1"), (2, "3")],
      #  validators=[Required()],
    )

    grade = SelectField(
        'grade &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "1"), (1, "2"), (2, "3")],
      #  validators=[Required()],
    )

    invasive = SelectField(
        'invasive &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "YES"), (1, "NO")],
     #   validators=[Required()],
    )

    histology2 = SelectField(
        'histology2 &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "ILO"), (1, "IDC"), (2, "DCIS"), (3, "NC")],
      #  validators=[Required()],
    )

    invasive_tumor_Location = SelectField(
        'invasive_tumor_Location &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "LOBULAR"),
            (1, "DUCT"),
            (2, "MIXED DUCT AND LOBULAR"),
            (3, "NONE"),
        ],
      #  validators=[Required()],
    )

    DCIS_level = SelectField(
        'DCIS_level &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "SOLID"),
            (1, "NOT PRESENT"),
            (2, "COMEDO"),
            (3, "CRIBRIFORM"),
            (4, "APOCRINE"),
            (5, "DCIS"),
            (6, "PAPILLARY"),
            (7, "MICROPAPILLALRY"),
            (8, "MICROPAPILLARY"),
        ],
       # validators=[Required()],
    )

    re_excision = SelectField(
        're_excision &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "0"), (1, "1")],
       # validators=[Required()],
    )

    surgical_margins = SelectField(
        'surgical_margins &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[
            (0, "NO RESIDUAL TUMOR"),
            (1, "NO PRIMARY SITE SURGERY"),
            (2, "MICROSCOPIC RESIDUAL TUMOR"),
            (3, '"RESIDUAL TUMOR, NOS"'),
            (4, "MARGINS NOT EVALUABLE"),
        ],
       # validators=[Required()],
    )

    MRIs_60_surgery = SelectField(
        'MRIs_60_surgery &nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[(0, "0"), (1, "1")],
      #  validators=[Required()],
    )

    show_folds = BooleanField("Show Individual Folds", default=True)
    help_btn = SubmitField("Help")
    predict = SubmitField("Predict")


class LogRegForm(RunForm):
    solver = SelectField(
        label='Solver&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        choices=[(s, s) for s in ["newton-cg", "lbfgs", "liblinear", "sag", "saga"]],
        default="liblinear",
    )
    max_iter = IntegerField(
        'Max Number of Iterations&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[ NumberRange(min=1)], #Required(),
        default=100,
    )
    C = FloatField(
        'Inverse of Regularization Strength&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        default=1.0,
    )
    intercept_scaling = FloatField(
        'Alpha&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        default=1.0,
    )


class LassoForm(RunForm):
    alpha = FloatField(
        'Alpha&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        default=1.0,
    )
    tol = FloatField(
        'Tolerance for Optimization&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        default=0.0001,
    )

    max_iter = IntegerField(
        'Max Number of Iterations&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=1)], #Required(),
        default=1000,
    )


class SVMForm(RunForm):
    C = FloatField(
        'Alpha&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
       # validators=[Required()],
        default=1.0,
    )
    kernel = SelectField(
        label='kernel&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
       # validators=[Required()],
        choices=[(k, k) for k in ["linear", "poly", "rbf", "sigmoid"]],
        default="rbf",
    )
    gamma = StringField(
        'Gamma (Number value or "auto")&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
       # validators=[Required()],
        default="auto",
    )
    tol = FloatField(
        'Tolerance for Stopping Criterion&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
      #  validators=[Required()],
        default=0.001,
    )
    max_iter = IntegerField(
        'Max Number of Iterations (or -1 For No Limit)&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[NumberRange(min=-1)], #Required(),
        default=-1,
    )

    def validate_gamma(form, field):
        try:
            field.data = float(field.data)
        except BaseException:
            if field.data not in ["auto", "scale"]:
                raise ValidationError("Invalid Gamma")


class NBForm(RunForm):
    def __init__(self, *args, **kwargs):
        print(self._unbound_fields)
        super().__init__(*args, **kwargs)

    whichnb = SelectField(
        "Variation",
        choices=[(c, c) for c in ("BernoulliNB", "ComplementNB", "MultinomialNB")],
        default="BernoulliNB",
       # validators=[Required()],
    )

    alpha = FloatField(
        'Alpha&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
       # validators=[Required()],
        default=1.0,
    )


class KNNForm(RunForm):
    n_neighbors = IntegerField(
        'Number of Neighbors&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[ NumberRange(min=1)], #Required(),
        default=3,
    )


class DTForm(RunForm):
    splitter = SelectField(
        "Splitter",
        choices=[("best", "best"), ("random", "random")],
        default="best",
       # validators=[Required()],
    )
    min_samples_split = FloatField(
        "Min Samples Split", validators=[InputRequired()], default=2
    )
    min_samples_leaf = FloatField(
        "Min Samples Leaf",
        #validators=[Required()],
        default=1
    )
    min_weight_fraction_leaf = FloatField(
        "Min Weight Fraction Leaf",
        validators=[InputRequired()],
        default=0
    )
    min_impurity_split = FloatField(
        'Min Impurity Split&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[InputRequired()],
        default=1e-7,
    )


class RFForm(RunForm):
    criterion = SelectField(
        'Criterion&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        choices=[("gini", "gini"), ("entropy", "entropy")],
        default="gini",
        #validators=[Required()],
    )
    min_samples_split = FloatField(
        'Min Samples Split&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[InputRequired()],
        default=2,
    )
    min_samples_leaf = FloatField(
        'Min Samples Leaf&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        #validators=[Required()],
        default=1,
    )
    min_weight_fraction_leaf = FloatField(
        'Min Weight Fraction Leaf&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[InputRequired()],
        default=0,
    )
    min_impurity_split = FloatField(
        'Min Impurity Split&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[InputRequired()],
        default=1e-7,
    )


class ABForm(RunForm):
    learning_rate = FloatField(
        'Learning Rate&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>',
        validators=[InputRequired()],
        default=1.0,
    )


class VoteForm(RunForm):
    """Form for the voting Ensemble classifier, combining
    all of the other classifiers with default values."""


def PredictForm(*features):
    class F(FlaskForm):
        pass

    for name in features:
        setattr(F, f"feature_{name}", FloatField(str(name)))
    F.run = SubmitField("Predict")
    return F()


class PredictFileForm(FlaskForm):
    def __init__(self, length):
        super().__init__()
        self.length = length

    input_data = FileField("Upload Dataset",
                           #validators=[Required()]
                           )
    get_auc = BooleanField(
        'Get ROC AUC&nbsp;<span class="w3tooltip">🛈<span class="w3tooltiptext">Tooltip text</span></span>'
    )
    run = SubmitField("Predict")

    def validate_input_data(form, field):
        input_data = io.BytesIO()
        field.data.save(input_data)
        input_data.seek(0)  # so we can read the file
        if form.get_auc.data:
            form.length += 1
        try:
            df = pd.read_csv(input_data, sep=None)
        except BaseException:
            raise ValidationError("Cannot Read Data")
        if len(df.columns) != form.length:
            raise ValidationError(
                f"Input data has wrong number of columns. Expected {form.length}, got {len(df.columns)}"
            )
        else:
            form.df = df


class DataForm(FlaskForm):
    name = StringField("Dataset Name", validators=[Length(min=3, max=255)]) #Required(),
    provider = StringField("Provider", validators=[ Length(min=3, max=255)]) #Required(),
    curator = StringField("Curator", validators=[Length(min=3, max=255)]) #Required(),
    original_publication = StringField(
        "Original Publication", validators=[Optional(), Length(min=3, max=255)]
    )
    data_restrict = RadioField(
        label="Data Use Restriction",
        #validators=[Required()],
        choices=[("Yes", "Yes"), ("No", "No")],
        default="No",
    )
    restriction = StringField("Restriction", widget=TextArea())
    input_data = FileField("Upload Dataset", )#validators=[Required()])
    input_description = FileField(
        "Upload Description Document",
        validators=[FileAllowed(["pdf"], message="Must be a pdf")], #Required()
    )
    submit = SubmitField("Upload")


# Treatment Interaction Forms
class Option_1:
    tneg = SelectField(
        label="TNEG",
        #validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    grade = SelectField(
        label="Grade",
        #validators=[Required()],
        choices=[(1, "One"), (2, "Two"), (3, "Three")],
        default=1,
    )
    p53 = SelectField(
        label="P53",
        #validators=[Required()],
        choices=[("pos", "Positive"), ("neg", "Negative")],
        default="neg",
    )
    er = SelectField(
        label="ER",
        #validators=[Required()],
        choices=[("pos", "Positive"), ("neg", "Negative")],
        default="neg",
    )
    node_status = SelectField(
        label="node_status",
       # validators=[Required()],
        choices=[("pos", "Positive"), ("neg", "Negative")],
        default="neg",
    )
    menopause = SelectField(
        label="Menopause",
       # validators=[Required()],
        choices=[("pre", "Pre"), ("post", "Post")],
        default="pre",
    )
    her2 = SelectField(
        label="HER2",
       # validators=[Required()],
        choices=[("pos", "Positive"), ("neg", "Negative")],
        default="neg",
    )


class Option_2:
    nodal_radi = SelectField(
        label="Nodal Radi",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    antihormone = SelectField(
        label="Antihormone",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    breast_chest_radi = SelectField(
        label="Breast_chest_radi",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    chemo = SelectField(
        label="Chemo",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    her2_inhib = SelectField(
        label="Her2_inhib",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )
    neo = SelectField(
        label="Neo",
       # validators=[Required()],
        choices=[("yes", "Yes"), ("no", "No")],
        default="yes",
    )


class SystemRecommendationForm(Option_1, FlaskForm):
    proceed = SubmitField("Proceed")


class UserInterventionForm(Option_1, Option_2, FlaskForm):
    proceed = SubmitField("Proceed")
