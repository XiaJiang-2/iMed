#! /usr/bin/env python3
"""Test a trained model on the data"""
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from task2a import deep_build_fn

if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as f:
        clf = pickle.load(f)
    X = np.array((pd.read_csv(sys.argv[2])).drop(['T'], 1))
    y = np.array((pd.read_csv(sys.argv[2]))['T'])

    y_score = clf.predict_proba(X)

    fpr,tpr,_ = roc_curve(y, y_score)
    auroc=auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr,tpr, label=f'ROC curve (area = {auroc})')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()


