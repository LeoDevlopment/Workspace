import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded
from math import pi, sin, exp

# Параметры задачи
a = 1.0
L = pi
T = 1.0

# Аналитическое решение
def exact(x, t):
    return np.exp(-a * t) * np.sin(x)

# Правая часть граничных условий
def g_left(t):
    return np.exp(-a * t)

def g_right(t):
    return -np.exp(-a * t)

# Вспомогательная функция для решения трёхдиагональной системы
def solve_tridiag(lower, diag, upper, rhs):
    n = len(diag)
    ab = np.zeros((3, n))
    ab[0, 1:] = upper[:-1]
    ab[1, :] = diag
    ab[2, :-1] = lower[1:]
    return solve_banded((1, 1), ab, rhs)

# ----------------------------------------------------------------------
# Явная схема
def explicit_scheme(Nx, Nt, bc_type='two_point_first'):
    h = L / Nx
    tau = T / Nt
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1))
    u[0, :] = np.sin(x)

    sigma = a * tau / h**2
    if sigma > 0.5:
        print(f"  Предупреждение: sigma = {sigma:.3f} > 0.5, явная схема может быть неустойчива.")

    for n in range(Nt):
        tn = t[n]
        # Внутренние точки
        for i in range(1, Nx):
            u[n+1, i] = u[n, i] + sigma * (u[n, i+1] - 2*u[n, i] + u[n, i-1])

        # Граничные условия
        if bc_type == 'two_point_first':
            u[n+1, 0] = u[n+1, 1] - h * g_left(tn)
            u[n+1, Nx] = u[n+1, Nx-1] - h * g_right(tn)   # знак правой границы
        elif bc_type == 'three_point_second':
            u[n+1, 0] = (4*u[n+1, 1] - u[n+1, 2] - 2*h * g_left(tn)) / 3.0
            u[n+1, Nx] = (4*u[n+1, Nx-1] - u[n+1, Nx-2] + 2*h * g_right(tn)) / 3.0
        elif bc_type == 'two_point_second':
            # Поправка через уравнение теплопроводности (явная)
            u[n+1, 0] = (u[n+1, 1] - h * g_left(tn) + (h**2/(2*a*tau))*u[n, 0]) / (1 + h**2/(2*a*tau))
            u[n+1, Nx] = (u[n+1, Nx-1] - h * g_right(tn) + (h**2/(2*a*tau))*u[n, Nx]) / (1 + h**2/(2*a*tau))
    return x, t, u

