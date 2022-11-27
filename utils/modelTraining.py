import sys

from sklearn.preprocessing import MinMaxScaler

sys.path.append('../../')
from tensorflow import keras, metrics
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
import tensorflow.keras.optimizers as opt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, StratifiedShuffleSplit
from sklearn.metrics import roc_curve, auc
from tensorflow.keras import regularizers
import pandas as pandas
import shap


def loadandprocess(file, sep='\t', predtype=1, scaled=True):
    """

    :return:
    :param file:
    :param sep:
    :param predtype:
    :param scaled:
    :return:
    """
    """
    :param file:
    :param sep:
    :param predtype:
    :param scaled:
    :return:
    """
    print(file)
    if file[-3:] == "txt":
        df = pandas.read_csv(file, sep, lineterminator='\n')
    elif file[-3:] == "csv":
        df = pandas.read_csv(file)
    column_names = list(df.columns)[0:-1]
    print(column_names)
    # cols=[0,532]
    # predset = df.drop(df.columns[cols],axis=1)
    if predtype == 1:
        predset = df.iloc[:, :-1]  # all columns except for the last one are predictors
    elif predtype == 2:
        predset = df.iloc[:, 1:-1]  # all columns except for the first and last ones are predictors
    if scaled:
        scaler = MinMaxScaler()
        scaler.fit(predset)
        predset = scaler.transform(predset)
    # If scaled is true, Normalized to [0,1]. Default is true.
    print(f'pred shape: {predset.shape}')
    print(f'pred dimension: {predset.ndim}')
    # tarcol2 = n.array(df.columns[-1])
    tarcol = df.iloc[:, -1]
    print(tarcol.head(4))
    print(f'target frame dimension: {tarcol.ndim}')
    print(f'target frame shape: {tarcol.shape}')
    tarcol = tarcol.to_numpy()
    print(f'target dimension: {tarcol.ndim}')
    predset = predset.to_numpy()
    # if have a problem"numpy.ndarray' object has no attribute 'to_numpy" when scale = True,
    # you can just comment"predset = predset.to_numpy()" because predset = scaler.transform(predset) will return numpy object directly
    print(predset.shape)
    # which we want to make a prediction
    return (predset, tarcol, column_names)
def create_model(mstruct, idim, drate, kinit, iacti, hacti, oacti, opti, lrate, momen ,dec,ls, L1, L2,ltype):
    # create a model that KerasClassifier needs as an input for parameter build_fn
    model = Sequential()
    if ltype==0:
        model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer = kinit, activation= iacti))
    elif ltype==1:
        model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer = kinit, activation= iacti,kernel_regularizer=regularizers.l1(L1)))
    elif ltype ==2:
        model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer = kinit, activation= iacti,kernel_regularizer=regularizers.l2(L2)))
    elif ltype ==3:
        model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer = kinit, activation= iacti,kernel_regularizer=regularizers.l1_l2(l1=L1, l2=L2)))


    model.add(Dropout(drate))
    nlayers = len(mstruct)
    nhiddenlayers =nlayers -2
    for i in range(nhiddenlayers):
        model.add(Dense(mstruct[i+1], activation=hacti))
        model.add(Dropout(drate))
    model.add(Dense(mstruct[nlayers-1], activation=oacti))
    # Using 'softmax' as the activation function for the output layer will return all 0.5s when class is binary

    for layer in model.layers:
        print(layer.weights)
    cur_opt = opti
    if opti == 'Adagrad':
        cur_opt = opt.Adagrad(lr = lrate, decay=dec)
    elif opti == 'SGD':
        cur_opt = opt.SGD(lr = lrate, momentum=momen, decay=dec)
    model.compile(optimizer=cur_opt, loss=ls, metrics = "accuracy")
    model.save('user_training_model.h5')
    return model
def model_val(params, x_cv, y_cv):
    print(params)
    m_struct = params['mstruct']
    n_epochs =params['epochs']
    batch=params['batch_size']
    print (m_struct, n_epochs, batch)
    del params['epochs']
    del params['batch_size']
    clf = KerasClassifier(build_fn=create_model, ** params, epochs=n_epochs, batch_size=batch )
    params['batch_size'] = batch
    params['epochs'] = n_epochs
    clf.fit(x_cv, y_cv)
    return clf



def model_gsearch_val(predset, target, params, nsplits=5, seed=123, scores='roc_auc'):
    split = 'SKF'
    """
Conduct grid search with 80% of data, and then validate the best model using the 20% set aside data in two ways:1.
validate using the best model (esitmator) found by grid search, and 2. validate using a model "manually" created
with the best set of parameter values found by grid search
    :param predset:
    :param target:
    :param params:
    :param nsplits:
    :param seed:
    :param scores:
    :return:
    """
    # keep 20% dataset as validation data set, and 80% dataset as CV train dataset
    strat_shuf= StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    for CV_index, val_index in strat_shuf.split(predset, target):
        print(len(CV_index))
    print(len(val_index))
    print(target[CV_index])
    print(target[val_index])
    X_CV, X_val = predset[CV_index], predset[val_index]
    Y_CV, Y_val = target[CV_index], target[val_index]
    clf = KerasClassifier(build_fn=create_model)
    if split == "SKF":
        cur_cv = StratifiedKFold(n_splits=nsplits, shuffle=True, random_state=seed)
    elif split == 'SSS':
        cur_cv = StratifiedShuffleSplit(n_splits=nsplits, test_size=0.2, random_state=seed)
    g_search= GridSearchCV(clf, param_grid=params,cv=cur_cv,refit ='AUC', scoring=scores, return_train_score =True,n_jobs= -1)
    # we have 2 ways to predict validation dataset
    # 1: the best model from gridsearch;
    gs=g_search.fit(X=X_CV, y=Y_CV)
    # 2: the best model trained manually from best parameter from gridsearch;
    clf_val = model_val(gs.best_params_, X_CV, Y_CV)
    # way1 results
    Y_pred1 = gs.predict_proba(X_val)[:, 1]
    # way2 results
    Y_pred2 = clf_val.predict_proba(X_val)[:,1]
    Y_pred1 = Y_pred1.reshape(-1)
    Y_pred2= Y_pred2.reshape(-1)
    # way1 AUC
    FP, TP, thresholds = roc_curve(Y_val.astype(float), Y_pred1.astype(float))
    val_auc_grid = auc(FP, TP)
    # way2 AUC
    FP2, TP2, thresholds2 = roc_curve(Y_val.astype(float), Y_pred2.astype(float))
    val_auc_manu = auc(FP2, TP2)
    plt.title('Validation roc Curve')
    plt.plot(FP,  TP, label = r'Mean Validation ROC (area=%0.4f)' % val_auc_grid)
    plt.plot([0, 1], ls="--")
    plt.plot([0, 0], [1, 0], c=".7"), plt.plot([1, 1], c=".7")
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend()
    plt.savefig('static/img/roc/roc_curve.png')
    plt.clf()
    print("best val score grid: "+str(val_auc_grid))
    print("best val score manual: "+str(val_auc_manu))
    print("best mean auc: %f and best index: %s using %s" % (gs.best_score_, gs.best_index_,gs.best_params_))
    print("")
    # shap
    # def f(X):
    #     # return best_model.predict(X).flatten()
    #     return gs.predict_proba(X)[:, 1]
    #
    # explainer = shap.KernelExplainer(f, X_CV)
    # shap_values = explainer.shap_values(X_val[10])

    return gs, val_auc_grid, val_auc_manu