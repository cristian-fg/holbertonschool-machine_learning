#!/usr/bin/env python3
"""BIC for a GMM"""
import numpy as np
expectation_maximization = __import__('8-EM').expectation_maximization


def BIC(X, kmin=1, kmax=None, iterations=1000, tol=1e-5, verbose=False):
    """finds the best number of clusters for a GMM using
        the Bayesian Information Criterion:

    -> X is a numpy.ndarray of shape (n, d) containing the data set

    -> kmin is a positive integer containing the minimum number
        of clusters to check for (inclusive)

    -> kmax is a positive integer containing the maximum number
        of clusters to check for (inclusive)

    -> iterations is a positive integer containing the maximum
        number of iterations for the EM algorithm

    -> tol is a non-negative float containing the tolerance
        for the EM algorithm

    -> verbose is a boolean that determines if the EM algorithm
        should print information to the standard output

    -> Returns: best_k, best_result, l, b,
        or None, None, None, None on failure

        * best_k is the best value for k based on its BIC

        * best_result is tuple containing pi, m, S
            ** pi is a numpy.ndarray of shape (k,) containing the
                cluster priors for the best number of clusters
            ** m is a numpy.ndarray of shape (k, d) containing
                the centroid means for the best number of clusters
            ** S is a numpy.ndarray of shape (k, d, d) containing
                the covariance matrices for the best number of clusters

        * l is a numpy.ndarray of shape (kmax - kmin + 1) containing
            the log likelihood for each cluster size tested

        * b is a numpy.ndarray of shape (kmax - kmin + 1) containing
            the BIC value for each cluster size tested
            ** p is the number of parameters required for the model
            ** n is the number of data points used to create the model
            ** l is the log likelihood of the model
    """
    try:
        if kmin >= kmax:
            return None, None, None, None

        n, d = X.shape
        lk = []
        b = []
        for i in range(kmin, kmax + 1):
            pi, m, S, g, lkhood = expectation_maximization(X,
                                                           i,
                                                           iterations,
                                                           tol,
                                                           verbose)

            """Multivariate: 𝑀𝐷+𝑀(𝐷(𝐷+1)/2)+𝑀−1
                free parameters formula"""
            p = i * d + i * (d * (d + 1) / 2) + i - 1
            BIC = p * np.log(n) - 2 * lkhood
            if i == kmin:
                BIC_prev = BIC

            if BIC_prev >= BIC:
                best_k = i
                best_result = (pi, m, S)
                BIC_prev = BIC

            lk.append(lkhood)
            b.append(BIC)

        return best_k, best_result, np.array(lk), np.array(b)
    except Exception:
        return None, None, None, None
