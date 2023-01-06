from flask import redirect, url_for, render_template, send_file, request
from flask_security import login_required
from tempfile import TemporaryDirectory, TemporaryFile, NamedTemporaryFile
import os
import pandas as pd
import subprocess
import tarfile
import sys
sys.path.append("../")

from utils.forms import (
    MBSForm,
    UserInterventionForm,
    SystemRecommendationForm,
    LearnParentsForm,
    TestPredictionForm,
)
from application import application
from utils.help import (
    view_data,
    upload_filepath,
    result_text_by_uuid,
    read_result_file_by_uuid,
)


def run_mbs(input_data, sep="\t", header_row=True, idx=-1, alpha=9):
    """ Run the MBS.java program"""
    input_dir = TemporaryDirectory(prefix="mbs_")
    output_dir = TemporaryDirectory(prefix="mbs_out_")
    with open(os.path.join(input_dir.name, "MBS.ini"), "w") as f:
        f.write(
            f"""
input_directory_or_file=input.txt
input_mode=0
prefix_indicator=0
input_prefix=200
prefix_start_position=3
input_file_separator={sep}
first_row_col_names={1 if header_row else 0}
output_directory={output_dir.name}
output_file_mode=0
number_of_reported_models_mbs=100
target_index={idx}
alpha={alpha}
type=4
maximum_number_of_edges=4
minimum_number_of_edges=2
"""
        )

    with open(os.path.join(input_dir.name, "input.txt"), "wb") as f:
        f.write(input_data)
    # run jar in the temporary directory
    os.chdir(input_dir.name)
    return_code = subprocess.run(
        ["java", "-jar", os.path.join(application.root_path, "java", "MBS.jar"), "MBS.ini"]
    ).returncode
    # cd back to root
    os.chdir(application.root_path)
    if return_code != 0:
        raise RuntimeError("Error Running Java")

    return output_dir


@application.route("/odpac/learn/mbs/", methods=("GET", "POST"))
def learn_mbs():
    form = MBSForm()
    if form.validate_on_submit():
        input_data = TemporaryFile()
        form.input_file.data.save(input_data)
        input_data.seek(0)  # so we can read the file
        if form.run.data:
            out_dir = run_mbs(
                input_data.read(),
                sep=form.sep.data,
                idx=form.target_index.data,
                alpha=form.alpha.data,
            )
            out_file_tgz = NamedTemporaryFile(prefix="mbs_result_tgz_", delete=False)
            with tarfile.open(out_file_tgz.name, "w:gz") as tar:
                tar.add(out_dir.name, arcname=os.path.basename(out_dir.name))
            df = pd.read_csv(
                os.path.join(out_dir.name, "input_MBSTopModels.csv"), header=None
            )

            # Fix output for web
            for i in range(1, len(df.columns)):
                # move score to the right
                df.loc[df[i].isna(), i] = df[i - 1]
                # delete score on the left (if it was moved)
                df.loc[df[i] == df[i - 1], i - 1] = " "

            df.index.name = "Model Ranking"
            new_col_names = []
            for i in range(0, len(df.columns) - 1):
                new_col_names.append(f"feature_{i}")
            new_col_names.append("Score")
            df.columns = new_col_names
            uuid = upload_filepath(out_file_tgz.name, text=df.to_html())
            return redirect(url_for("learn_mbs_result", uuid=uuid))

        elif form.view_data.data:
            return view_data(form)
        elif form.help_btn.data:
            text = "PLACEHOLDER: help display"
            return render_template("odpac_blurb.html", text=text, title="Placeholder"), 501
        else:
            text = "Bad Request"
            return render_template("odpac_blurb.html", text=text, title="400"), 400

    return render_template("odpac_form.html", heading="MBS.java", form=form)


@application.route("/odpac/learn/mbs/result/<uuid>")
def learn_mbs_result(uuid):
    """result view"""
    table = result_text_by_uuid(uuid)
    text = f"""{table}<div class="text-center my-3"><a href="{url_for('download', uuid=uuid)}" class="btn btn-primary btn-lg mx-auto">Click to Download Results</a></div>"""
    return render_template("odpac_blurb.html", text=text, title="MBS Results")


