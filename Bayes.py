__author__ = 'Sriganesh'

import math

def test_naive_bayes(word_0, word_1, test):
    i = 0
    pr_1 = float(0)
    pr_0 = float(0)
    label = []
    while i < 200:
        x = test[i]
        for y in range(1,len(x)):
            pr_0 += math.log(word_0[y], math.e)*x[y]
            pr_1 += math.log(word_1[y], math.e)*x[y]
        if pr_0 > pr_1:
            label.append(0)
        else:
            label.append(1)
        pr_0, pr_1 = float(0), float(0)
        i += 1
    return label

def train_naive_bayes(train, label):
    pr_1 = 1
    pr_0 = 1
    count_0 = 0
    count_1 = 0
    for i in label:
        if i == 0:
            count_0 += 1
        if i == 1:
            count_1 += 1
    # Computing probabilities of the labelled documents
    pr_1 = float(count_1)/float(count_1+count_0)
    pr_0 = float(count_0)/float(count_1+count_0)
    # Counting all the words in the labelled documents
    # Count also the number of occurrences of a particular word in all the documents with the particular label.
    i = 0
    word_0 = [1 for i in range(len(train[0]))]
    word_1 = [1 for i in range(len(train[0]))]
    while i < 200:
        x = train[i]
        if label[i] == 0:
            for y in range(1,len(x)):
                word_0[y] += x[y]
        if label[i] == 1:
            for y in range(1,len(x)):
                word_1[y] += x[y]
        i += 1
    sum_0 = sum(word_0)
    sum_1 = sum(word_1)
    for i in range(len(word_0)):
        word_0[i] = float(word_0[i])/float(sum_0)
        word_1[i] = float(word_1[i])/float(sum_1)
    i = 0
    # Compute the probabilities of the the word given the label of the document.
    while i < 200:
        x = train[i]
        if label[i] == 0:
            for y in range(len(x)):
                word_0[y] = float(word_0[y])*float(pr_0)
        if label[i] == 1:
            for y in range(len(x)):
                word_1[y] = float(word_1[y])*float(pr_1)
        i += 1
    return (word_0,word_1)

f = open('train.data', 'r')
train = []
temp = []
label = []
count = 0
for line in f:
    temp = line.split(" ")
    count = max(count, int(temp[1]))
count += 1
for x in range(201):
    train.append([0 for i in range(count)])
f.close()
f = open('train.data','r')
for line in f:
    temp = line.split(" ")
    train[int(temp[0])][int(temp[1])] = int(temp[2])
f.close()
f = open('train.label', 'r')
for line in f:
    label.append(int(line))
(word_0, word_1) = train_naive_bayes(train[1:], label)
for x in range(201):
    train.append([0 for i in range(count)])
f.close()
f = open('test.data','r')
for line in f:
    temp = line.split(" ")
    train[int(temp[0])][int(temp[1])] = int(temp[2])
f.close()
result = test_naive_bayes(word_0, word_1, train[1:])
f = open('test.label', 'r')
i = 0
correct = 0
total = 0
for line in f:
    if result[i] == int(line):
        correct += 1
    total += 1
    i += 1
print float(correct)/float(total)