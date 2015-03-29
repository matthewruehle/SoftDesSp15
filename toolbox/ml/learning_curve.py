""" 
Exploring learning curves for classification of handwritten digits 

Toolbox submission for Matt Ruehle.

...is that it? I... don't feel like I actually learned any ML. This toolbox was kind of just writing a for loop and using scipy/sklearn...
"""

import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

def make_accuracy_plot(num_trials=10):
    """
    Plots model accuracy versus amount of model training. Shorter runtime than the deviation plot, since it uses fewer trials and percentages.
    """
    data = load_digits()
    # print data.DESCR
    train_percentages = range(5, 95, 5)
    test_accuracies = numpy.zeros(len(train_percentages))

    for i in range(len(train_percentages)):
        individual_trial_accuracies = []
        for j in range(num_trials):
            X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=train_percentages[i]*.01)
            model = LogisticRegression(C=10**-10)
            model.fit(X_train, y_train)
            individual_trial_accuracies.append(model.score(X_test, y_test))
        test_accuracies[i] = numpy.mean(individual_trial_accuracies)

    fig = plt.figure()
    plt.plot(train_percentages, test_accuracies, 'b')
    plt.xlabel('Percentage of Data Used for Training')
    plt.ylabel('Accuracy on Test Set')
    plt.show()


def make_deviation_plot(num_trials=100):
    """
    Plots the standard deviation as a function of training percentages. Takes a bit of time to run.
    """
    data = load_digits()
    # print data.DESCR
    train_percentages = range(5, 95, 1)
    test_accuracies = numpy.zeros(len(train_percentages))
    test_sdevs = numpy.zeros(len(train_percentages))

    for i in range(len(train_percentages)):
        individual_trial_accuracies = []
        for j in range(num_trials):
            X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=train_percentages[i]*.01)
            model = LogisticRegression(C=10**-10)
            model.fit(X_train, y_train)
            individual_trial_accuracies.append(model.score(X_test, y_test))
        test_sdevs[i] = numpy.std(individual_trial_accuracies)
        test_accuracies[i] = numpy.mean(individual_trial_accuracies)

    fig = plt.figure()
    plt.plot(train_percentages, test_sdevs)
    plt.xlabel('Percentage used for training')
    plt.ylabel('Standard deviation')
    plt.show()

if __name__ == "__main__":
    make_accuracy_plot()
    # make_deviation_plot()