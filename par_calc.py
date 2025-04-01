from math import sqrt

def plan(x_b: float, x_e: float,
              v_b: float = 0, v_e: float = 0,
              a_b: float = 0, a_e: float = 0,
              v_max: float = 2, a_max: float = 0.5, j_max: float = 1):
    def update_segments(seg):
        X[seg] = X[seg - 1] + V[seg - 1] * T[seg] + A[seg - 1] * T[seg] ** 2 / 2 + J[seg - 1] * T[seg] ** 3 / 6
        V[seg] = V[seg - 1] + A[seg - 1] * T[seg] + J[seg - 1] * T[seg] ** 2 / 2
        A[seg] = A[seg - 1] + J[seg - 1] * T[seg]

    def t4_pos():
        T = [0] * 8
        V = v_max
        if V >= (2 * a_max ** 2 - a0 ** 2) / (2 * j_max) + v0:
            Aa = a_max
        else:
            Aa = sqrt(j_max * (v_max - v0) + a0 ** 2 / 2)
        if V >= (2 * a_max ** 2 - a7 ** 2) / (2 * j_max) + v7:
            Ad = a_max
        else:
            Ad = sqrt(j_max * (v_max - v7) + a7 ** 2 / 2)
        T[1] = (Aa - a0) / j_max
        T[3] = Aa / j_max
        T[2] = ((V - v0) - (2 * Aa ** 2 - a0 ** 2) / (2 * j_max)) / Aa
        if T[2] < 0:
            raise ValueError
        v1 = v0 + a0 * T[1] + j_max * T[1] ** 2 / 2
        v2 = v1 + Aa * T[2]
        xa = (v0 * T[1] + a0 * T[1] ** 2 / 2 + j_max * T[1] ** 3 / 6 +
              v1 * T[2] + Aa * T[2] ** 2 / 2 +
              v2 * T[3] + Aa * T[3] ** 2 / 2 - j_max * T[3] ** 3 / 6)
        T[5] = Ad / j_max
        T[7] = (Ad + a7) / j_max
        T[6] = ((V - v7) - (2 * Ad ** 2 - a7 ** 2) / (2 * j_max)) / Ad
        if T[6] < 0:
            raise ValueError
        v5 = V - j_max * T[5] ** 2 / 2
        v6 = v5 - Ad * T[6]
        xd = (V * T[5] - j_max * T[5] ** 3 / 6 +
              v5 * T[6] - Ad * T[6] ** 2 / 2 +
              v6 * T[7] - Ad * T[7] ** 2 / 2 + j_max * T[7] ** 3 / 6)
        if x < xa + xd:
            raise Exception
        T[4] = (x - (xa + xd)) / V
        return T

    def t2_t6_pos():
        root_expr = (6 * a_max ** 4 + 6 * a_max ** 2 * a0 ** 2 - 8 * a_max * a0 ** 3 + 3 * a0 ** 4 +
                 6 * a_max ** 2 * a7 ** 2 + 8 * a_max * a7 ** 3 + 3 * a7 ** 4 -
                 12 * a_max ** 2 * j_max * v0 + 24 * a_max * a0 * j_max * v0 -
                 12 * a0 ** 2 * j_max * v0 + 12 * j_max ** 2 * v0 ** 2 - 12 * a_max ** 2 * j_max * v7 -
                 24 * a_max * a7 * j_max * v7 - 12 * a7 ** 2 * j_max * v7 +
                 12 * j_max ** 2 * v7 ** 2 + 24 * a_max * j_max ** 2 * x)
        if root_expr < 0:
            raise Exception
        V = - (a_max ** 2 / (2 * j_max)) + (1 / (2 * (6 ** 0.5) * j_max)) * sqrt(root_expr)
        if V > v_max or V < (2 * a_max ** 2 - a0 ** 2) / (2 * j_max) + v0 or V < (2 * a_max ** 2 - a7 ** 2) / (2 * j_max) + v7:
            raise Exception
        T = [0] * 8
        A = a_max
        T[1] = (A - a0) / j_max
        T[3] = A / j_max
        T[2] = ((V - v0) - (2 * A ** 2 - a0 ** 2) / (2 * j_max)) / A
        if T[2] < 0:
            raise ValueError
        T[5] = A / j_max
        T[7] = (A + a7) / j_max
        T[6] = ((V - v7) - (2 * A ** 2 - a7 ** 2) / (2 * j_max)) / A
        if T[6] < 0:
            raise ValueError
        return T

    if j_max == 0:
        raise ValueError('Jerk limitations cannot be null')
    neg = False
    v_max = abs(v_max)
    a_max = abs(a_max)
    v0 = v_b
    v7 = v_e
    a0 = a_b
    a7 = a_e
    x = x_e - x_b
    if x < 0:
        neg = True
        x = -x
        v0 = -v0
        v7 = -v7
        a0 = -a0
        a7 = -a7
    if abs(v0) > v_max:
        raise ValueError('The initial velocity does not fit in the set kinematic limits')
    if abs(v7) > v_max:
        raise ValueError('The final velocity does not fit in the set kinematic limits')
    if abs(a0) > a_max:
        raise ValueError('The initial acceleration does not fit in the set kinematic limits')
    if abs(a7) > a_max:
        raise ValueError('The final acceleration does not fit in the set kinematic limits')
    if (a0 > 0 and v0 + a0 ** 2 / (2 * j_max) > v_max) or (a0 < 0 and v0 - a0 ** 2 / (2 * j_max) < -v_max):
        raise ValueError('Velocity limit is inevitable to exceed')
    if (a7 > 0 and v7 - a7 ** 2 / (2 * j_max) < -v_max) or (a7 < 0 and v7 + a7 ** 2 / (2 * j_max) > v_max):
        raise ValueError('The final velocity is unreachable in the set kinematic limits')

    try:
        T = t4_pos()
    except Exception:
        try:
            T = t2_t6_pos()
        except Exception:
            raise Exception('The overall displacement is too small for this approach')
    
    if neg:
        J = [-j_max, 0, j_max, 0, j_max, 0, -j_max]
    else:
        J = [j_max, 0, -j_max, 0, -j_max, 0, j_max]
    X = [x_b] + [0] * 7
    V = [v_b] + [0] * 7
    A = [a_b] + [0] * 7
    for seg in range(1, 8):
        update_segments(seg)
    return T, X, V, A, J
