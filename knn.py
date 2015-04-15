__author__ = 'sriganesh'


import scipy.io
import scipy.spatial.distance
import operator
import matplotlib.pyplot as plt

def display(data):
    for x in data:
        print x

def compute_distances(train_data, test_data):
    if len(train_data)==0 or len(test_data)==0:
        return None
    NN =[]
    for faces in test_data:
        i = 0
        L = {}
        for example in train_data:
            L[i] = scipy.spatial.distance.cosine(faces, example)
            i += 1
        NN.append(sorted(L.items(),key=operator.itemgetter(1)))
    return NN

def train_knn(train_label, NN, k):
    i = 0
    labels = []
    for faces in NN:
        count_1, count_2 = 0, 0
        for x in faces[:k]:
            if train_label[x[i]] == 1:
                count_1 += 1
            else:
                count_2 += 1
        pr = float(count_1)/float(count_1+count_2)
        if pr >= 0.5:
            labels.append(1)
        else:
            labels.append(2)
    return labels

def accuracy(labels, test_labels):
    correct = 0
    i = 0
    while i < len(labels):
        if labels[i] == test_labels[i]:
            correct += 1
        i += 1
    return float(correct)/float(len(labels))

def cross_validate(data, labels, NN, n=10, k=9):
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
        L = train_knn(train_labels, NN[i], k)
        acc.append(1-accuracy(L, labels[start:end]))
        i += 1
    return float(sum(acc))/float(len(acc))

def compute_train_distances(data, n=10):
    limit = len(data)/n
    i = 0
    NN = []
    while i < n:
        start = i * limit
        end = (i+1) * limit
        train = list(data[:start])
        if len(train) > 0:
            train.extend(data[end:])
        else:
            train = list(data[end:])
        L = compute_distances(train,data[start:end])
        NN.append(L)
        i += 1
    return NN

if __name__== "__main__":
    print "Enter n for cross validation:"
    n = int(raw_input())
    data = scipy.io.loadmat("hw3_matlab/faces.mat")
    NN_train = compute_distances(data['traindata'], data['traindata'])
    NN = compute_distances(data['traindata'], data['testdata'])
    NN_10 = compute_train_distances(data['traindata'], n)
    cross_acc, train_acc, test_acc = [], [], []
    for k in range(1,101):
        cross_acc.append(cross_validate(data['traindata'],data['trainlabels'], NN_10, n, k))
        labels = train_knn(data['trainlabels'],NN, k)
        labels_train = train_knn(data['trainlabels'], NN_train, k)
        train_acc.append(1-accuracy(labels_train, data['trainlabels']))
        test_acc.append(1-accuracy(labels, data['testlabels']))
    for k in range(100):
        print "k= ", k
        print "Train Error :", train_acc[k]
        print "Cross Validation Error :", train_acc[k]
        print "Test Error:", test_acc[k]
        print "-------------------------------"
    lineup, = plt.plot(train_acc,label="train")
    linecross, = plt.plot(cross_acc,label="cross")
    linedown, =plt.plot(test_acc, label="test")
    plt.legend([lineup,linecross, linedown], ['Train', 'Cross', 'Test'])
    plt.show()