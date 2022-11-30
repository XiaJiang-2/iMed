#! /usr/bin/env python3
""" Performs grid search on various machine learning models,
    outputs summary results and raw results of grid search. """
import argparse
import datetime
import numpy as np
import os
import pandas as pd
import pickle
import time
import yaml
from multiprocessing import Process, Pipe
from sklearn_extensions.extreme_learning_machines import ELMClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import sklearn.linear_model

def parse_cmd_line():
    """Parse command line input."""
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
    parser = argparse.ArgumentParser(
        description="Report the AUROC of different machine learning models,\
        default is to use all types.")
    parser.add_argument("--deep", "-d",
                        help="Deep learning", action='store_true')
    parser.add_argument("--elm", "-e",
                        help="ELM", action='store_true')
    parser.add_argument("--lasso", "-a",
                        help="LASSO", action='store_true')
    parser.add_argument("--lr", '-r',
                        help="Logistic Regression", action='store_true')
    parser.add_argument("--knn", '-k',
                        help="K Nearest Neighbor", action ='store_true')
    parser.add_argument("--svm", '-s',
                        help="Support Vector Machine Classifier", action ='store_true')
    parser.add_argument("--nb", '-n',
                        help="Naive Bayes", action ='store_true')
    parser.add_argument("--config", '-c', default="conf.yaml",
                        help="Configuration file. Default is conf.yaml")
    parser.add_argument("--resultdir",
                        help="The directory for results in CSV format.", default=timestamp+"-results")
    parser.add_argument("--save-models", action='store_true',
                        help="Save the models to be used for testing later.")
    parser.add_argument("--save-summary", action='store_true',
                        help="Save the summary results")
    parser.add_argument("--save-grid-search-results", action='store_true')
    parser.add_argument("dataset",nargs="+",
                        help="The data to be used for training.")
    ret = parser.parse_args()
    if not (ret.lasso or ret.elm or ret.deep or ret.lr or ret.knn or ret.svm or ret.nb):
        ret.lasso = True
        ret.elm   = True
        ret.deep  = True
        ret.lr    = True
        ret.knn   = True
        ret.svm   = True
        ret.nb    = True
    return ret

def child_process(func):
    """Makes the function run as a separate process
    needed for keras to work on multiple datasets"""
    def wrapper(*args, **kwargs):
        def worker(conn, func, args, kwargs):
            conn.send(func(*args, **kwargs))
            conn.close()
        parent_conn, child_conn = Pipe()
        p = Process(target=worker, args=(child_conn, func, args, kwargs))
        p.start()
        ret = parent_conn.recv()
        p.join()
        return ret
    return wrapper

def grid_search(func):
    """Decorator for machine learning functions
    to take the result and perform grid search"""
    @child_process
    def wrapper(*args, **kwargs):
        clf, params = func(*args, **kwargs)
        return GridSearchCV(clf, params, scoring='roc_auc', refit=True,
                            cv=StratifiedKFold(n_splits=5), return_train_score=True, n_jobs=-1)
    return wrapper

@grid_search
def lasso(conf):
    """LASSO"""
    return sklearn.linear_model.Lasso(), conf

@grid_search
def logistic(conf):
    """Logistic Regression"""
    return sklearn.linear_model.LogisticRegression(), conf

@grid_search
def elm(conf):
    """Extreme Learning Machine"""
    return  ELMClassifier(), conf

@grid_search
def knn(conf):
    """K Nearest Neighbor"""
    return KNeighborsClassifier(), conf

@grid_search
def naive_bayes(conf):
    """Naive Bayes"""
    return BernoulliNB(), conf

@grid_search
def svm(conf):
    """Support Vector Machine"""
    return SVC(), conf

