__author__ = 'Sriganesh'
import math, random, matplotlib.pyplot as plt

stumps = {}

def get_alpha(error):
    return math.log((1-error)/error, math.e)

def get_identity(my_labels, t, w = None, equal=True):
    correct = 0
    # weighted Error calculation
    if not equal:
        for i in range(len(my_labels)):
            if my_labels[i] != t[i]:
                correct += w[i]
        return float(correct)#/float(sum(w))
    # accuracy calculation
    else:
        for i in range(len(my_labels)):
            if my_labels[i] == t[i]:
                correct += 1
        return float(correct)/float(len(t))

def get_error(t, data, hypothesis, alphas):
    error = 0
    for i in range(len(t)):
        if t[i] != predict_boost(hypothesis,alphas,data[i]):
            error += 1
    return float(error)/float(len(t))

def get_criteria(data, feat):
    min_val, max_val, total = data[0][feat], data[0][feat], 0.0
    for x in data:
        min_val = min(min_val, x[feat])
        max_val = max(max_val, x[feat])
        total += x[feat]
    avg = total/len(data)
    return min_val, max_val, avg

def populate_stumps(small, big, feat):
    #step = random.uniform(0.3, 4.5)
    step = 1
    L = []
    small += step
    while small < big:
        L.append(small)
        small += step
    stumps[feat] = L

def populate_labels(data, t, margin, feat):
    label_1, label_2 = [], []
    for i in range(len(data)):
        if data[i][feat] > margin:
            label_2.append(2)
            label_1.append(1)
        else:
            label_2.append(1)
            label_1.append(2)
    if get_identity(label_1, t) < get_identity(label_2, t):
        return (label_2, 1)
    return (label_1, -1)

def fit_model(data, t, w):
    error = 10000000000000
    alpha = 0
    best = (0,0,0)
    label = []
    for i in stumps.keys():
        for x in stumps[i]:
            my_labels, rule = populate_labels(data, t, x, i)
            temp = get_identity(my_labels, t, w, False)
            if temp < error:
                error = temp
                alpha = get_alpha(error)
                best = (i, x, rule)
                label = my_labels
    return alpha, best, label, error

def get_weights(alpha, w, label, t):
    for i in range(len(w)):
        k = 0
        if label[i] != t[i]: k = 1
        w[i] *= math.exp(alpha*k)
    total = float(sum(w))
    for i in range(len(w)):
        w[i] /= total
    return w

def train_boost(w, data, t, test= None, test_label= None):
    classifier_weights = []
    hypothesis = []
    for i in range(len(data[0])):
        min_val, max_val, avg = get_criteria(data,i)
        populate_stumps(min_val, max_val, i)
    plot_data_1 = []
    plot_data_2 = []
    cdf = []
    for i in range(100):
        alpha, thesis, label, error = fit_model(data, t, w)
        w = get_weights(alpha, w, label, t)
        hypothesis.append(thesis)
        classifier_weights.append(alpha)
        train_error = get_error(t, data, hypothesis, classifier_weights)
        if test is not None:
            test_error = get_error(test_label, test, hypothesis, classifier_weights)
            plot_data_2.append(test_error)
        else:
            if i == 9 or i == 49 or i == 99:
                cdf.append(predict_boost(hypothesis, classifier_weights, data, True) * t[i])
        plot_data_1.append(train_error)
    if test is None:
        plt.plot(cdf)
        plt.show()
    return hypothesis, classifier_weights, plot_data_1, plot_data_2

def predict_boost(hypothesis, alphas, data, cdf = False):
    total = 0
    for i in range(len(hypothesis)):
        if data[hypothesis[i][0]] > hypothesis[i][1]:
            total += alphas[i] * hypothesis[i][2]
        else:
            total += alphas[i] * hypothesis[i][2] * -1
    if cdf:
        return total
    if total > 0:
        return 2
    else:
        return 1

def random_split(percent, data, t):
    indices = random.sample(xrange(0,len(data)), percent)
    train_data = []
    train_label = []
    test = []
    label = []
    for x in indices:
        train_data.append(data[x])
        train_label.append(t[x])
    for i in range(len(data)):
        if i not in indices:
            test.append(data[i])
            label.append(t[i])
    return train_data, train_label, test, label

def etl():
    f = open('bupa.data','r')
    data = []
    t = []
    for line in f:
        L = map(float, line.split(',')[:6])
        data.append(L)
        t.append(int(line.split(',')[6].strip()))
    w1 = [float(1)/float(len(data)) for i in range(len(data))]
    hypothesis, alpha, train_error, test_error = train_boost(w1, data, t)
    k = 0
    for i in hypothesis:
        print "Feature chosen-----Split boundary chosen"
        print "----", i[0],'--------------', i[1]
        k += 1
        if k > 9:
            break
    w = [float(1)/float(int(0.90*len(data))) for i in range(int(0.90*len(data)))]
    train, test = [], []
    for x in range(3):
        print "----------------------Sample", x+1, "---------------------------"
        train_data, train_label, test_data, test_label = random_split(int(0.90*len(data)), data, t)
        hypothesis, alpha, train_error, test_error = train_boost(w, train_data, train_label, test_data, test_label)
        print "train error:", train_error
        print"test_error:", test_error
        train.append(train_error)
        test.append(test_error)
    avg_train, avg_test = [], []
    for i in range(len(train[0])):
        temp_1, temp_2 = 0, 0
        for j in range(len(train)):
            temp_1 += train[j][i]
            temp_2 += test[j][i]
        avg_train.append(float(temp_1)/float(len(train)))
        avg_test.append(float(temp_2)/float(len(test)))
    plt.plot(avg_train, label="train")
    plt.plot(avg_test, label="test")
    plt.show()


if __name__ == '__main__':
    etl()
