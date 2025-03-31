import numpy as np

def count_tau(T, t):
    if t < 0:
        return None
    for seg in range (1, 8):
        if t < T[seg]:
            return t, seg - 1
        t -= T[seg]
    return None

def X_func(T, X, V, A, J, t):
    z = count_tau(T, t)
    if z is None:
        return np.nan
    tau, i = z
    return X[i] + V[i] * tau + A[i] * tau ** 2 / 2 + J[i] * tau ** 3 / 6

def V_func(T, X, V, A, J, t):
    z = count_tau(T, t)
    if z is None:
        return np.nan
    tau, i = z
    return V[i] + A[i] * tau + J[i] * tau ** 2 / 2

def A_func(T, X, V, A, J, t):
    z = count_tau(T, t)
    if z is None:
        return np.nan
    tau, i = z
    return A[i] + J[i] * tau

def J_func(T, X, V, A, J, t):
    z = count_tau(T, t)
    if z is None:
        return np.nan
    tau, i = z
    return J[i]
