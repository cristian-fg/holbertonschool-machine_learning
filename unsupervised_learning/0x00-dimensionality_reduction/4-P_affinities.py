#!/usr/bin/env python3
"""P affinities"""
import numpy as np
P_init = __import__('2-P_init').P_init
HP = __import__('3-entropy').HP


def P_affinities(X, tol=1e-5, perplexity=30.0):
    """calculates the symmetric P affinities of a data set:

    -> X is a numpy.ndarray of shape (n, d) containing
        the dataset to be transformed by t-SNE
        * n is the number of data points
        * d is the number of dimensions in each point

    -> perplexity is the perplexity that all Gaussian
        distributions should have

    -> tol is the maximum tolerance allowed (inclusive)
        for the difference in Shannon entropy from perplexity
        for all Gaussian distributions

    -> Returns: P, a numpy.ndarray of shape (n, n)
        containing the symmetric P affinities
    """
    D, P, betas, H = P_init(X, perplexity)

    n, d = X.shape

    for i in range(n):
        high = None
        low = None

        Di = np.append(D[i, :i], D[i, i+1:])
        Hi, Pi = HP(Di, betas[i])

        H_dif = Hi - H

        while np.abs(H_dif) > tol:
            if H_dif > 0:
                low = betas[i].copy()
                if high is None:
                    betas[i] = betas[i] * 2
                else:
                    betas[i] = (betas[i] + high) / 2
            else:
                high = betas[i].copy()
                if low is None:
                    betas[i] = betas[i] / 2
                else:
                    betas[i] = (betas[i] + low) / 2

            Hi, Pi = HP(Di, betas[i])
            H_dif = Hi - H

        P[i, :i] = Pi[:i]
        P[i, i+1:] = Pi[i:]
    P = (P + P.T) / (2 * n)
    return P
