__author__ = 'sriganesh'

import scipy.io
from matplotlib import pyplot as plt
from sklearn import svm
import numpy as np

def train_svm(train_data, labels, C_val=500):
    clf = svm.SVC(C=C_val,kernel='linear')
    clf.fit(train_data, labels)
    return clf


def classify(data,clf):
    labels = []
    for x in data:
        labels.append(clf.predict(x))
    return labels

def accuracy(labels, test_labels):
    correct = 0
    i = 0
    while i < len(labels):
        if labels[i] == test_labels[i]:
            correct += 1
        i += 1
    return float(correct)/float(len(labels))

def cross_validate(data, labels, n=10, C_val = 500):
    limit = len(data)/n
    i = 0
    acc =[]
    while i < n:
        start = i * limit
        end = (i+1) * limit
        train = list(data[:start])
        if len(train) > 0:
            train.extend(data[end:])
        else:
            train = list(data[end:])
        train_labels = list(labels[:start])
        if len(train_labels) > 0:
            train_labels.extend(labels[end:])
        else:
            train_labels = list(labels[end:])
        clf = train_svm(train, np.ravel(train_labels),C_val)
        L = classify(data[start:end],clf)
        acc.append(1-accuracy(L, labels[start:end]))
        i += 1
    return float(sum(acc))/float(len(acc))

if __name__== "__main__":
    #n = int(raw_input())
    data = scipy.io.loadmat("hw3_matlab/faces.mat")
    C = [10, 100, 1000, 10000, 50000, 100000, 500000, 1000000]
    cross_acc, train_acc, test_acc = [], [], []
    for x in C:
        print "C: ", x
        clf = train_svm(data['traindata'], np.ravel(data['trainlabels']), x)
        labels = classify(data['testdata'],clf)
        temp = 1-accuracy(labels, data['testlabels'])
        test_acc.append(temp)
        print "Test Error:", temp
        labels = classify(data['traindata'],clf)
        temp =  1-accuracy(labels, data['trainlabels'])
        train_acc.append(temp)
        print "Train Error:", temp
        temp = cross_validate(data['traindata'],data['trainlabels'], 10, x)
        cross_acc.append(temp)
        print "Cross validate Error (n=10):", temp
        print "---"
    lineup, = plt.plot(train_acc,label="train")
    linecross, = plt.plot(cross_acc,label="cross")
    linedown, =plt.plot(test_acc, label="test")
    plt.legend([lineup,linecross, linedown], ['Train', 'Cross', 'Test'])
    plt.show()
