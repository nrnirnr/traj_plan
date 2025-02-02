def count_values(x_b, v_b, a_b, j_b, s_b, t):
    x_e = count_x(x_b, v_b, a_b, j_b, s_b, t)
    v_e = count_v(v_b, a_b, j_b, s_b, t)
    a_e = count_a(a_b, j_b, s_b, t)
    j_e = count_j(j_b, s_b, t)
    return x_e, v_e, a_e, j_e

def count_j(j_b, s_b, t):
    return j_b + s_b * t

def count_a(a_b, j_b, s_b, t):
    return a_b + j_b * t + s_b / 2 * t ** 2

def count_v(v_b, a_b, j_b, s_b, t):
    return v_b + a_b * t + j_b / 2 * t ** 2 + s_b / 6 * t ** 3

def count_x(x_b, v_b, a_b, j_b, s_b, t):
    return x_b + v_b * t + a_b / 2 * t ** 2 + j_b / 6 * t ** 3 + s_b / 24 * t ** 4

def jerk_gain(delta_j, s_max):
    delta_j = abs(delta_j)
    t_1 = delta_j / s_max
    return[0, t_1]

def acceleration_gain(delta, j_max, s_max):
    def count_next(j_b, s_b, delta_t):
        delta_a_cur = count_a(0, j_b, s_b, delta_t)
        return delta_a_cur

    delta = abs(delta)
    t = [0] * 4
    delta_a = [0] * 4
    j = [0] + [0, j_max, j_max]
    s = [0] + [s_max, 0, -s_max]

    seg_1 = jerk_gain(j_max, s_max)
    seg_3 = jerk_gain(-j_max, s_max)

    delta_done = 0
    t[1] = seg_1[1]
    delta_a[1] = count_next(j[1], s[1], t[1])
    delta_done += delta_a[1]
    t[3] = seg_3[1]
    delta_a[3] = count_next(j[3], s[3], t[3])
    delta_done += delta_a[3]

    delta_a[2] = delta - delta_done
    t[2] = delta_a[2] / j_max
    return t

def velocity_gain(delta, a_0, a_7, a_max, j_max, s_max):
    def count_next(a_b, j_b, s_b, delta_t):
        delta_v_cur = count_v(0, a_b, j_b, s_b, delta_t)
        a_next = count_a(a_b, j_b, s_b, delta_t)
        return delta_v_cur, a_next

    if delta < 0:
        delta = -delta
        a_0 = -a_0
        a_7 = -a_7
    t = [0] * 8
    delta_v = [0] * 8
    a = [a_0] + [0] * 7
    j = [0, j_max, j_max, 0, 0, -j_max, -j_max]
    s = [s_max, 0, -s_max, 0, -s_max, 0, s_max]

    seg_1_3 = acceleration_gain(a_max - a_0, j_max, s_max)
    seg_5_7 = acceleration_gain(a_7 - a_max, j_max, s_max)

    delta_done = 0
    for i in range(1, 4):
        t[i] = seg_1_3[i]
        delta_v[i], a[i] = count_next(a[i - 1], j[i - 1], s[i - 1], t[i])
        delta_done += delta_v[i]
    for i in range(5, 8):
        t[i] = seg_5_7[i - 4]
        delta_v[i], a[i] = count_next(a[i - 1], j[i - 1], s[i - 1], t[i])
        delta_done += delta_v[i]

    delta_v[4] = delta - delta_done
    t[4] = delta_v[4] / a_max
    return t

def position_gain(delta, v_0, v_15, a_0, a_15, v_max, a_max, j_max, s_max):
    def count_next(v_b, a_b, j_b, s_b, delta_t):
        delta_x_cur = count_x(0, v_b, a_b, j_b, s_b, delta_t)
        v_next = count_v(v_b, a_b, j_b, s_b, delta_t)
        a_next = count_a(a_b, j_b, s_b, delta_t)
        return delta_x_cur, v_next, a_next

    if delta < 0:
        delta = -delta
        v_0 = -v_0
        v_15 = -v_15
        a_0 = -a_0
        a_15 = -a_15
    t = [0] * 16
    delta_x = [0] * 16
    v = [v_0] + [0] * 15
    a = [a_0] + [0] * 15
    j = [0, j_max, j_max, 0, 0, -j_max, -j_max, 0, 0, -j_max, -j_max, 0, 0, j_max, j_max]
    s = [s_max, 0, -s_max, 0, -s_max, 0, s_max, 0, -s_max, 0, s_max, 0, s_max, 0, -s_max]

    seg_1_7 = velocity_gain(v_max - v_0, a_0, 0, a_max, j_max, s_max)
    seg_9_15 = velocity_gain(v_15 - v_max, 0, a_15, a_max, j_max, s_max)

    delta_done = 0
    for i in range(1, 8):
        t[i] = seg_1_7[i]
        delta_x[i], v[i], a[i] = count_next(v[i - 1], a[i - 1], j[i - 1], s[i - 1], t[i])
        delta_done += delta_x[i]
    for i in range(9, 16):
        t[i] = seg_9_15[i - 8]
        delta_x[i], v[i], a[i] = count_next(v[i - 1], a[i - 1], j[i - 1], s[i - 1], t[i])
        delta_done += delta_x[i]

    delta_x[8] = delta - delta_done
    t[8] = delta_x[8] / v_max
    return t



#данная функция рассматривает исключительно случай прохождения всех сегментов с достижением кинематических пределов (перемещение достаточно большое)
def trajectory(x_b: float = 0, x_e: float = 0, v_b: float = 0, v_e: float = 0, v_max: float = 5, a_b: float = 0, a_e: float = 0, a_max: float = 10, j_max: float = 30, s_max: float = 500, t = False):
    eps = 1e-6
    def update_values(seg):
        nonlocal x, v, a, j, s, t_min
        x[seg], v[seg], a[seg], j[seg] = count_values(x[seg - 1], v[seg - 1], a[seg - 1], j[seg - 1], s[seg - 1], t_min[seg])

    x = [x_b] + [0] * 15
    v = [v_b] + [0] * 15
    a = [a_b] + [0] * 15
    j = [0] * 16
    if (x_e > x_b):
        s = [s_max, 0, -s_max, 0, -s_max, 0, s_max, 0, -s_max, 0, s_max, 0, s_max, 0, -s_max]
    else:
        s = [-s_max, 0, s_max, 0, s_max, 0, -s_max, 0, s_max, 0, -s_max, 0, -s_max, 0, s_max]

    delta_x = x_e - x_b
    t_min = position_gain(delta_x, v_b, v_e, a_b, a_e, v_max, a_max, j_max, s_max)

    '''if t != False:
        if t < t_min_sum - eps:
            raise ValueError(f'Trajectory is unreachable int the set time. \n'
                             f'The minimal time is {t_min_sum}')
        elif t > t_min_sum + eps:
            #пересчет траектории в заданных условиях
            return
    else:'''

    for i in range(1, 15):
        update_values(i)
    return t_min, x, v, a, j, s