def run_parents(input_data, sep, target_name, alpha_1, alpha_2, threshold):
    """ Run the java program"""
    output_dir = TemporaryDirectory(prefix="parents_")
    input_dir = TemporaryDirectory(prefix="parents_in_")
    with open(os.path.join(input_dir.name, "TestWeb2.ini"), "w") as f:
        f.write(
            f"""
input_file_path=input.txt
data_column_separator={sep}
output_directory={output_dir.name}
target_name={target_name}
alpha1={alpha_1}
alpha2={alpha_2}
maximum_number_of_edges=7
maximum_single_predictors=20
maximum_set_Length=3
maximum_number_of_interactions_reported=20
threshold={threshold}
skipString=""
"""
        )
    with open(os.path.join(input_dir.name, "input.txt"), "wb") as f:
        f.write(input_data)

    os.chdir(input_dir.name)
    return_code = subprocess.run(
        [
            "java",
            "-jar",
            os.path.join(application.root_path, "java", "TestWeb2.jar"),
            "TestWeb2.ini",
        ]
    ).returncode
    os.chdir(application.root_path)
    if return_code != 0:
        raise RuntimeError("Error Running Java")

    return output_dir


@application.route("/odpac/learn/interactive-parents/", methods=("GET", "POST"))
def learn_interactive_parents():
    form = LearnParentsForm()
    if form.validate_on_submit():
        input_data = TemporaryFile()
        form.input_file.data.save(input_data)
        input_data.seek(0)  # so we can read the file
        if form.run.data:
            out_dir = run_parents(
                input_data.read(),
                form.sep.data,
                form.target_name.data,
                form.alpha_1.data,
                form.alpha_2.data,
                form.is_thresh.data,
            )
            out_file_tgz = NamedTemporaryFile(
                prefix="parents_result_tgz_", delete=False
            )
            # for testing
            out_dir.name = os.path.join(application.root_path, "static", "test-output")
            with tarfile.open(out_file_tgz.name, "w:gz") as tar:
                tar.add(out_dir.name, arcname=os.path.basename(out_dir.name))
            uuid = upload_filepath(out_file_tgz.name)
            return redirect(url_for("learn_interactive_parents_result", uuid=uuid))

        elif form.view_data.data:
            return view_data(form)
        elif form.help_btn.data:
            text = "PLACEHOLDER: help display"
            return render_template("odpac_blurb.html", text=text, title="Placeholder"), 501
        else:
            text = "Bad Request"
            return render_template("odpac_blurb.html", text=text, title="400"), 400

    return render_template(
        "odpac_form.html", heading="Interactive Parents, testweb2.java", form=form
    )


@application.route("/odpac/learn/interactive-parents/result/<uuid>")
def learn_interactive_parents_result(uuid):
    """result view"""
    table = result_text_by_uuid(uuid)
    text = f"""{table}<div class="text-center my-3"><a href="{url_for('download', uuid=uuid)}" class="btn btn-primary btn-lg mx-auto">Click to Download Results</a></div>"""
    return render_template("odpac_blurb.html", text=text, title="Interactive Parents Results")


def run_test_prediction(form):
    """ Run the java program"""
    output_dir = TemporaryDirectory(prefix="testpred_in")
    input_dir = TemporaryDirectory(prefix="testpred_in")
    with open(os.path.join(input_dir.name, "TestWeb3.ini"), "w") as f:
        f.write(
            f"""
output_directory="{output_dir.name}"
race="{form.race.data}"
ethnicity="{form.ethnicity.data}"
smoking="{form.smoking.data}"
alcohol_useage="{form.alcohol_useage.data}"
family_history="{form.family_history.data}"
age_at_diagnosis="{form.age_at_diagnosis.data}"
menopause_status="{form.menopause_status.data}"
side="{form.side.data}"
TNEG="{form.TNEG.data}"
ER="{form.ER.data}"
ER_percent="{form.ER_percent.data}"
PR="{form.PR.data}"
PR_percent="{form.PR_percent.data}"
P53="{form.P53.data}"
HER2="{form.HER2.data}"
t_tnm_stage="{form.t_tnm_stage.data}"
n_tnm_stage="{form.n_tnm_stage.data}"
stage="{form.stage.data}"
lymph_node_removed="{form.lymph_node_removed.data}"
lymph_node_positive="{form.lymph_node_positive.data}"
lymph_node_status="{form.lymph_node_status.data}"
Histology="{form.Histology.data}"
size="{form.size.data}"
grade="{form.grade.data}"
invasive="{form.invasive.data}"
histology2="{form.histology2.data}"
invasive_tumor_Location="{form.invasive_tumor_Location.data}"
DCIS_level="{form.DCIS_level.data}"
re_excision="{form.re_excision.data}"
surgical_margins="{form.surgical_margins.data}"
MRIs_60_surgery="{form.MRIs_60_surgery.data}"
"""
        )

    os.chdir(input_dir.name)
    java = subprocess.run(
        [
            "java",
            "-jar",
            os.path.join(application.root_path, "java", "TestWeb3.jar"),
            "TestWeb3.ini",
        ],
        capture_output=True,
    )

    return_code = java.returncode
    os.chdir(application.root_path)
    if return_code != 0:
        raise RuntimeError("Error Running Java")

    output_text = str(java.stdout, "utf-8")
    with open(NamedTemporaryFile(prefix="testpred_", delete=False).name, "w") as tmp:
        tmp.write(output_text)
        output_file = tmp.name

    uuid = upload_filepath(output_file)
    return output_text, uuid


