#!/usr/bin/env python3
"""neural network"""
import numpy as np


def sigmoid(X):
    """sigmoid function"""
    return 1.0 / (1.0 + np.exp(-X))


class NeuralNetwork():
    """neural network with one hidden layer"""
    def __init__(self, nx, nodes):
        """constructor"""
        if type(nx) is not int:
            raise TypeError('nx must be an integer')
        if nx < 1:
            raise ValueError('nx must be a positive integer')
        if type(nodes) is not int:
            raise TypeError('nodes must be an integer')
        if nodes < 1:
            raise ValueError('nodes must be a positive integer')

        self.__W1 = np.random.normal(0, 1, size=(nodes, nx))
        self.__b1 = np.zeros((nodes, 1))
        self.__A1 = 0
        self.__W2 = np.random.normal(0, 1, size=(1, nodes))
        self.__b2 = 0
        self.__A2 = 0

    @property
    def W1(self):
        """getter W1"""
        return self.__W1

    @property
    def b1(self):
        """getter b1"""
        return self.__b1

    @property
    def A1(self):
        """getter A1"""
        return self.__A1

    @property
    def W2(self):
        """getter W2"""
        return self.__W2

    @property
    def b2(self):
        """getter b2"""
        return self.__b2

    @property
    def A2(self):
        """getter A2"""
        return self.__A2

    def forward_prop(self, X):
        """Calculates the forward
        propagation of the neural
        network"""
        self.__A1 = sigmoid(np.matmul(self.__W1, X) + self.__b1)
        self.__A2 = sigmoid(np.matmul(self.__W2, self.__A1) + self.__b2)
        return self.__A1, self.__A2

    def cost(self, Y, A):
        """Calculates the cost of
        the model using logistic regression"""
        m = Y.shape[1]
        cost = (-1 / m) * (np.matmul(np.log(A), Y.T) +
                           np.matmul(np.log(1.0000001 - A), 1 - Y.T))
        return np.squeeze(cost)

    def evaluate(self, X, Y):
        """Evaluates the neural network’s predictions"""
        self.forward_prop(X)
        cost = self.cost(Y, self.__A2)
        prediction = np.where(self.__A2 >= 0.5, 1, 0)
        return prediction, cost

    def gradient_descent(self, X, Y, A1, A2, alpha=0.05):
        """Calculates one pass of gradient descent
        on the neural network"""
        m = Y.shape[1]

        error = A2 - Y
        dw2 = np.matmul(A1, error.T) / m
        db2 = np.sum(error, axis=1, keepdims=True) / m

        dz0 = A1 * (1 - A1)
        dz1 = np.matmul(self.__W2.T, error) * dz0
        dw1 = np.matmul(X, dz1.T) / m
        db1 = np.sum(dz1, axis=1, keepdims=True) / m

        self.__W1 -= alpha * dw1.T
        self.__b1 -= alpha * db1
        self.__W2 -= alpha * dw2.T
        self.__b2 -= alpha * db2

    def train(self, X, Y, iterations=5000, alpha=0.05):
        """Trains the neural network"""
        if type(iterations) is not int:
            raise TypeError('iterations must be an integer')
        if iterations <= 0:
            raise ValueError('iterations must be a positive integer')

        if type(alpha) is not float:
            raise TypeError('alpha must be a float')
        if alpha < 0:
            raise ValueError('alpha must be positive')

        for i in range(iterations):
            self.forward_prop(X)
            self.gradient_descent(X, Y, self.__A1, self.__A2, alpha=alpha)

        return self.evaluate(X, Y)