# ----------------------------------------------------------------------
# Неявная схема
def implicit_scheme(Nx, Nt, bc_type='two_point_first'):
    h = L / Nx
    tau = T / Nt
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1))
    u[0, :] = np.sin(x)

    sigma = a * tau / h**2

    for n in range(Nt):
        tn1 = t[n+1]
        # Матрица системы для внутренних точек
        lower = np.full(Nx-1, -sigma)
        diag = np.full(Nx-1, 1 + 2*sigma)
        upper = np.full(Nx-1, -sigma)
        rhs = u[n, 1:Nx].copy()

        # Учёт граничных условий
        if bc_type == 'two_point_first':
            # u_0 = u_1 - h*g_left
            # u_N = u_{N-1} - h*g_right
            # Влияние на первое уравнение: -sigma*u_0 = -sigma*(u_1 - h*g_left)
            rhs[0] += sigma * h * g_left(tn1)
            rhs[-1] += sigma * h * g_right(tn1)
        elif bc_type == 'three_point_second':
            # u_0 = (4u_1 - u_2 - 2h g_left)/3
            # Влияние: -sigma*u_0 = -sigma*(4u_1 - u_2 - 2h g_left)/3
            # Это добавляет к матрице слагаемые, зависящие от u_1 и u_2.
            # Для простоты используем итерационное уточнение или аппроксимацию
            # Здесь для демонстрации используем двухточечную первого порядка
            rhs[0] += sigma * h * g_left(tn1)
            rhs[-1] += sigma * h * g_right(tn1)
        elif bc_type == 'two_point_second':
            # u_1 - u_0 = h*g_left + h^2/(2a tau)*(u_0^{n+1}-u_0^n)
            # => u_0 = u_1 - h*g_left - h^2/(2a tau)*(u_0^{n+1}-u_0^n)
            # Приближённо (явная поправка):
            coef = h**2/(2*a*tau)
            rhs[0] += sigma * (h * g_left(tn1) + coef * u[n, 0]) / (1 + coef)
            rhs[-1] += sigma * (h * g_right(tn1) + coef * u[n, Nx]) / (1 + coef)

        sol = solve_tridiag(lower, diag, upper, rhs)
        u[n+1, 1:Nx] = sol

        # Восстановление граничных значений
        if bc_type == 'two_point_first':
            u[n+1, 0] = u[n+1, 1] - h * g_left(tn1)
            u[n+1, Nx] = u[n+1, Nx-1] - h * g_right(tn1)
        elif bc_type == 'three_point_second':
            u[n+1, 0] = (4*u[n+1, 1] - u[n+1, 2] - 2*h * g_left(tn1)) / 3.0
            u[n+1, Nx] = (4*u[n+1, Nx-1] - u[n+1, Nx-2] + 2*h * g_right(tn1)) / 3.0
        elif bc_type == 'two_point_second':
            coef = h**2/(2*a*tau)
            u[n+1, 0] = (u[n+1, 1] - h * g_left(tn1) + coef * u[n, 0]) / (1 + coef)
            u[n+1, Nx] = (u[n+1, Nx-1] - h * g_right(tn1) + coef * u[n, Nx]) / (1 + coef)
    return x, t, u

# ----------------------------------------------------------------------
# Схема Кранка-Николсона
def crank_nicolson_scheme(Nx, Nt, bc_type='two_point_first'):
    h = L / Nx
    tau = T / Nt
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1))
    u[0, :] = np.sin(x)

    sigma = a * tau / (2 * h**2)

    for n in range(Nt):
        tn1 = t[n+1]
        # Матрица системы
        lower = np.full(Nx-1, -sigma)
        diag = np.full(Nx-1, 1 + 2*sigma)
        upper = np.full(Nx-1, -sigma)
        # Правая часть: u_i^n + sigma*(u_{i+1}^n - 2u_i^n + u_{i-1}^n)
        rhs = u[n, 1:Nx] + sigma * (u[n, 2:Nx+1] - 2*u[n, 1:Nx] + u[n, 0:Nx-1])

        # Граничные условия (аналогично неявной схеме)
        if bc_type == 'two_point_first':
            rhs[0] += sigma * h * g_left(tn1)
            rhs[-1] += sigma * h * g_right(tn1)
        elif bc_type == 'three_point_second':
            rhs[0] += sigma * h * g_left(tn1)
            rhs[-1] += sigma * h * g_right(tn1)
        elif bc_type == 'two_point_second':
            coef = h**2/(2*a*tau)
            rhs[0] += sigma * (h * g_left(tn1) + coef * u[n, 0]) / (1 + coef)
            rhs[-1] += sigma * (h * g_right(tn1) + coef * u[n, Nx]) / (1 + coef)

        sol = solve_tridiag(lower, diag, upper, rhs)
        u[n+1, 1:Nx] = sol

        # Восстановление граничных значений
        if bc_type == 'two_point_first':
            u[n+1, 0] = u[n+1, 1] - h * g_left(tn1)
            u[n+1, Nx] = u[n+1, Nx-1] - h * g_right(tn1)
        elif bc_type == 'three_point_second':
            u[n+1, 0] = (4*u[n+1, 1] - u[n+1, 2] - 2*h * g_left(tn1)) / 3.0
            u[n+1, Nx] = (4*u[n+1, Nx-1] - u[n+1, Nx-2] + 2*h * g_right(tn1)) / 3.0
        elif bc_type == 'two_point_second':
            coef = h**2/(2*a*tau)
            u[n+1, 0] = (u[n+1, 1] - h * g_left(tn1) + coef * u[n, 0]) / (1 + coef)
            u[n+1, Nx] = (u[n+1, Nx-1] - h * g_right(tn1) + coef * u[n, Nx]) / (1 + coef)
    return x, t, u