@application.route("/odpac/test-prediction", methods=("GET", "POST"))
def test_prediction():
    form = TestPredictionForm()

    if request.method == "POST":
        output, uuid = run_test_prediction(form)
        output = output
        return render_template(
            "odpac_form-treatment.html",
            heading="Test Prediction Form template",
            form=form,
            output=output,
            uuid=uuid,
        )
    return render_treatment_form(
        0, form, "Test Prediction Form template", treatment=False
    )


def run_treatment(
    option,
    tneg,
    grade,
    p53,
    er,
    node_status,
    menopause,
    her2,
    nodal_radi,
    antihormone,
    breast_chest_radi,
    chemo,
    her2_inhib,
    neo,
):
    """ Run the java program"""
    output_dir = TemporaryDirectory(prefix="treatment_")
    input_dir = TemporaryDirectory(prefix="treatment_in_")
    with open(os.path.join(input_dir.name, "TestWeb1.ini"), "w") as f:
        f.write(
            f"""
output_directory={output_dir.name}
TNEG={tneg}
Grade={grade}
p53={p53}
ER={er}
Node_status={node_status}
Menopause={menopause}
HER2={her2}
Nodal_radi={nodal_radi}
Antihormone={antihormone}
Breast_chest_radi={breast_chest_radi}
Chemo={chemo}
Her2_Inhib={her2_inhib}
Neo={neo}
option={option}
"""
        )

    os.chdir(input_dir.name)
    return_code = subprocess.run(
        [
            "java",
            "-jar",
            os.path.join(application.root_path, "java", "TestWeb1.jar"),
            "TestWeb1.ini",
        ]
    ).returncode
    os.chdir(application.root_path)
    if return_code != 0:
        raise RuntimeError("Error Running Java")

    output_file = os.listdir(output_dir.name)[0]
    output_file = os.path.abspath(os.path.join(output_dir.name, output_file))
    with open(output_file) as f:
        output_text = f.read()
        with open(
            NamedTemporaryFile(prefix="treatment_", delete=False).name, "w"
        ) as tmp:
            tmp.write(output_text)
            output_file = tmp.name

    uuid = upload_filepath(output_file)
    return output_text, uuid


@application.route("/odpac/treatment/download/<uuid>")
def treatment_download(uuid):
    """download from the download table"""
    return send_file(
        read_result_file_by_uuid(uuid),
        mimetype="text/plain",
        attachment_filename="result.txt",
        as_attachment=True,
    )


@application.route("/odpac/treatment-interaction", methods=["GET", "POST"])
@login_required
def treatment_interaction():
    return render_template("odpac_treatment.html")


@application.route("/odpac/treatment-interaction/system-recommendation", methods=["GET", "POST"])
@login_required
def treatment_recommendation():
    form = SystemRecommendationForm()
    output = False

    heading = "Treatment Recommendation"
    if request.method == "POST":
        return render_treatment_form(1, form, heading)
    return render_template(
        "odpac_form-treatment.html", heading=heading, form=form, output=output
    )


@application.route("/odpac/treatment-interaction/user-intervention", methods=["GET", "POST"])
@login_required
def treatment_user_intervention():
    form = UserInterventionForm()
    output = False

    heading = "User Intervention"
    if request.method == "POST":
        return render_treatment_form(2, form, heading)
    return render_template(
        "odpac_form-treatment.html", heading=heading, form=form, output=output
    )


def render_treatment_form(option, form, heading, treatment=True):
    output = False
    uuid = False
    if treatment:
        output = False
        tneg = form.tneg.data
        grade = form.grade.data
        p53 = form.p53.data
        er = form.er.data
        node_status = form.node_status.data
        menopause = form.menopause.data
        her2 = form.her2.data
        nodal_radi = None
        antihormone = None
        breast_chest_radi = None
        chemo = None
        her2_inhib = None
        neo = None
        if option == 2:
            nodal_radi = form.nodal_radi.data
            antihormone = form.antihormone.data
            breast_chest_radi = form.breast_chest_radi.data
            chemo = form.chemo.data
            her2_inhib = form.her2_inhib.data
            neo = form.neo.data

        output, uuid = run_treatment(
            option,
            tneg,
            grade,
            p53,
            er,
            node_status,
            menopause,
            her2,
            nodal_radi,
            antihormone,
            breast_chest_radi,
            chemo,
            her2_inhib,
            neo,
        )
    return render_template(
        "odpac_form-treatment.html", heading=heading, form=form, output=output, uuid=uuid
    )


