from lmfit import Model
import numpy as np

def logistic_fit(x, a, b, c):
    """
    x is variable.
    a is shift along x axis
    b is steepness
    c is asymptote max
    """
    return c / (1 + a * np.exp(-b*x))

LogisticModel = Model(logistic_fit)