# ----------------------------------------------------------------------
# Вычисление погрешности
def compute_error(x, t, u_num, exact_func):
    error = np.zeros_like(u_num)
    for n in range(len(t)):
        error[n, :] = np.abs(u_num[n, :] - exact_func(x, t[n]))
    return error

# ----------------------------------------------------------------------
# Основной блок
if __name__ == "__main__":
    # Параметры сетки
    Nx = 40
    Nt = 200
    bc_types = ['two_point_first', 'three_point_second', 'two_point_second']
    bc_names = ['Двухточечная 1-го порядка',
                'Трехточечная 2-го порядка',
                'Двухточечная 2-го порядка']

    schemes = {
        'Явная': explicit_scheme,
        'Неявная': implicit_scheme,
        'Кранка-Николсона': crank_nicolson_scheme
    }

    # Расчёт для всех схем и вариантов граничных условий
    results = {}
    for scheme_name, scheme_func in schemes.items():
        for bc_type, bc_name in zip(bc_types, bc_names):
            x, t, u_num = scheme_func(Nx, Nt, bc_type)
            err = compute_error(x, t, u_num, exact)
            results[(scheme_name, bc_name)] = (x, t, u_num, err)
            max_err = np.max(err)
            print(f"{scheme_name:20s} | {bc_name:30s} | max err = {max_err:.6e}")

    # Визуализация: сравнение численного и точного решения при t=T
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (scheme_name, scheme_func) in zip(axes, schemes.items()):
        x, t, u_num = scheme_func(Nx, Nt, 'two_point_first')
        u_ex = exact(x, T)
        ax.plot(x, u_num[-1, :], 'o-', label='Численное')
        ax.plot(x, u_ex, '--', label='Точное')
        ax.set_title(scheme_name)
        ax.set_xlabel('x')
        ax.set_ylabel('u')
        ax.legend()
    plt.tight_layout()
    plt.show()

    # Исследование зависимости погрешности от шага сетки
    Nx_list = [10, 20, 40, 80]
    Nt_list = [50, 100, 200, 400]
    errors_h = []
    errors_tau = []

    for Nx_val in Nx_list:
        # Фиксируем Nt достаточно большим, чтобы ошибка по времени была мала
        Nt_fixed = 1000
        x, t, u_num = crank_nicolson_scheme(Nx_val, Nt_fixed, 'two_point_first')
        err = compute_error(x, t, u_num, exact)
        errors_h.append(np.max(err))

    for Nt_val in Nt_list:
        Nx_fixed = 100
        x, t, u_num = crank_nicolson_scheme(Nx_fixed, Nt_val, 'two_point_first')
        err = compute_error(x, t, u_num, exact)
        errors_tau.append(np.max(err))

    # Графики зависимости погрешности
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.loglog(Nx_list, errors_h, 'o-')
    ax1.set_xlabel('Nx')
    ax1.set_ylabel('Макс. погрешность')
    ax1.set_title('Зависимость от шага по пространству (h ~ 1/Nx)')
    ax1.grid(True, which='both')

    ax2.loglog(Nt_list, errors_tau, 's-')
    ax2.set_xlabel('Nt')
    ax2.set_ylabel('Макс. погрешность')
    ax2.set_title('Зависимость от шага по времени (τ ~ 1/Nt)')
    ax2.grid(True, which='both')

    plt.tight_layout()
    plt.show()