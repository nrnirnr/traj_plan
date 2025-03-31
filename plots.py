import numpy as np
import matplotlib.pyplot as plt
from functions import X_func, V_func, A_func, J_func

def plots(T, X, V, A, J,
               x_b, x_e, v_b, v_e, a_b, a_e, v_max, a_max, j_max):
    T_sum = [0]
    for i in T:
        if i:
            T_sum.append(T_sum[-1] + i)
    n = 1000
    t = np.linspace(0, T_sum[-1], n)
    q = np.array([X_func(T, X, V, A, J, i) for i in t])
    v = np.array([V_func(T, X, V, A, J, i) for i in t])
    a = np.array([A_func(T, X, V, A, J, i) for i in t])
    j = np.array([J_func(T, X, V, A, J, i) for i in t])

    fig, axes = plt.subplots(4, 1, figsize=(8, 10))

    axes[0].plot(t, q, lw=3)
    axes[0].set_xlabel(r'$t, \mathrm{s}$', loc='right', fontsize=9)
    axes[0].set_ylabel(r'$q, \mathrm{rad}$', loc='top', rotation=0, fontsize=9)
    axes[0].set_title('displacement')
    axes[0].axhline(y=x_b, color='grey', linestyle=':', alpha=0.5)
    axes[0].axhline(y=x_e, color='grey', linestyle=':', alpha=0.5)
    for i in T_sum:
        axes[0].axvline(x=i, color='grey', linestyle='--', alpha=0.3)

    axes[1].plot(t, v, lw=3)
    axes[1].set_xlabel(r'$t, \mathrm{s}$', loc='right', fontsize=9)
    axes[1].set_ylabel(r'$v, \frac{\mathrm{rad}}{\mathrm{s}}$', loc='top', rotation=0, fontsize=9)
    axes[1].set_title('velocity')
    axes[1].axhline(y=0, color='black', lw=1)
    axes[1].axhline(y=v_b, color='grey', linestyle=':', alpha=0.5)
    axes[1].axhline(y=v_e, color='grey', linestyle=':', alpha=0.5)
    axes[1].axhline(y=v_max, color='red', alpha=0.1)
    axes[1].axhline(y=-v_max, color='red', alpha=0.1)
    for i in T_sum:
        axes[1].axvline(x=i, color='grey', linestyle='--', alpha=0.3)

    axes[2].plot(t, a, lw=3)
    axes[2].set_xlabel(r'$t, \mathrm{s}$', loc='right', fontsize=9)
    axes[2].set_ylabel(r'$a, \frac{\mathrm{rad}}{\mathrm{s}^2}$', loc='top', rotation=0, fontsize=9)
    axes[2].set_title('acceleration')
    axes[2].axhline(y=0, color='black', lw=1)
    axes[2].axhline(y=a_b, color='grey', linestyle=':', alpha=0.5)
    axes[2].axhline(y=a_e, color='grey', linestyle=':', alpha=0.5)
    axes[2].axhline(y=a_max, color='red', alpha=0.1)
    axes[2].axhline(y=-a_max, color='red', alpha=0.1)
    for i in T_sum:
        axes[2].axvline(x=i, color='grey', linestyle='--', alpha=0.3)

    axes[3].plot(t, j, lw=3)
    axes[3].set_xlabel(r'$t, \mathrm{s}$', loc='right', fontsize=9)
    axes[3].set_ylabel(r'$j, \frac{\mathrm{rad}}{\mathrm{s}^3}$', loc='top', rotation=0, fontsize=9)
    axes[3].set_title('jerk')
    axes[3].axhline(y=0, color='black', lw=1)
    axes[3].axhline(y=j_max, color='red', alpha=0.1)
    axes[3].axhline(y=-j_max, color='red', alpha=0.1)
    for i in T_sum:
        axes[3].axvline(x=i, color='grey', linestyle='--', alpha=0.3)

    plt.subplots_adjust(hspace=1)
    plt.tight_layout()
    plt.show()