from par_calc import plan
from plots import plots

def traj_plan(x_b: float, x_e: float,
              v_b: float = 0, v_e: float = 0,
              a_b: float = 0, a_e: float = 0,
              v_max: float = 2, a_max: float = 0.5, j_max: float = 1):
    try:
        T, X, V, A, J = plan(x_b, x_e, v_b, v_e, a_b, a_e, v_max, a_max, j_max)
    except Exception or ValueError as e:
        print(f'Unable to plan a trajectory: {e}')
        return

    T_sum = [0]
    for i in range(1, 8):
        T_sum.append(T_sum[-1] + T[i])

    print(f'the minimal time is {T_sum[-1]} sec. \n')
    print('q(t) = ')
    for i in range(7):
        if T_sum[i] != T_sum[i + 1]:
            print(f'        {X[i]} + {V[i]} * (t - {T_sum[i]}) + {A[i] / 2} * (t - {T_sum[i]})^2 + {J[i] / 6} * (t - {T_sum[i]})^3'
                  f',    {T_sum[i]} <= t <= {T_sum[i + 1]}')


    plots(T, X, V, A, J, x_b, x_e, v_b, v_e, a_b, a_e, v_max, a_max, j_max)
    return
