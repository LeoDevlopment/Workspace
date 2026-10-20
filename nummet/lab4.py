"""
Лабораторная работа N4
Решение двумерного начально-краевой задачи для уравнения параболического типа
с использованием схем переменных направлений и дробных шагов.

Задача N1:
    du/dt = a*(d2u/dx2 + d2u/dy2),  a > 0
    u(0,y,t)   = cos(mu2*y)*exp(-(mu1^2+mu2^2)*a*t)
    u(pi,y,t)  = (-1)^mu1 * cos(mu2*y)*exp(-(mu1^2+mu2^2)*a*t)
    u(x,0,t)   = cos(mu1*x)*exp(-(mu1^2+mu2^2)*a*t)
    u(x,pi,t)  = (-1)^mu2 * cos(mu1*x)*exp(-(mu1^2+mu2^2)*a*t)
    u(x,y,0)   = cos(m1*x)*cos(m2*y)

    Аналитическое решение:
    U(x,y,t) = cos(m1*x)*cos(m2*y)*exp(-(m1^2+m2^2)*a*t)

    Варианты: 1) m1=1,m2=1  2) m1=2,m2=1  3) m1=1,m2=2
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # для сохранения графиков без отображения окна
import matplotlib.pyplot as plt


# =====================================================================
#                        ПАРАМЕТРЫ ЗАДАЧИ
# =====================================================================
a = 1.0                     # коэффициент теплопроводности
m1, m2 = 1, 1               # параметры (вариант 1: m1=1, m2=1)
mu1, mu2 = m1, m2           # параметры граничных условий

Lx, Ly = np.pi, np.pi       # размеры области
T = 0.1                     # конечное время


# =====================================================================
#                        АНАЛИТИЧЕСКОЕ РЕШЕНИЕ
# =====================================================================
def U_exact(x, y, t):
    """Аналитическое решение задачи."""
    return np.cos(m1 * x) * np.cos(m2 * y) * np.exp(-(m1**2 + m2**2) * a * t)


# =====================================================================
#                        ГРАНИЧНЫЕ УСЛОВИЯ
# =====================================================================
def bc_left(y, t):
    return np.cos(mu2 * y) * np.exp(-(mu1**2 + mu2**2) * a * t)

def bc_right(y, t):
    return (-1)**mu1 * np.cos(mu2 * y) * np.exp(-(mu1**2 + mu2**2) * a * t)

def bc_bottom(x, t):
    return np.cos(mu1 * x) * np.exp(-(mu1**2 + mu2**2) * a * t)

def bc_top(x, t):
    return (-1)**mu2 * np.cos(mu1 * x) * np.exp(-(mu1**2 + mu2**2) * a * t)


# =====================================================================
#                МЕТОД ПРОГОНКИ (алгоритм Томаса)
# =====================================================================
def solve_tridiagonal(A, B, C, F):
    """
    Решение системы с трёхдиагональной матрицей:
        A[i]*u[i-1] + B[i]*u[i] + C[i]*u[i+1] = F[i],  i = 0..n-1
    A[0] и C[n-1] не используются (граничные условия уже учтены в F).
    """
    n = len(F)
    alpha = np.zeros(n)
    beta = np.zeros(n)
    u = np.zeros(n)

    # Прямой ход
    alpha[0] = -C[0] / B[0]
    beta[0] = F[0] / B[0]
    for i in range(1, n):
        denom = B[i] + A[i] * alpha[i-1]
        alpha[i] = -C[i] / denom
        beta[i] = (F[i] - A[i] * beta[i-1]) / denom

    # Обратный ход
    u[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        u[i] = alpha[i] * u[i+1] + beta[i]
    return u


# =====================================================================
#     СХЕМА ПЕРЕМЕННЫХ НАПРАВЛЕНИЙ (Писмена-Рекфорда)
# =====================================================================
def solve_peaceman_rachford(Nx, Ny, hx, hy, tau, U0, T, a):
    """
    Решение схемы переменных направлений (Писмена-Рекфорда).
    Каждый полушаг: неявный по одному направлению, явный по другому.
    Схема безусловно устойчива, имеет 2-й порядок точности.
    """
    U = U0.copy()
    U_new = U.copy()
    U_half = U.copy()
    Nt = int(round(T / tau))

    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)

    for n in range(Nt):
        t_next = (n + 1) * tau

        # -------- Первый полушаг: неявный по x, явный по y --------
        for j in range(1, Ny):
            A = np.zeros(Nx - 1)
            B = np.zeros(Nx - 1)
            C = np.zeros(Nx - 1)
            F = np.zeros(Nx - 1)

            for i in range(1, Nx):
                A[i-1] = -a * tau / (2 * hx**2)
                B[i-1] = 1 + a * tau / hx**2
                C[i-1] = -a * tau / (2 * hx**2)
                F[i-1] = U[i, j] + (a * tau / (2 * hy**2)) * (
                    U[i, j+1] - 2*U[i, j] + U[i, j-1]
                )

            # Учёт граничных условий
            F[0]  += -A[0]  * bc_left(y[j], t_next)
            F[-1] += -C[-1] * bc_right(y[j], t_next)

            U_half[1:Nx, j] = solve_tridiagonal(A, B, C, F)

        # Границы по x
        for j in range(Ny + 1):
            U_half[0,  j] = bc_left(y[j], t_next)
            U_half[Nx, j] = bc_right(y[j], t_next)
        # Границы по y
        for i in range(Nx + 1):
            U_half[i, 0]  = bc_bottom(x[i], t_next)
            U_half[i, Ny] = bc_top(x[i], t_next)

        # -------- Второй полушаг: явный по x, неявный по y --------
        for i in range(1, Nx):
            A = np.zeros(Ny - 1)
            B = np.zeros(Ny - 1)
            C = np.zeros(Ny - 1)
            F = np.zeros(Ny - 1)

            for j in range(1, Ny):
                A[j-1] = -a * tau / (2 * hy**2)
                B[j-1] = 1 + a * tau / hy**2
                C[j-1] = -a * tau / (2 * hy**2)
                F[j-1] = U_half[i, j] + (a * tau / (2 * hx**2)) * (
                    U_half[i+1, j] - 2*U_half[i, j] + U_half[i-1, j]
                )

            F[0]  += -A[0]  * bc_bottom(x[i], t_next)
            F[-1] += -C[-1] * bc_top(x[i], t_next)

            U_new[i, 1:Ny] = solve_tridiagonal(A, B, C, F)

        # Обновление границ
        for i in range(Nx + 1):
            U_new[i, 0]  = bc_bottom(x[i], t_next)
            U_new[i, Ny] = bc_top(x[i], t_next)
        for j in range(Ny + 1):
            U_new[0,  j] = bc_left(y[j], t_next)
            U_new[Nx, j] = bc_right(y[j], t_next)

        U = U_new.copy()

    return U


# =====================================================================
#              МЕТОД ДРОБНЫХ ШАГОВ (Яненко)
# =====================================================================
def solve_fractional_steps(Nx, Ny, hx, hy, tau, U0, T, a):
    """
    Решение методом дробных шагов (Яненко).
    На каждом шаге решается одномерное уравнение по одному направлению.
    Схема абсолютно устойчива.
    """
    U = U0.copy()
    U_new = U.copy()
    U_half = U.copy()
    Nt = int(round(T / tau))

    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)

    for n in range(Nt):
        t_next = (n + 1) * tau

        # -------- Первый дробный шаг: неявный по x --------
        for j in range(1, Ny):
            A = np.zeros(Nx - 1)
            B = np.zeros(Nx - 1)
            C = np.zeros(Nx - 1)
            F = np.zeros(Nx - 1)

            for i in range(1, Nx):
                A[i-1] = -a * tau / hx**2
                B[i-1] = 1 + 2 * a * tau / hx**2
                C[i-1] = -a * tau / hx**2
                F[i-1] = U[i, j]

            F[0]  += -A[0]  * bc_left(y[j], t_next)
            F[-1] += -C[-1] * bc_right(y[j], t_next)

            U_half[1:Nx, j] = solve_tridiagonal(A, B, C, F)

        # Границы
        for j in range(Ny + 1):
            U_half[0,  j] = bc_left(y[j], t_next)
            U_half[Nx, j] = bc_right(y[j], t_next)
        for i in range(Nx + 1):
            U_half[i, 0]  = bc_bottom(x[i], t_next)
            U_half[i, Ny] = bc_top(x[i], t_next)

        # -------- Второй дробный шаг: неявный по y --------
        for i in range(1, Nx):
            A = np.zeros(Ny - 1)
            B = np.zeros(Ny - 1)
            C = np.zeros(Ny - 1)
            F = np.zeros(Ny - 1)

            for j in range(1, Ny):
                A[j-1] = -a * tau / hy**2
                B[j-1] = 1 + 2 * a * tau / hy**2
                C[j-1] = -a * tau / hy**2
                F[j-1] = U_half[i, j]

            F[0]  += -A[0]  * bc_bottom(x[i], t_next)
            F[-1] += -C[-1] * bc_top(x[i], t_next)

            U_new[i, 1:Ny] = solve_tridiagonal(A, B, C, F)

        # Обновление границ
        for i in range(Nx + 1):
            U_new[i, 0]  = bc_bottom(x[i], t_next)
            U_new[i, Ny] = bc_top(x[i], t_next)
        for j in range(Ny + 1):
            U_new[0,  j] = bc_left(y[j], t_next)
            U_new[Nx, j] = bc_right(y[j], t_next)

        U = U_new.copy()

    return U


# =====================================================================
#                   ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =====================================================================
def build_initial(Nx, Ny):
    """Начальное условие u(x,y,0) = cos(m1*x)*cos(m2*y)."""
    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)
    U0 = np.zeros((Nx + 1, Ny + 1))
    for i in range(Nx + 1):
        for j in range(Ny + 1):
            U0[i, j] = np.cos(m1 * x[i]) * np.cos(m2 * y[j])
    return U0


def build_exact(Nx, Ny, t_final):
    """Точное решение на сетке в момент t_final."""
    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)
    Ue = np.zeros((Nx + 1, Ny + 1))
    for i in range(Nx + 1):
        for j in range(Ny + 1):
            Ue[i, j] = U_exact(x[i], y[j], t_final)
    return Ue


def compute_error(U_num, t_final):
    """Максимальная погрешность на сетке."""
    Nx, Ny = U_num.shape[0] - 1, U_num.shape[1] - 1
    U_ex = build_exact(Nx, Ny, t_final)
    return np.max(np.abs(U_num - U_ex))


# =====================================================================
#                    ОСНОВНОЙ РАСЧЁТ И ВИЗУАЛИЗАЦИЯ
# =====================================================================
def main():
    Nx, Ny = 50, 50
    hx = Lx / Nx
    hy = Ly / Ny
    tau = 0.001

    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)

    print("=" * 65)
    print(" Лабораторная работа N4")
    print(" Решение двумерного параболического уравнения")
    print("=" * 65)
    print(f" Параметры: a = {a}, m1 = {m1}, m2 = {m2}, T = {T}")
    print(f" Сетка: Nx = {Nx}, Ny = {Ny}, hx = {hx:.4f}, hy = {hy:.4f}, tau = {tau}")
    print("-" * 65)

    U0 = build_initial(Nx, Ny)

    # Метод переменных направлений
    U_pr = solve_peaceman_rachford(Nx, Ny, hx, hy, tau, U0, T, a)
    err_pr = compute_error(U_pr, T)
    print(f" Схема переменных направлений (Писмена-Рекфорда):")
    print(f"     Максимальная погрешность = {err_pr:.6e}")

    # Метод дробных шагов
    U_fs = solve_fractional_steps(Nx, Ny, hx, hy, tau, U0, T, a)
    err_fs = compute_error(U_fs, T)
    print(f" Метод дробных шагов (Яненко):")
    print(f"     Максимальная погрешность = {err_fs:.6e}")
    print("-" * 65)

    # ---------------------------------------------------------------
    # Визуализация
    # ---------------------------------------------------------------
    X, Y = np.meshgrid(x, y, indexing='ij')
    U_ex = U_exact(X, Y, T)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    im0 = axes[0, 0].contourf(X, Y, U_ex, levels=20, cmap='viridis')
    axes[0, 0].set_title('Аналитическое решение')
    axes[0, 0].set_xlabel('x'); axes[0, 0].set_ylabel('y')
    plt.colorbar(im0, ax=axes[0, 0])

    im1 = axes[0, 1].contourf(X, Y, U_pr, levels=20, cmap='viridis')
    axes[0, 1].set_title('Схема переменных направлений')
    axes[0, 1].set_xlabel('x'); axes[0, 1].set_ylabel('y')
    plt.colorbar(im1, ax=axes[0, 1])

    im2 = axes[0, 2].contourf(X, Y, U_fs, levels=20, cmap='viridis')
    axes[0, 2].set_title('Метод дробных шагов')
    axes[0, 2].set_xlabel('x'); axes[0, 2].set_ylabel('y')
    plt.colorbar(im2, ax=axes[0, 2])

    im3 = axes[1, 0].contourf(X, Y, np.abs(U_pr - U_ex), levels=20, cmap='hot')
    axes[1, 0].set_title('Погрешность (перем. направления)')
    axes[1, 0].set_xlabel('x'); axes[1, 0].set_ylabel('y')
    plt.colorbar(im3, ax=axes[1, 0])

    im4 = axes[1, 1].contourf(X, Y, np.abs(U_fs - U_ex), levels=20, cmap='hot')
    axes[1, 1].set_title('Погрешность (дробные шаги)')
    axes[1, 1].set_xlabel('x'); axes[1, 1].set_ylabel('y')
    plt.colorbar(im4, ax=axes[1, 1])

    j_mid = Ny // 2
    axes[1, 2].plot(x, U_ex[:, j_mid],  'k-',  label='Аналитическое',      linewidth=2)
    axes[1, 2].plot(x, U_pr[:, j_mid],  'r--', label='Перем. направления', linewidth=2)
    axes[1, 2].plot(x, U_fs[:, j_mid],  'b:',  label='Дробные шаги',       linewidth=2)
    axes[1, 2].set_title(f'Сечение y = {y[j_mid]:.2f}')
    axes[1, 2].set_xlabel('x'); axes[1, 2].set_ylabel('u')
    axes[1, 2].legend()
    axes[1, 2].grid(True)

    plt.tight_layout()
    plt.savefig('lab4_results.png', dpi=150)
    plt.close()
    print(" Графики сохранены в файл 'lab4_results.png'")
    print("=" * 65)


# =====================================================================
#              ИССЛЕДОВАНИЕ СХОДИМОСТИ
# =====================================================================
def convergence_study():
    """Исследование зависимости погрешности от сеточных параметров."""
    print("\n" + "=" * 65)
    print(" Исследование зависимости погрешности от сеточных параметров")
    print("=" * 65)

    # -------- Зависимость от шага по пространству --------
    print("\n 1. Зависимость от шага по пространству (tau = 0.001):")
    print("-" * 65)
    print(f"{'Nx=Ny':>8} {'h':>10} {'Ошибка (ПР)':>16} {'Ошибка (ДШ)':>16}")
    print("-" * 65)

    tau_fixed = 0.001
    for N in [10, 20, 40, 80]:
        h = Lx / N
        U0_ = build_initial(N, N)
        U_ex_ = build_exact(N, N, T)

        U_pr_ = solve_peaceman_rachford(N, N, h, h, tau_fixed, U0_, T, a)
        U_fs_ = solve_fractional_steps(N, N, h, h, tau_fixed, U0_, T, a)

        e_pr = np.max(np.abs(U_pr_ - U_ex_))
        e_fs = np.max(np.abs(U_fs_ - U_ex_))
        print(f"{N:>8} {h:>10.5f} {e_pr:>16.6e} {e_fs:>16.6e}")

    # -------- Зависимость от шага по времени --------
    print("\n 2. Зависимость от шага по времени (Nx = Ny = 40):")
    print("-" * 65)
    print(f"{'tau':>10} {'Ошибка (ПР)':>16} {'Ошибка (ДШ)':>16}")
    print("-" * 65)

    N_fixed = 40
    h_f = Lx / N_fixed
    U0_f = build_initial(N_fixed, N_fixed)
    U_ex_f = build_exact(N_fixed, N_fixed, T)

    for tau_ in [0.01, 0.005, 0.002, 0.001, 0.0005]:
        U_pr_t = solve_peaceman_rachford(N_fixed, N_fixed, h_f, h_f, tau_, U0_f, T, a)
        U_fs_t = solve_fractional_steps(N_fixed, N_fixed, h_f, h_f, tau_, U0_f, T, a)

        e_pr_t = np.max(np.abs(U_pr_t - U_ex_f))
        e_fs_t = np.max(np.abs(U_fs_t - U_ex_f))
        print(f"{tau_:>10.5f} {e_pr_t:>16.6e} {e_fs_t:>16.6e}")

    print("=" * 65)


# =====================================================================
#                              ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    main()
    convergence_study()