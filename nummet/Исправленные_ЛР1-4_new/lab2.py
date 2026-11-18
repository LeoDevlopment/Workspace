# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА № 2
Одномерное волновое уравнение. Вариант 1 из задания.

    u_tt = a^2 * u_xx,      0 < x < pi, 0 < t <= T
    u(0,t) = -sin(a*t)
    u(pi,t) =  sin(a*t)
    u(x,0) = sin(x)
    u_t(x,0) = -a*cos(x)

Точное решение: U(x,t) = sin(x-a*t).

Выполняются явная схема (схема "крест") и неявная схема.
Второе начальное условие аппроксимируется первым и вторым порядком.
Для варианта 1 в самом задании указаны значения u на концах отрезка,
то есть условия Дирихле. Поэтому в этой программе не вводятся фиктивные
варианты Неймана: используются именно граничные условия варианта 1.
"""

# ============================================================================
# БЛОК 1. ИМПОРТ БИБЛИОТЕК И ПАРАМЕТРЫ ЗАДАЧИ
# ============================================================================
import numpy as np
import matplotlib.pyplot as plt

A_WAVE = 1.0
L = np.pi
T_FINAL = 1.0


# ============================================================================
# БЛОК 2. АНАЛИТИЧЕСКОЕ РЕШЕНИЕ И ГРАНИЧНЫЕ ЗНАЧЕНИЯ
# ============================================================================
def exact_solution(x, t, a=A_WAVE):
    """Точное решение, приведённое в варианте 1 задания."""
    return np.sin(x - a * t)


def left_boundary(t, a=A_WAVE):
    """Значение u(0,t) = -sin(a*t)."""
    return -np.sin(a * t)


def right_boundary(t, a=A_WAVE):
    """Значение u(pi,t) = sin(a*t)."""
    return np.sin(a * t)


# ============================================================================
# БЛОК 3. РЕШЕНИЕ ТРЁХДИАГОНАЛЬНОЙ СИСТЕМЫ МЕТОДОМ ПРОГОНКИ
# ============================================================================
def solve_tridiagonal(lower, diagonal, upper, rhs):
    """
    Решить трёхдиагональную систему методом прогонки (алгоритм Томаса).

    Система имеет вид:
      lower[i]*y[i-1] + diagonal[i]*y[i] + upper[i]*y[i+1] = rhs[i].

    Возвращается вектор y. Первый элемент нижней диагонали и последний
    элемент верхней диагонали не используются.
    """
    n = len(diagonal)
    if n == 0 or not (len(lower) == len(upper) == len(rhs) == n):
        raise ValueError("Неверные размеры трёхдиагональной системы.")

    # Прямой ход: выражаем y[i] через y[i+1].
    alpha = np.zeros(n, dtype=float)
    beta = np.zeros(n, dtype=float)
    denominator = diagonal[0]
    if abs(denominator) < 1e-14:
        raise ZeroDivisionError("Нулевой знаменатель в методе прогонки.")
    alpha[0] = -upper[0] / denominator if n > 1 else 0.0
    beta[0] = rhs[0] / denominator

    for i in range(1, n):
        denominator = diagonal[i] + lower[i] * alpha[i - 1]
        if abs(denominator) < 1e-14:
            raise ZeroDivisionError("Нулевой знаменатель в методе прогонки.")
        alpha[i] = -upper[i] / denominator if i < n - 1 else 0.0
        beta[i] = (rhs[i] - lower[i] * beta[i - 1]) / denominator

    # Обратный ход: восстанавливаем решение справа налево.
    solution = np.zeros(n, dtype=float)
    solution[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        solution[i] = alpha[i] * solution[i + 1] + beta[i]

    return solution


# ============================================================================
# БЛОК 4. ПОДГОТОВКА СЕТКИ И ПЕРВОГО ВРЕМЕННОГО СЛОЯ
# ============================================================================
def build_grid_and_initial_layer(a, length, final_time, nx, nt, init_order):
    """
    Создать сетки x и t и заполнить первые два временных слоя.

    Первое начальное условие задаёт u(x,0).
    Второе начальное условие задаёт скорость изменения решения u_t(x,0).

    Для слоя t=tau используем разложение Тейлора:
      u(x,tau) = u(x,0) + tau*u_t(x,0)
                 + tau^2/2*u_tt(x,0) + ...
    А из волнового уравнения u_tt(x,0)=a^2*u_xx(x,0).
    """
    if nx < 2 or nt < 1:
        raise ValueError("Требуется nx >= 2 и nt >= 1.")
    if init_order not in (1, 2):
        raise ValueError("init_order должен быть равен 1 или 2.")

    h = length / nx
    tau = final_time / nt
    x = np.linspace(0.0, length, nx + 1)
    t = np.linspace(0.0, final_time, nt + 1)

    u = np.zeros((nt + 1, nx + 1), dtype=float)
    u0 = np.sin(x)
    ut0 = -a * np.cos(x)
    u[0, :] = u0

    # Первый порядок: u^1 = u^0 + tau*u_t(x,0).
    u[1, 1:nx] = u0[1:nx] + tau * ut0[1:nx]

    if init_order == 2:
        # Второй порядок: добавляем tau^2/2 * u_tt(x,0).
        # Здесь u_xx(x,0) = -sin(x), поэтому u_tt=-a^2*sin(x).
        u[1, 1:nx] += 0.5 * tau**2 * (-a**2 * np.sin(x[1:nx]))

    # На первом слое границы задаются непосредственно из варианта 1.
    u[1, 0] = left_boundary(t[1], a)
    u[1, nx] = right_boundary(t[1], a)

    return x, t, u, h, tau


# ============================================================================
# БЛОК 5. ОСНОВНОЙ РЕШАТЕЛЬ ВОЛНОВОГО УРАВНЕНИЯ
# ============================================================================
def solve_hyperbolic(a=A_WAVE, length=L, final_time=T_FINAL,
                     nx=50, nt=50, scheme="explicit", init_order=2):
    """
    Решить волновое уравнение выбранной схемой.

    scheme='explicit' - явная схема "крест";
    scheme='implicit' - неявная схема с методом прогонки;
    init_order=1 или 2 - порядок аппроксимации второго начального условия.

    Возвращает x, t, u, где u[n,i] - решение в узле x[i] в момент t[n].
    """
    if scheme not in ("explicit", "implicit"):
        raise ValueError("scheme должен быть 'explicit' или 'implicit'.")

    x, t, u, h, tau = build_grid_and_initial_layer(
        a, length, final_time, nx, nt, init_order
    )

    # Число Куранта: r = a*tau/h.
    # Для явной схемы одномерного волнового уравнения нужно r <= 1.
    r = a * tau / h
    if scheme == "explicit" and r > 1.0 + 1e-12:
        raise ValueError(
            f"Нарушено условие устойчивости явной схемы: r={r:.5f}>1. "
            "Увеличьте nt или уменьшите nx."
        )
    r2 = r**2

    # Идём от известной пары слоёв n-1 и n к слою n+1.
    for n in range(1, nt):
        t_new = t[n + 1]

        if scheme == "explicit":
            # ------------------------------------------------------------
            # ЯВНАЯ СХЕМА "КРЕСТ"
            # u_i^(n+1) = 2u_i^n-u_i^(n-1)
            #             + r^2*(u_(i+1)^n-2u_i^n+u_(i-1)^n).
            # ------------------------------------------------------------
            u[n + 1, 1:nx] = (
                2.0 * u[n, 1:nx] - u[n - 1, 1:nx]
                + r2 * (u[n, 2:nx + 1] - 2.0 * u[n, 1:nx] + u[n, 0:nx - 1])
            )

            # Условия Дирихле на новом временном слое.
            u[n + 1, 0] = left_boundary(t_new, a)
            u[n + 1, nx] = right_boundary(t_new, a)

        else:
            # ------------------------------------------------------------
            # НЕЯВНАЯ СХЕМА
            # -r^2*u_(i-1)^(n+1) + (1+2r^2)*u_i^(n+1)
            # -r^2*u_(i+1)^(n+1) = 2u_i^n-u_i^(n-1).
            # Неизвестные нового слоя связаны в трёхдиагональную систему.
            # ------------------------------------------------------------
            number_of_unknowns = nx - 1
            lower = np.full(number_of_unknowns, -r2, dtype=float)
            diagonal = np.full(number_of_unknowns, 1.0 + 2.0 * r2, dtype=float)
            upper = np.full(number_of_unknowns, -r2, dtype=float)
            rhs = 2.0 * u[n, 1:nx] - u[n - 1, 1:nx]

            # Переносим известные граничные значения в правую часть.
            rhs[0] += r2 * left_boundary(t_new, a)
            rhs[-1] += r2 * right_boundary(t_new, a)

            # Решаем систему для всех внутренних узлов.
            u[n + 1, 1:nx] = solve_tridiagonal(lower, diagonal, upper, rhs)

            # Граничные значения заданы прямо в условии варианта 1.
            u[n + 1, 0] = left_boundary(t_new, a)
            u[n + 1, nx] = right_boundary(t_new, a)

    return x, t, u


# ============================================================================
# БЛОК 6. СРАВНЕНИЕ С АНАЛИТИЧЕСКИМ РЕШЕНИЕМ
# ============================================================================
def compute_error(x, t, u_numerical, a=A_WAVE):
    """Вернуть матрицу абсолютных ошибок |u_num-U_exact| на всей сетке."""
    exact = np.array([exact_solution(x, tn, a) for tn in t])
    return np.abs(u_numerical - exact), exact


def print_errors_at_times(t, error):
    """Показать максимальную по пространству ошибку в выбранные моменты времени."""
    print("Погрешность в выбранные моменты времени:")
    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        n = int(round(fraction * (len(t) - 1)))
        print(f"  t={t[n]:.4f}: max_x error={np.max(error[n, :]):.6e}")


# ============================================================================
# БЛОК 7. ИССЛЕДОВАНИЕ ВЛИЯНИЯ ПРОСТРАНСТВЕННОГО И ВРЕМЕННОГО ШАГОВ
# ============================================================================
def convergence_study():
    """Проверить изменение ошибки при измельчении h и tau для двух схем."""
    print("\nИсследование по пространственной сетке (второй порядок начального слоя):")
    for nx in (20, 40, 60, 80):
        # Для явной схемы выбираем nt так, чтобы число Куранта было около 0.8.
        nt = max(1, int(np.ceil(A_WAVE * T_FINAL * nx / (0.8 * L))))
        for scheme in ("explicit", "implicit"):
            x, t, u = solve_hyperbolic(nx=nx, nt=nt, scheme=scheme, init_order=2)
            error, _ = compute_error(x, t, u)
            print(f"{scheme:8s}: Nx={nx:3d}, Nt={nt:4d}, h={L/nx:.5f}, max error={np.max(error):.6e}")

    print("\nИсследование по временному шагу (Nx=50):")
    nx = 50
    for nt in (25, 50, 100, 200, 400):
        for scheme in ("explicit", "implicit"):
            x, t, u = solve_hyperbolic(nx=nx, nt=nt, scheme=scheme, init_order=2)
            error, _ = compute_error(x, t, u)
            print(f"{scheme:8s}: Nt={nt:4d}, tau={T_FINAL/nt:.5f}, max error={np.max(error):.6e}")


# ============================================================================
# БЛОК 8. ГЛАВНЫЙ ЗАПУСК: ДВЕ СХЕМЫ И ДВА ПОРЯДКА НАЧАЛЬНОГО УСЛОВИЯ
# ============================================================================
def main():
    nx, nt = 50, 50
    all_results = {}

    print("Лабораторная работа № 2. Вариант 1")
    print("Уравнение: u_tt = a^2*u_xx; точное решение: sin(x-a*t)")
    print(f"a={A_WAVE}, L=pi, T={T_FINAL}, Nx={nx}, Nt={nt}")
    print(f"Число Куранта r={A_WAVE*(T_FINAL/nt)/(L/nx):.5f}\n")

    # Проверяем обе схемы и оба способа старта временного процесса.
    for scheme in ("explicit", "implicit"):
        for init_order in (1, 2):
            x, t, u = solve_hyperbolic(
                nx=nx, nt=nt, scheme=scheme, init_order=init_order
            )
            error, exact = compute_error(x, t, u)
            all_results[(scheme, init_order)] = (x, t, u, error, exact)
            print(
                f"{scheme:8s}, порядок начального условия={init_order}: "
                f"max error={np.max(error):.6e}"
            )
            print_errors_at_times(t, error)

    # График решения при t=T для явной и неявной схемы (порядок старта 2).
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, scheme in zip(axes, ("explicit", "implicit")):
        x, t, u, error, exact = all_results[(scheme, 2)]
        ax.plot(x, u[-1, :], label="Численное", marker="o", ms=3)
        ax.plot(x, exact[-1, :], "--", label="Точное")
        ax.set_title("Явная схема" if scheme == "explicit" else "Неявная схема")
        ax.set_xlabel("x")
        ax.set_ylabel("u(x,T)")
        ax.grid(True, alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig("lab2_comparison.png", dpi=150)
    plt.show()
    # Карта изменения решения со временем для явной схемы.
    x, t, u, _, _ = all_results[("explicit", 2)]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    image = ax.imshow(u, aspect="auto", extent=[0, L, T_FINAL, 0], cmap="viridis")
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_title("Решение волнового уравнения во времени")
    fig.colorbar(image, ax=ax, label="u")
    fig.tight_layout()
    fig.savefig("lab2_space_time.png", dpi=150)
    plt.show()
    print("\nГрафики сохранены: lab2_comparison.png, lab2_space_time.png")

    return all_results


# ============================================================================
# БЛОК 9. ТОЧКА ВХОДА
# ============================================================================
if __name__ == "__main__":
    main()
    convergence_study()
