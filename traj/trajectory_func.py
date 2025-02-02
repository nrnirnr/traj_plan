from trajectory_parameters import count_x, count_v, count_a, count_j

def count_tau(t, t_min):
    i = 1
    tau = t
    while i < 15 and tau > t_min[i]:
        tau -= t_min[i]
        i += 1
    return tau, i

def X(t, t_min, x, v, a, j, s):
    tau, i = count_tau(t, t_min)
    if tau > t_min[-1] or tau < 0:
        return None
    return count_x(x[i - 1], v[i - 1], a[i - 1], j[i - 1], s[i - 1], tau)

def V(t, t_min, v, a, j, s):
    tau, i = count_tau(t, t_min)
    if tau > t_min[-1] or tau < 0:
        return None
    return count_v(v[i - 1], a[i - 1], j[i - 1], s[i - 1], tau)

def A(t, t_min, a, j, s):
    tau, i = count_tau(t, t_min)
    if tau > t_min[-1] or tau < 0:
        return None
    return count_a(a[i - 1], j[i - 1], s[i - 1], tau)

def J(t, t_min, j, s):
    tau, i = count_tau(t, t_min)
    if tau > t_min[-1] or tau < 0:
        return None
    return count_j(j[i - 1], s[i - 1], tau)

def S(t, t_min, s):
    tau, i = count_tau(t, t_min)
    if tau > t_min[-1] or tau < 0:
        return None
    return s[i - 1]