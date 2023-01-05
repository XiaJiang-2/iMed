from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from tempfile import NamedTemporaryFile
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from flask import url_for, redirect, render_template, send_file, abort
import sys
sys.path.append("../")

from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    VotingClassifier,
)
from utils.forms import (
    LogRegForm,
    PredictForm,
    LassoForm,
    PredictFileForm,
    SVMForm,
    NBForm,
    KNNForm,
    DTForm,
    RFForm,
    ABForm,
    VoteForm,
)
import io
import pandas as pd
import pickle
from application import application
from utils.help import (
    view_data,
    upload_filepath,
    read_result_file_by_uuid,
    result_score_by_uuid,
)


@application.route("/odpac/learn/prediction")
def learn_prediction_model():
    return render_template("odpac_learn-prediction.html")


def check_valid_model(model):
    if model not in MODEL_LIST.keys():
        abort(404)


def get_train_score(clf, X, y, show_folds=True):
    """ inspired by https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html"""

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    cv = StratifiedKFold(n_splits=5)
    aucs = []
    entire_test = pd.DataFrame()
    entire_proba = pd.DataFrame()
    clf.fit(X, y)
    for k, X_y_split in enumerate(cv.split(X, y)):
        train, test = X_y_split
        clf.fit(X.iloc[train], y.iloc[train])
        probas_ = clf.predict_proba(X.iloc[test])
        fpr, tpr, thresholds = roc_curve(y.iloc[test], probas_[:, 1])
        entire_test = pd.concat([entire_test, pd.DataFrame(y.iloc[test])])
        entire_proba = pd.concat([entire_proba, pd.DataFrame(probas_[:, 1])])
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        if show_folds:
            ax.plot(
                fpr, tpr, lw=1, label=f"Fold - {k+1} - AUC {roc_auc:.4f}", alpha=0.9
            )

    fpr, tpr, thresholds = roc_curve(entire_test, entire_proba)
    roc_auc = auc(fpr, tpr)
    ax.plot(
        fpr, tpr, lw=1, label=f"Entire Data- AUC {roc_auc:.4f}", color="b", alpha=0.9
    )

    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic")
    ax.legend(loc="lower right")
    img = NamedTemporaryFile(prefix=f"roc_plot_", delete=False)
    canvas.print_png(img.name)
    uuid = upload_filepath(img.name)
    return sum(aucs) / 5, uuid, clf


@application.route("/odpac/download/<uuid>")
def download_plot(uuid):
    return send_file(
        read_result_file_by_uuid(uuid),
        mimetype="image/png",
        attachment_filename="plot.png",
        as_attachment=False,
    )


MODEL_LIST = {
    "logreg": "Logistic Regression",
    "lasso": "Lasso",
    "nb": "Naive Bayes",
    "svm": "SVM",
    "knn": "K Nearest Neighbor",
    "decision_trees": "Decision Trees",
    "random_forest": "Random Forest",
    "adaboost": "AdaBoost",
    "voting": "Ensemble Voting Classifier",
}


@application.route("/odpac/learn/prediction/<model>", methods=("GET", "POST"))
def model_train(model):
    check_valid_model(model)
    forms = {
        "logreg": LogRegForm,
        "lasso": LassoForm,
        "svm": SVMForm,
        "nb": NBForm,
        "knn": KNNForm,
        "decision_trees": DTForm,
        "random_forest": RFForm,
        "adaboost": ABForm,
        "voting": VoteForm,
    }

    form = forms[model]()

    if form.validate_on_submit():
        if model == "nb":
            nb_variations = {
                "BernoulliNB": lambda: BernoulliNB(alpha=form.alpha.data),
                "MultinomialNB": lambda: MultinomialNB(alpha=form.alpha.data),
                "ComplementNB": lambda: ComplementNB(alpha=form.alpha.data),
            }
            nb = nb_variations[form.whichnb.data]
        else:
            nb = None
        get_model = {
            # use lambda so models are not evaluated until called
            "lasso": lambda: Lasso(
                alpha=form.alpha.data, tol=form.tol.data, max_iter=form.max_iter.data
            ),
            "logreg": lambda: LogisticRegression(
                solver=form.solver.data,
                max_iter=form.max_iter.data,
                C=form.C.data,
                intercept_scaling=form.intercept_scaling.data,
            ),
            "svm": lambda: SVC(
                C=form.C.data,
                kernel=form.kernel.data,
                gamma=form.gamma.data,
                tol=form.tol.data,
                max_iter=form.max_iter.data,
                probability=True,
            ),
            # NB variation is chosen above
            "nb": nb,
            "knn": lambda: KNeighborsClassifier(n_neighbors=form.n_neighbors.data),
            "decision_trees": lambda: DecisionTreeClassifier(
                criterion=form.criterion.data,
                splitter=form.splitter.data,
                min_samples_split=int(form.min_samples_split.data)
                if form.min_samples_split.data > 1
                else form.min_samples_split.data,
                min_samples_leaf=1
                if form.min_samples_leaf.data == 1.0
                else form.min_samples_leaf.data,
                min_weight_fraction_leaf=1
                if form.min_weight_fraction_leaf.data == 1.0
                else form.min_weight_fraction_leaf.data,
                min_impurity_split=form.min_impurity_split.data,
            ),
            "random_forest": lambda: RandomForestClassifier(
                criterion=form.criterion.data,
                min_samples_split=int(form.min_samples_split.data)
                if form.min_samples_split.data > 1
                else form.min_samples_split.data,
                min_samples_leaf=1
                if form.min_samples_leaf.data == 1.0
                else form.min_samples_leaf.data,
                min_weight_fraction_leaf=1
                if form.min_weight_fraction_leaf.data == 1.0
                else form.min_weight_fraction_leaf.data,
                min_impurity_split=form.min_impurity_split.data,
            ),
            "adaboost": lambda: AdaBoostClassifier(
                learning_rate=form.learning_rate.data
            ),
            "voting": lambda: VotingClassifier(
                [
                    ("LogisticRegression", LogisticRegression()),
                    ("SVC", SVC(probability=True)),
                    ("MultinomialNB", MultinomialNB()),
                    ("KNeighborsClassifier", KNeighborsClassifier()),
                    ("DecisionTreeClassifier", DecisionTreeClassifier()),
                    ("RandomForestClassifier", RandomForestClassifier()),
                    ("AdaBoostClassifier", AdaBoostClassifier()),
                ],
                voting="soft",
                n_jobs=-1,
            ),
        }
        input_data = io.BytesIO()
        form.input_file.data.save(input_data)
        input_data.seek(0)  # so we can read the file
        if form.run.data:
            df = pd.read_csv(input_data, sep=None, header=0)
            X = df.drop(df.columns[form.target_index.data], 1)
            y = df[df.columns[form.target_index.data]]
            clf = get_model[model]()
            out_file_mod = NamedTemporaryFile(prefix=f"{model}_result_", delete=False)
            try:
                # this also trains model
                score, plot_id, clf = get_train_score(
                    clf, X, y, show_folds=form.show_folds.data
                )
            except ValueError:
                return (
                    render_template(
                        "blurb.html",
                        text="Bad input: try changing the target class index or cleaning up your data.",
                        title="Bad Input",
                    ),
                    400,
                )
            with open(out_file_mod.name, "wb") as f:
                pickle.dump({"clf": clf, "cols": X.columns}, f)
            uuid = upload_filepath(out_file_mod.name, score=f"{score:01.3f}")
            return redirect(
                url_for(
                    "learn_prediction_model_result",
                    model=model,
                    uuid=uuid,
                    plot=plot_id,
                )
            )

        elif form.view_data.data:
            return view_data(form)
        elif form.help_btn.data:
            text = "PLACEHOLDER: help display"
            return render_template("odpac_blurb.html", text=text, title="Placeholder"), 501
        else:
            text = "Bad Request"
            return render_template("odpac_blurb.html", text=text, title="400"), 400

    return render_template("odpac_form.html", heading=MODEL_LIST[model], form=form)


