__author__ = 'Sriganesh'

import math

def get_likelihood(x,y,w):
    result = 0
    for j in range(len(y)):
        ans = w[0]
        for i in range(1,len(x)):
            ans += x[j][i]*w[i]
        result += y[j]*(ans) - math.log((1+math.exp(ans)))
    return result

def get_sigmoid(x, w):
    ans = w[0]
    for i in range(1, len(x)):
        ans += x[i]*w[i]
    result = float(math.exp(ans))
    result /= float((1+result))
    return result

def train_reg(train, y, w):
    step = 0.0001
    result = 0
    x = []
    compute = []
    i = 0
    while i < 200:
        x.append(train[i])
        i += 1
    likelihood = get_likelihood(x,y,w)
    while True:
        pr = []
        compute = []
        for i in range(len(y)):
            pr.append(get_sigmoid(x[i], w))
        for i in range(len(x[0])):
            if i == 0:
                for j in range(len(y)):
                    result += (y[j]-pr[j])
            else:
                for j in range(len(y)):
                    result += x[j][i]*(y[j]-pr[j])
            compute.append(step*float(result))
            print result,
            result = 0
        print ''
        for t in range(len(w)):
            w[t] += compute[t]
        temp = get_likelihood(x,y,w)
        if temp < likelihood:
            break
        likelihood = temp
    return w

def test_reg(w, train):
    x = []
    i = 0
    label = []
    while i < 200:
        x.append(train[i])
        i += 1
    for i in range(len(x)):
        temp = get_sigmoid(x[i], w)
        if temp > 0.5:
            label.append(1)
        else:
            label.append(0)
    return label

f = open('train.data', 'r')
train = []
temp = []
label = []
count = 0
for line in f:
    temp = line.split(" ")
    count = max(count, int(temp[1]))
count += 1
initial_weights = [0 for i in range(count)]
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
weights = train_reg(train[1:], label, initial_weights)
f.close()
f = open('test.data', 'r')
for x in range(201):
    train[x] = [0 for i in range(count)]
for line in f:
    temp = line.split(" ")
    train[int(temp[0])][int(temp[1])] = int(temp[2])
result = test_reg(weights, train[1:])
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