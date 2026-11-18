# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА № 4
Двумерное уравнение теплопроводности. Задача 1, вариант 1:

    u_t = a*(u_xx + u_yy),       0<x<pi, 0<y<pi, 0<t<=T
    u(0,y,t)  = cos(y)*exp(-2*a*t)
    u(pi,y,t) = -cos(y)*exp(-2*a*t)
    u(x,0,t)  = cos(x)*exp(-2*a*t)
    u(x,pi,t) = -cos(x)*exp(-2*a*t)
    u(x,y,0)  = cos(x)*cos(y)

Точное решение: U(x,y,t)=cos(x)*cos(y)*exp(-2*a*t).

Реализованы:
  1) схема переменных направлений Писмена - Рекфорда (ADI);
  2) метод дробных шагов (последовательное неявное решение по x и y).

Главное исправление по сравнению с исходником: в промежуточном слое
схемы Писмена - Рекфорда граничные значения задаются на половинном моменте
времени t_n+tau/2, а не на t_n+tau. Также приведены в порядок проверка
шагов времени, прогонка и комментарии к каждому блоку.
"""

# ============================================================================
# БЛОК 1. БИБЛИОТЕКИ И ПАРАМЕТРЫ ЗАДАЧИ
# ============================================================================
import numpy as np
import matplotlib
matplotlib.use("Agg")  # сохраняем графики в файлы без открытия окон
import matplotlib.pyplot as plt

A_DIFFUSION = 1.0
M1, M2 = 1, 1
LX, LY = np.pi, np.pi
T_FINAL = 0.1


# ============================================================================
# БЛОК 2. ТОЧНОЕ РЕШЕНИЕ И ЧЕТЫРЕ ГРАНИЧНЫХ УСЛОВИЯ
# ============================================================================
def exact_solution(x, y, t):
    """Точное решение задачи 1: cos(m1*x)*cos(m2*y)*exp(-(m1²+m2²)*a*t)."""
    return (
        np.cos(M1 * x) * np.cos(M2 * y)
        * np.exp(-(M1**2 + M2**2) * A_DIFFUSION * t)
    )


def boundary_left(y, t):
    """Значения на левой стороне x=0."""
    return np.cos(M2 * y) * np.exp(-(M1**2 + M2**2) * A_DIFFUSION * t)


def boundary_right(y, t):
    """Значения на правой стороне x=pi."""
    return (-1)**M1 * np.cos(M2 * y) * np.exp(-(M1**2 + M2**2) * A_DIFFUSION * t)


def boundary_bottom(x, t):
    """Значения на нижней стороне y=0."""
    return np.cos(M1 * x) * np.exp(-(M1**2 + M2**2) * A_DIFFUSION * t)


def boundary_top(x, t):
    """Значения на верхней стороне y=pi."""
    return (-1)**M2 * np.cos(M1 * x) * np.exp(-(M1**2 + M2**2) * A_DIFFUSION * t)


def apply_all_boundaries(U, x, y, t):
    """Заполнить значения U на всех четырёх сторонах прямоугольной сетки."""
    U[0, :] = boundary_left(y, t)
    U[-1, :] = boundary_right(y, t)
    U[:, 0] = boundary_bottom(x, t)
    U[:, -1] = boundary_top(x, t)
    # В углах два граничных условия встречаются. В варианте 1 они согласованы.


# ============================================================================
# БЛОК 3. СОЗДАНИЕ СЕТКИ И ПРОВЕРКА ВРЕМЕННОГО ШАГА
# ============================================================================
def make_grid(nx, ny, tau, final_time=T_FINAL):
    """
    Создать координатные сетки и временную сетку.

    Для простоты и точного попадания в конечное время требуем, чтобы
    final_time/tau было целым числом (с небольшой погрешностью округления).
    """
    if nx < 2 or ny < 2 or tau <= 0 or final_time <= 0:
        raise ValueError("Нужно nx>=2, ny>=2, tau>0 и final_time>0.")

    steps_real = final_time / tau
    nt = int(round(steps_real))
    if nt < 1 or not np.isclose(steps_real, nt, rtol=1e-10, atol=1e-10):
        raise ValueError("Выберите tau так, чтобы final_time/tau было целым числом.")

    # Шаги и координаты по двум пространственным направлениям.
    hx = LX / nx
    hy = LY / ny
    x = np.linspace(0.0, LX, nx + 1)
    y = np.linspace(0.0, LY, ny + 1)
    t = np.linspace(0.0, final_time, nt + 1)
    return x, y, t, hx, hy, nt


# ============================================================================
# БЛОК 4. МЕТОД ПРОГОНКИ ДЛЯ ТРЁХДИАГОНАЛЬНОЙ СИСТЕМЫ
# ============================================================================
def solve_tridiagonal(lower, diagonal, upper, rhs):
    """
    Решить трёхдиагональную систему методом прогонки (алгоритм Томаса).

    На каждом шаге прямого хода уравнение преобразуется к виду:
        v[i] = alpha[i]*v[i+1] + beta[i].
    После прямого хода выполняется обратный ход справа налево.

    lower, diagonal, upper - три диагонали матрицы;
    rhs - правая часть.
    """
    n = len(rhs)
    if n == 0 or not (len(lower) == len(diagonal) == len(upper) == n):
        raise ValueError("Неверный размер трёхдиагональной системы.")

    alpha = np.zeros(n, dtype=float)
    beta = np.zeros(n, dtype=float)

    # ------------------------------------------------------------
    # Прямой ход прогонки
    # ------------------------------------------------------------
    denominator = diagonal[0]
    if abs(denominator) < 1e-14:
        raise ZeroDivisionError("Нулевой знаменатель на первом шаге прогонки.")
    alpha[0] = -upper[0] / denominator if n > 1 else 0.0
    beta[0] = rhs[0] / denominator

    for i in range(1, n):
        denominator = diagonal[i] + lower[i] * alpha[i - 1]
        if abs(denominator) < 1e-14:
            raise ZeroDivisionError(f"Нулевой знаменатель на шаге прогонки i={i}.")
        alpha[i] = -upper[i] / denominator if i < n - 1 else 0.0
        beta[i] = (rhs[i] - lower[i] * beta[i - 1]) / denominator

    # ------------------------------------------------------------
    # Обратный ход прогонки
    # ------------------------------------------------------------
    solution = np.zeros(n, dtype=float)
    solution[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        solution[i] = alpha[i] * solution[i + 1] + beta[i]

    return solution


# ============================================================================
# БЛОК 5. ВСПОМОГАТЕЛЬНОЕ РЕШЕНИЕ СИСТЕМ ВДОЛЬ ОДНОЙ КООРДИНАТЫ
# ============================================================================
def solve_x_line(rhs_line, y_value, t_boundary, hx, nx, coefficient):
    """
    Решить одну строку неизвестных по x при фиксированном y.

    Уравнение имеет вид:
      -q*u_(i-1) + (1+2q)*u_i - q*u_(i+1) = rhs_i.

    Граничные значения по x известны и переносятся в правую часть.
    coefficient обычно равен a*tau/(2*hx^2) для схемы Писмена - Рекфорда
    или a*tau/hx^2 для метода дробных шагов.
    """
    q = coefficient
    lower = np.full(nx - 1, -q, dtype=float)
    diagonal = np.full(nx - 1, 1.0 + 2.0 * q, dtype=float)
    upper = np.full(nx - 1, -q, dtype=float)
    rhs = np.asarray(rhs_line, dtype=float).copy()

    # Известные u(0,y,t) и u(pi,y,t) переносятся в правую часть.
    left_value = boundary_left(y_value, t_boundary)
    right_value = boundary_right(y_value, t_boundary)
    rhs[0] -= lower[0] * left_value
    rhs[-1] -= upper[-1] * right_value

    return solve_tridiagonal(lower, diagonal, upper, rhs)


def solve_y_line(rhs_line, x_value, t_boundary, hy, ny, coefficient):
    """
    Решить один столбец неизвестных по y при фиксированном x.

    Граничные значения снизу и сверху задаются условиями варианта 1.
    """
    q = coefficient
    lower = np.full(ny - 1, -q, dtype=float)
    diagonal = np.full(ny - 1, 1.0 + 2.0 * q, dtype=float)
    upper = np.full(ny - 1, -q, dtype=float)
    rhs = np.asarray(rhs_line, dtype=float).copy()

    bottom_value = boundary_bottom(x_value, t_boundary)
    top_value = boundary_top(x_value, t_boundary)
    rhs[0] -= lower[0] * bottom_value
    rhs[-1] -= upper[-1] * top_value

    return solve_tridiagonal(lower, diagonal, upper, rhs)


# ============================================================================
# БЛОК 6. СХЕМА ПЕРЕМЕННЫХ НАПРАВЛЕНИЙ ПИСМЕНА - РЕКФОРДА (ADI)
# ============================================================================
def solve_peaceman_rachford(nx, ny, tau, initial=None, final_time=T_FINAL, return_history=False):
    """
    Решить двумерное уравнение схемой переменных направлений Писмена - Рекфорда.

    Каждый полный временной шаг состоит из двух полушагов:
      1) неявное решение по x и явное по y;
      2) явное решение по x и неявное по y.

    В промежуточном слое границы должны соответствовать t_n+tau/2.
    В исходном коде они ставились на t_n+tau; это исправлено.
    """
    x, y, t, hx, hy, nt = make_grid(nx, ny, tau, final_time)
    X, Y = np.meshgrid(x, y, indexing="ij")

    # Начальное распределение температуры при t=0.
    if initial is None:
        U = exact_solution(X, Y, 0.0)
    else:
        U = np.asarray(initial, dtype=float).copy()
    if U.shape != (nx + 1, ny + 1):
        raise ValueError("Размер initial не совпадает с размером сетки.")
    apply_all_boundaries(U, x, y, 0.0)

    U_half = np.empty_like(U)
    U_next = np.empty_like(U)
    history = np.empty((nt + 1, nx + 1, ny + 1), dtype=float)
    history[0] = U

    # Коэффициенты половинного шага в направлениях x и y.
    qx = A_DIFFUSION * tau / (2.0 * hx**2)
    qy = A_DIFFUSION * tau / (2.0 * hy**2)

    for n in range(nt):
        t_half = 0.5 * (t[n] + t[n + 1])
        t_next = t[n + 1]

        # --------------------------------------------------------
        # Первый полушаг: (I - tau/2*A_x) U_half = (I + tau/2*A_y) U_old.
        # Для каждой фиксированной строки y решается система по x.
        # --------------------------------------------------------
        apply_all_boundaries(U_half, x, y, t_half)
        for j in range(1, ny):
            rhs = (
                U[1:nx, j]
                + qy * (U[1:nx, j + 1] - 2.0 * U[1:nx, j] + U[1:nx, j - 1])
            )
            U_half[1:nx, j] = solve_x_line(
                rhs, y[j], t_half, hx, nx, qx
            )

        # --------------------------------------------------------
        # Второй полушаг: (I - tau/2*A_y) U_next = (I + tau/2*A_x) U_half.
        # Для каждого фиксированного x решается система по y.
        # --------------------------------------------------------
        apply_all_boundaries(U_next, x, y, t_next)
        for i in range(1, nx):
            rhs = (
                U_half[i, 1:ny]
                + qx * (U_half[i + 1, 1:ny] - 2.0 * U_half[i, 1:ny] + U_half[i - 1, 1:ny])
            )
            U_next[i, 1:ny] = solve_y_line(
                rhs, x[i], t_next, hy, ny, qy
            )

        # Переходим к следующему временному шагу.
        apply_all_boundaries(U_next, x, y, t_next)
        U[:, :] = U_next
        history[n + 1] = U

    if return_history:
        return x, y, history
    return x, y, U


# ============================================================================
# БЛОК 7. МЕТОД ДРОБНЫХ ШАГОВ (ЯНЕНКО)
# ============================================================================
def solve_fractional_steps(nx, ny, tau, initial=None, final_time=T_FINAL, return_history=False):
    """
    Решить двумерное уравнение методом дробных шагов (последовательное расщепление).

    Один полный временной шаг разбивается на два последовательных действия:
      1) решается неявная задача только по x;
      2) решается неявная задача только по y.

    В отличие от схемы Писмена - Рекфорда, здесь каждый одномерный шаг
    использует полный tau. Метод расщепления такого типа имеет первый порядок
    по времени в общем случае.
    """
    x, y, t, hx, hy, nt = make_grid(nx, ny, tau, final_time)
    X, Y = np.meshgrid(x, y, indexing="ij")

    if initial is None:
        U = exact_solution(X, Y, 0.0)
    else:
        U = np.asarray(initial, dtype=float).copy()
    if U.shape != (nx + 1, ny + 1):
        raise ValueError("Размер initial не совпадает с размером сетки.")
    apply_all_boundaries(U, x, y, 0.0)

    U_half = np.empty_like(U)
    U_next = np.empty_like(U)
    history = np.empty((nt + 1, nx + 1, ny + 1), dtype=float)
    history[0] = U

    # Коэффициенты полного дробного шага.
    qx = A_DIFFUSION * tau / hx**2
    qy = A_DIFFUSION * tau / hy**2

    for n in range(nt):
        t_next = t[n + 1]

        # --------------------------------------------------------
        # Первый дробный шаг: неявное решение по x.
        # Для каждой строки y решается своя трёхдиагональная система.
        # --------------------------------------------------------
        apply_all_boundaries(U_half, x, y, t_next)
        for j in range(1, ny):
            rhs = U[1:nx, j].copy()
            U_half[1:nx, j] = solve_x_line(
                rhs, y[j], t_next, hx, nx, qx
            )

        # --------------------------------------------------------
        # Второй дробный шаг: неявное решение по y.
        # Для каждого столбца x решается своя система.
        # --------------------------------------------------------
        apply_all_boundaries(U_next, x, y, t_next)
        for i in range(1, nx):
            rhs = U_half[i, 1:ny].copy()
            U_next[i, 1:ny] = solve_y_line(
                rhs, x[i], t_next, hy, ny, qy
            )

        # Новый слой становится исходным для следующего шага.
        apply_all_boundaries(U_next, x, y, t_next)
        U[:, :] = U_next
        history[n + 1] = U

    if return_history:
        return x, y, history
    return x, y, U


# ============================================================================
# БЛОК 8. ПОСТРОЕНИЕ НАЧАЛЬНОГО И ТОЧНОГО РЕШЕНИЙ, ОШИБКА
# ============================================================================
def build_initial(nx, ny):
    """Создать начальный слой U(x,y,0)=cos(m1*x)*cos(m2*y)."""
    x = np.linspace(0.0, LX, nx + 1)
    y = np.linspace(0.0, LY, ny + 1)
    X, Y = np.meshgrid(x, y, indexing="ij")
    return exact_solution(X, Y, 0.0)


def build_exact(nx, ny, t_final):
    """Построить точное решение на всей сетке в заданный момент времени."""
    x = np.linspace(0.0, LX, nx + 1)
    y = np.linspace(0.0, LY, ny + 1)
    X, Y = np.meshgrid(x, y, indexing="ij")
    return exact_solution(X, Y, t_final)


def compute_error(numerical, t_final):
    """Вычислить максимальную и среднеквадратичную ошибку на сетке."""
    nx, ny = numerical.shape[0] - 1, numerical.shape[1] - 1
    exact = build_exact(nx, ny, t_final)
    error = np.abs(numerical - exact)
    max_error = float(np.max(error))
    rms_error = float(np.sqrt(np.mean(error**2)))
    return max_error, rms_error, error


def print_history_errors(history, tau, title):
    """Напечатать максимальную ошибку на сетке в нескольких временных слоях."""
    nx, ny = history.shape[1] - 1, history.shape[2] - 1
    print(f"Погрешность по времени ({title}):")
    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        index = int(round(fraction * (len(history) - 1)))
        time = index * tau
        exact = build_exact(nx, ny, time)
        error = np.abs(history[index] - exact)
        print(f"  t={time:.4f}: max error={np.max(error):.6e}")


# ============================================================================
# БЛОК 9. ОСНОВНОЙ РАСЧЁТ И ГРАФИКИ
# ============================================================================
def main():
    """Решить задачу двумя методами, сравнить с точным решением и сохранить графики."""
    nx = ny = 50
    tau = 0.001
    x = np.linspace(0.0, LX, nx + 1)
    y = np.linspace(0.0, LY, ny + 1)
    X, Y = np.meshgrid(x, y, indexing="ij")
    initial = build_initial(nx, ny)

    print("Лабораторная работа № 4. Задача 1, вариант 1")
    print(f"a={A_DIFFUSION}, m1={M1}, m2={M2}, T={T_FINAL}")
    print(f"Nx={nx}, Ny={ny}, hx={LX/nx:.6f}, hy={LY/ny:.6f}, tau={tau}")

    # Решение схемой переменных направлений.
    x, y, history_pr = solve_peaceman_rachford(
        nx, ny, tau, initial, return_history=True
    )
    U_pr = history_pr[-1]
    err_pr, rms_pr, error_pr = compute_error(U_pr, T_FINAL)
    print(f"Писмен - Рекфорд: max error={err_pr:.6e}, RMS error={rms_pr:.6e}")
    print_history_errors(history_pr, tau, "Писмен - Рекфорд")

    # Решение методом дробных шагов.
    x, y, history_fs = solve_fractional_steps(
        nx, ny, tau, initial, return_history=True
    )
    U_fs = history_fs[-1]
    err_fs, rms_fs, error_fs = compute_error(U_fs, T_FINAL)
    print(f"Дробные шаги:     max error={err_fs:.6e}, RMS error={rms_fs:.6e}")
    print_history_errors(history_fs, tau, "дробные шаги")

    # Аналитическое решение в момент T.
    U_exact = exact_solution(X, Y, T_FINAL)

    # ------------------------------------------------------------
    # Визуализация: точное решение, два численных решения и ошибки.
    # ------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    images = [
        (U_exact, "Аналитическое решение", "viridis"),
        (U_pr, "Схема Писмена - Рекфорда", "viridis"),
        (U_fs, "Метод дробных шагов", "viridis"),
        (error_pr, "Ошибка: Писмен - Рекфорд", "hot"),
        (error_fs, "Ошибка: дробные шаги", "hot"),
    ]
    for ax, (data, title, color_map) in zip(axes.flat[:5], images):
        image = ax.contourf(X, Y, data, levels=20, cmap=color_map)
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.colorbar(image, ax=ax)

    # Шестая панель: сравниваем сечения при y примерно равном pi/2.
    j_mid = ny // 2
    axes[1, 2].plot(x, U_exact[:, j_mid], label="Аналитическое", linewidth=2)
    axes[1, 2].plot(x, U_pr[:, j_mid], "--", label="Писмен - Рекфорд")
    axes[1, 2].plot(x, U_fs[:, j_mid], ":", label="Дробные шаги")
    axes[1, 2].set_title(f"Сечение y={y[j_mid]:.3f}")
    axes[1, 2].set_xlabel("x")
    axes[1, 2].set_ylabel("u")
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].legend()

    fig.tight_layout()
    fig.savefig("lab4_results.png", dpi=150)
    plt.show()
    print("График сохранён: lab4_results.png")


# ============================================================================
# БЛОК 10. ИССЛЕДОВАНИЕ ЗАВИСИМОСТИ ОШИБКИ ОТ hx, hy И tau
# ============================================================================
def convergence_study():
    """Сравнить ошибки обоих методов при изменении пространственного и временного шага."""
    tau_fixed = 0.001
    print("\nЗависимость ошибки от пространственной сетки (tau=0.001):")
    print(f"{'N':>6} {'h':>12} {'Ошибка PR':>16} {'Ошибка дробных шагов':>22}")
    for n in (10, 20, 40, 80):
        initial = build_initial(n, n)
        _, _, U_pr = solve_peaceman_rachford(n, n, tau_fixed, initial)
        _, _, U_fs = solve_fractional_steps(n, n, tau_fixed, initial)
        e_pr, _, _ = compute_error(U_pr, T_FINAL)
        e_fs, _, _ = compute_error(U_fs, T_FINAL)
        print(f"{n:6d} {LX/n:12.6f} {e_pr:16.6e} {e_fs:22.6e}")

    print("\nЗависимость ошибки от временного шага (Nx=Ny=40):")
    n = 40
    initial = build_initial(n, n)
    print(f"{'tau':>10} {'Ошибка PR':>16} {'Ошибка дробных шагов':>22}")
    for tau in (0.01, 0.005, 0.002, 0.001, 0.0005):
        _, _, U_pr = solve_peaceman_rachford(n, n, tau, initial)
        _, _, U_fs = solve_fractional_steps(n, n, tau, initial)
        e_pr, _, _ = compute_error(U_pr, T_FINAL)
        e_fs, _, _ = compute_error(U_fs, T_FINAL)
        print(f"{tau:10.5f} {e_pr:16.6e} {e_fs:22.6e}")


# ============================================================================
# БЛОК 11. ТОЧКА ВХОДА В ПРОГРАММУ
# ============================================================================
if __name__ == "__main__":
    main()
    convergence_study()