@application.route("/odpac/learn/prediction/<model>/result/<uuid>/<plot>")
def learn_prediction_model_result(model, uuid, plot):
    check_valid_model(model)
    score = result_score_by_uuid(uuid)
    return render_template(
        "odpac_learn-prediction-model-result.html",
        auc=score,
        model=model,
        uuid=uuid,
        plot=plot,
    )


@application.route("/odpac/learn/prediction/<model>/info")
def learn_prediction_model_info(model):
    check_valid_model(model)
    return render_template(
        "proceed-box.html",
        title=f"About Learn Predictions Models Using {MODEL_LIST[model]}",
        url=url_for("model_train", model=model),
    )


@application.route("/odpac/learn/predict/manual/<uuid>", methods=("GET", "POST"))
def predict_manual(uuid=None):
    result = None
    with read_result_file_by_uuid(uuid) as f:
        model = pickle.load(f)
    clf, cols = model["clf"], model["cols"]
    form = PredictForm(*cols)
    if form.validate_on_submit():
        features = dir(form)
        # grab all attributes that have feature in their name
        features = [getattr(form, f).data for f in features if "feature" in f]
        result = clf.predict([features])[0]
    return render_template(
        "odpac_predict-form.html",
        heading="Enter Patient Information Below",
        form=form,
        result=result,
    )


def get_test_score(clf, X, y):

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    probas_ = clf.predict_proba(X)
    fpr, tpr, thresholds = roc_curve(y, probas_[:, 1])
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, lw=1, label=f"ROC - AUC: {roc_auc:0.4f}", color="b", alpha=0.9)

    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic")
    ax.legend(loc="lower right")
    img = NamedTemporaryFile(prefix=f"roc_plot_", delete=False)
    canvas.print_png(img.name)
    uuid = upload_filepath(file_path=img.name)
    return uuid


@application.route("/odpac/learn/predict/file/<uuid>", methods=("GET", "POST"))
def predict_file(uuid=None):
    result = False
    plot_id = False

    with read_result_file_by_uuid(uuid) as f:
        model = pickle.load(f)
    clf, cols = model["clf"], model["cols"]
    form = PredictFileForm(len(cols))
    if form.validate_on_submit():
        df = form.df
        if form.get_auc.data:
            X = df.drop(df.columns[-1], 1)
            y = df[df.columns[-1]]
            plot_id = get_test_score(clf, X, y)
            df = X
        out_file_data = NamedTemporaryFile(prefix=f"predict_result_", delete=False)
        # train on whole data
        y = clf.predict(df)
        y = pd.DataFrame(y)
        y.to_csv(out_file_data.name, index=False)
        uuid = upload_filepath(file_path=out_file_data.name)
        result = True
    return render_template(
        "odpac_predict-file-form.html",
        heading="Enter Patient Information Below",
        form=form,
        uuid=uuid,
        plot_id=plot_id,
        result=result,
    )


@application.route("/odpac/learn/predict/file/result/download/<uuid>")
def predict_file_result_download(uuid):
    return send_file(
        read_result_file_by_uuid(uuid),
        mimetype="text/plain",
        attachment_filename="result.csv",
        as_attachment=True,
    )