def deep_build_fn(data_shape=(-1,29), nodes=25, layers=1 ):
    """Build the model for KerasClassifier"""
    from keras.layers import Dense
    from keras.models import Sequential
    model = Sequential()
    # the first layer
    model.add(Dense(output_dim=nodes, input_dim=data_shape[1], activation='relu'))
    for _ in range(layers - 1):
        model.add(Dense(nodes, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    return model

@grid_search
def deep(conf, shape):
    """Deep Learning"""
    from keras.wrappers.scikit_learn import KerasClassifier
    return KerasClassifier(build_fn=deep_build_fn, data_shape=shape), conf

@child_process
def run_grid_search(clf, conf, X, y, resultdir, clf_name):
    """Helper function to execute the grid search."""
    gscv = clf(conf) if clf is not deep else clf(conf, X.shape)
    gscv.fit(X,y)
    pd.DataFrame(gscv.cv_results_).to_csv(os.path.join(resultdir, clf_name+'_results.csv'),index=False)
    pickle_path = os.path.join(resultdir, clf_name+'-model.pkl')
    with open(pickle_path, 'wb') as f:
        pickle.dump(gscv.best_estimator_,f)
    results={'auroc_'+clf_name: gscv.best_score_, 'params_'+clf_name:gscv.best_params_}
    # est = {clf_name: gscv.best_estimator_}
    est = {clf_name: pickle_path}
    return results, est

def run_one_dataset(X, y, args, config, resultdir, fname):
    """Run Grid searches for all the methods once."""
    outdir = os.path.join(resultdir, fname)
    os.makedirs(outdir)
    models = []
    if args.lasso:
        models.append((lasso,'LASSO'))
    if args.elm:
        models.append((elm,'ELM'))
    if args.deep:
        models.append((deep,'deep_learning'))
    if args.lr:
        models.append((logistic, 'LR'))
    if args.knn:
        models.append((knn, 'KNN'))
    if args.nb:
        models.append((naive_bayes, 'naive_bayes'))
    if args.svm:
        models.append((svm, 'SVM'))
    # add all results to the result dictionary
    results = {"filename": fname}
    trained_model_paths={"filename": fname}
    for model, name in models:
        result_dict, model_dict = run_grid_search(model, config[name], X, y, outdir, name)
        results.update(result_dict)
        trained_model_paths.update(model_dict)

    print(fname)
    summary_string = ""
    for _, m in models:
        summary_string += "%40s%20s%40s\n" % (m, results['auroc_'+m], results['params_' + m])
    print(summary_string)
    with open(os.path.join(outdir, 'summary.txt'), 'w') as f:
        f.write(summary_string)
    return results, trained_model_paths

if __name__ == "__main__":
    # parse the input
    args = parse_cmd_line()
    with open(args.config) as f:
        config = yaml.load(f)

    # create directory for results
    os.makedirs(args.resultdir)

    # make sure all datasets exist
    for p in args.dataset:
        if not os.path.exists(p):
            raise FileNotFoundError(p)

    files = [ f for f in args.dataset if os.path.isfile(f) ]
    dirs = [ d for d in args.dataset if os.path.isdir(d) ]

    all_results = list()
    avg_results=pd.DataFrame()
    for dataset in files:
        try:
            data = pd.read_csv(dataset)
            X = np.array(data.drop(['T'], 1))
            y = np.array(data['T'])
        except:
            print("could not load " + dataset)
        else:
            results ,models = run_one_dataset(X, y, args, config, args.resultdir, os.path.basename(dataset))
            all_results.append(results)
    avg_results['files']=pd.DataFrame(all_results).mean()

    for d in dirs:
        dir_results = list()
        for f in os.listdir(d):
            dataset=os.path.join(d,f)
            dir_path= os.path.join(args.resultdir, os.path.basename(os.path.abspath(d)))
            try:
                data = pd.read_csv(dataset)
                X = np.array(data.drop(['T'], 1))
                y = np.array(data['T'])
            except:
                print("could not load " + dataset)
            else:
                results, models = run_one_dataset(X, y, args, config, dir_path,
                                                  os.path.basename(dataset))
                dir_results.append(results)
        df = pd.DataFrame(dir_results)
        df.to_csv(os.path.join(dir_path,'train_results_summary.csv'))
        mean = df.mean()
        avg_results[d] = df.mean()
        all_results += dir_results
    all_df = pd.DataFrame(all_results).set_index('filename')
    all_df.to_csv(os.path.join(args.resultdir, 'all_results.csv'))
    avg_results.to_csv(os.path.join(args.resultdir, 'avg_results.csv'))


