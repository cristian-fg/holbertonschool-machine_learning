#!/usr/bin/env python3
""" Deep RNN """
import numpy as np


def deep_rnn(rnn_cells, X, h_0):
    """performs forward propagation for a deep RNN

    -> rnn_cells is a list of RNNCell instances of length l
        that will be used for the forward propagation
        * l is the number of layers

    -> X is the data to be used, given as a numpy.ndarray of shape (t, m, i)
        * t is the maximum number of time steps
        * m is the batch size
        * i is the dimensionality of the data

    -> h_0 is the initial hidden state, given as a
        numpy.ndarray of shape (l, m, h)
        * h is the dimensionality of the hidden state

    -> Returns: H, Y
        * H is a numpy.ndarray containing all of the hidden states
        * Y is a numpy.ndarray containing all of the outputs
    """
    T, _, _ = X.shape
    L, m, h = h_0.shape
    H = np.ones((T + 1, L, m, h))
    Y = []
    H[0] = h_0

    for t in range(T):
        x_t = X[t]
        for l, cell in enumerate(rnn_cells):
            h, y = cell.forward(H[t, l], x_t)
            H[t + 1, l] = h
            x_t = h
        Y.append(y)

    return H, np.array(Y)
