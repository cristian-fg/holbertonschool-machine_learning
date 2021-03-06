#!/usr/bin/env python3
"""Initialize t-SNE"""
import numpy as np


def P_init(X, perplexity):
    """initializes all variables required to
        calculate the P affinities in t-SNE:

    -> X is a numpy.ndarray of shape (n, d) containing
        the dataset to be transformed by t-SNE
        * n is the number of data points
        * d is the number of dimensions in each point

    -> perplexity is the perplexity that all
        Gaussian distributions should have

    -> Returns: (D, P, betas, H)
        * D: a numpy.ndarray of shape (n, n) that calculates
            the squared pairwise distance between two data points
            -- The diagonal of D should be 0s

        * P: a numpy.ndarray of shape (n, n) initialized to
            all 0‘s that will contain the P affinities

        * betas: a numpy.ndarray of shape (n, 1) initialized to
            all 1’s that will contain all of the beta values

        * H is the Shannon entropy for perplexity perplexity
            with a base of 2
    """
    n, d = X.shape
    a = np.sum(X * X, 1)
    b = np.repeat(a[:, np.newaxis], n, axis=1)
    D = b + b.T - 2 * X.dot(X.T)
    np.fill_diagonal(D, 0.)

    P = np.zeros((n, n))

    betas = np.ones((n, 1))

    H = np.log2(perplexity)

    return D, P, betas, H
