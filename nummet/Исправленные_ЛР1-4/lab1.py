# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА № 1
Одномерное уравнение теплопроводности.
Вариант 4 из задания:

    u_t = a * u_xx,       0 < x < pi, 0 < t <= T
    u_x(0,t) = exp(-a*t)
    u_x(pi,t) = -exp(-a*t)
    u(x,0) = sin(x)

Точное решение: U(x,t) = exp(-a*t) * sin(x).

В программе сравниваются:
  1) явная конечно-разностная схема;
  2) неявная конечно-разностная схема;
  3) схема Кранка - Николсона.

Для каждой схемы проверяются три варианта аппроксимации производных
на границах. Комментарии поясняют как назначение блоков, так и смысл формул.
"""

# ============================================================================
# БЛОК 1. БИБЛИОТЕКИ И ПАРАМЕТРЫ ИСХОДНОЙ ЗАДАЧИ
# ============================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded

A_DIFFUSION = 1.0       # коэффициент a в уравнении теплопроводности
L = np.pi               # длина отрезка по x
T_FINAL = 1.0           # конечный момент времени


# ============================================================================
# БЛОК 2. ТОЧНОЕ РЕШЕНИЕ И ГРАНИЧНЫЕ УСЛОВИЯ
# ============================================================================
def exact_solution(x, t):
    """Вернуть точное значение U(x,t) = exp(-a*t)*sin(x)."""
    return np.exp(-A_DIFFUSION * t) * np.sin(x)


def left_derivative(t):
    """Значение производной u_x(0,t), заданное в условии задачи."""
    return np.exp(-A_DIFFUSION * t)


def right_derivative(t):
    """Значение производной u_x(L,t), заданное в условии задачи."""
    return -np.exp(-A_DIFFUSION * t)


def validate_boundary_type(bc_type):
    """Проверить название способа аппроксимации граничных условий."""
    allowed = {"two_point_first", "three_point_second", "two_point_second"}
    if bc_type not in allowed:
        raise ValueError(f"Неизвестный тип граничного условия: {bc_type}. Допустимо: {sorted(allowed)}")


# ============================================================================
# БЛОК 3. РЕШЕНИЕ ТРЁХДИАГОНАЛЬНОЙ СИСТЕМЫ
# ============================================================================
def solve_tridiagonal(lower, diagonal, upper, rhs):
    """
    Решить систему с трёхдиагональной матрицей.

    lower   - нижняя диагональ;
    diagonal- главная диагональ;
    upper   - верхняя диагональ;
    rhs     - правая часть.

    Используется solve_banded из SciPy. Это готовая реализация решения
    ленточной системы; в этой лабораторной она заменяет ручную прогонку.
    Первый элемент lower и последний элемент upper не используются.
    """
    n = len(diagonal)
    if not (len(lower) == len(upper) == len(rhs) == n):
        raise ValueError("Все диагонали и правая часть должны иметь одинаковую длину.")

    # Формат SciPy: строка 0 - верхняя диагональ,
    # строка 1 - главная, строка 2 - нижняя.
    banded = np.zeros((3, n), dtype=float)
    if n > 1:
        banded[0, 1:] = upper[:-1]
        banded[2, :-1] = lower[1:]
    banded[1, :] = diagonal

    return solve_banded((1, 1), banded, rhs)


# ============================================================================
# БЛОК 4. ОБЩАЯ ФУНКЦИЯ ДЛЯ ВЫЧИСЛЕНИЯ ГРАНИЧНЫХ ЗНАЧЕНИЙ
# ============================================================================
def set_boundary_values(u_new, u_old, h, tau, t_new, bc_type):
    """
    Заполнить два граничных узла нового временного слоя.

    u_new - слой, на котором уже рассчитаны внутренние узлы;
    u_old - предыдущий временной слой;
    h     - шаг по пространству;
    tau   - шаг по времени;
    t_new - момент времени нового слоя.

    Важно: справа используется u_N = u_(N-1) + h*g_right.
    Знак именно ПЛЮС, потому что производная задана как
    (u_N - u_(N-1))/h = g_right.
    """
    validate_boundary_type(bc_type)
    g_l = left_derivative(t_new)
    g_r = right_derivative(t_new)
    n = len(u_new) - 1

    if bc_type == "two_point_first":
        # Односторонняя разность первого порядка.
        u_new[0] = u_new[1] - h * g_l
        u_new[n] = u_new[n - 1] + h * g_r

    elif bc_type == "three_point_second":
        # Односторонняя трёхточечная формула второго порядка.
        if n < 3:
            raise ValueError("Для трёхточечной формулы требуется Nx >= 3.")
        u_new[0] = (4.0 * u_new[1] - u_new[2] - 2.0 * h * g_l) / 3.0
        u_new[n] = (4.0 * u_new[n - 1] - u_new[n - 2] + 2.0 * h * g_r) / 3.0

    elif bc_type == "two_point_second":
        # Двухточечная формула с поправкой через u_t = a*u_xx.
        # c появляется при замене u_t разностью (u_boundary_new-u_boundary_old)/tau.
        c = h**2 / (2.0 * A_DIFFUSION * tau)
        u_new[0] = (u_new[1] - h * g_l + c * u_old[0]) / (1.0 + c)
        u_new[n] = (u_new[n - 1] + h * g_r + c * u_old[n]) / (1.0 + c)


# ============================================================================
# БЛОК 5. ПОДСТАНОВКА ГРАНИЧНЫХ УСЛОВИЙ В ТРЁХДИАГОНАЛЬНУЮ СИСТЕМУ
# ============================================================================
def apply_boundary_to_system(lower, diagonal, upper, rhs,
                             boundary_factor, h, tau, t_new,
                             bc_type, u_old):
    """
    Учесть граничные условия в первой и последней строках СЛАУ.

    До этой функции неизвестными являются только внутренние значения
    u_1, ..., u_(N-1). Граничные значения u_0 и u_N выражаются через
    внутренние узлы и переносятся в коэффициенты матрицы/правую часть.

    boundary_factor - коэффициент s перед соседним значением в уравнении:
        s = a*tau/h^2 для неявной схемы;
        s = a*tau/(2*h^2) для схемы Кранка - Николсона.
    """
    validate_boundary_type(bc_type)
    s = boundary_factor
    g_l = left_derivative(t_new)
    g_r = right_derivative(t_new)
    n = len(diagonal)

    if n == 0:
        raise ValueError("Сетка должна содержать хотя бы один внутренний узел.")

    if bc_type == "two_point_first":
        # u_0 = u_1 - h*g_l; u_N = u_(N-1) + h*g_r.
        # После подстановки крайние элементы главной диагонали становятся 1+s.
        diagonal[0] -= s
        rhs[0] -= s * h * g_l
        diagonal[-1] -= s
        rhs[-1] += s * h * g_r

    elif bc_type == "three_point_second":
        # Левая граница: u_0=(4*u_1-u_2-2*h*g_l)/3.
        # Правая: u_N=(4*u_(N-1)-u_(N-2)+2*h*g_r)/3.
        if n < 2:
            raise ValueError("Для трёхточечной формулы требуется Nx >= 3.")
        diagonal[0] -= 4.0 * s / 3.0
        upper[0] += s / 3.0
        rhs[0] -= 2.0 * s * h * g_l / 3.0

        diagonal[-1] -= 4.0 * s / 3.0
        lower[-1] += s / 3.0
        rhs[-1] += 2.0 * s * h * g_r / 3.0

    elif bc_type == "two_point_second":
        # Граничная формула:
        # u_0^(n+1)=(u_1^(n+1)-h*g_l+c*u_0^n)/(1+c),
        # u_N^(n+1)=(u_(N-1)^(n+1)+h*g_r+c*u_N^n)/(1+c).
        c = h**2 / (2.0 * A_DIFFUSION * tau)
        diagonal[0] -= s / (1.0 + c)
        rhs[0] += (-s * h * g_l + s * c * u_old[0]) / (1.0 + c)

        diagonal[-1] -= s / (1.0 + c)
        rhs[-1] += (s * h * g_r + s * c * u_old[-1]) / (1.0 + c)


# ============================================================================
# БЛОК 6. ЯВНАЯ КОНЕЧНО-РАЗНОСТНАЯ СХЕМА
# ============================================================================
def explicit_scheme(Nx, Nt, bc_type="two_point_first", check_stability=True):
    """
    Решить уравнение явной схемой.

    На каждом новом временном слое внутренние точки вычисляются сразу
    по значениям предыдущего слоя. Решать систему уравнений не требуется.

    Для явной схемы обязательно условие устойчивости:
        sigma = a*tau/h**2 <= 1/2.
    """
    validate_boundary_type(bc_type)
    if Nx < 2 or Nt < 1:
        raise ValueError("Требуется Nx >= 2 и Nt >= 1.")

    h = L / Nx
    tau = T_FINAL / Nt
    x = np.linspace(0.0, L, Nx + 1)
    t = np.linspace(0.0, T_FINAL, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1), dtype=float)

    # В нулевой момент времени известно решение u(x,0)=sin(x).
    u[0, :] = np.sin(x)

    sigma = A_DIFFUSION * tau / h**2
    if check_stability and sigma > 0.5 + 1e-12:
        raise ValueError(
            f"Явная схема неустойчива при этих шагах: sigma={sigma:.5f}>0.5. "
            "Увеличьте Nt или уменьшите Nx."
        )

    # Последовательно вычисляем все временные слои.
    for n in range(Nt):
        # Сначала считаем только внутренние точки i=1,...,Nx-1.
        # Все значения справа берутся с уже известного слоя n.
        u[n + 1, 1:Nx] = (
            u[n, 1:Nx]
            + sigma * (u[n, 2:Nx + 1] - 2.0 * u[n, 1:Nx] + u[n, 0:Nx - 1])
        )

        # Затем восстанавливаем левый и правый граничные узлы.
        set_boundary_values(u[n + 1], u[n], h, tau, t[n + 1], bc_type)

    return x, t, u


# ============================================================================
# БЛОК 7. НЕЯВНАЯ КОНЕЧНО-РАЗНОСТНАЯ СХЕМА
# ============================================================================
def implicit_scheme(Nx, Nt, bc_type="two_point_first"):
    """
    Решить уравнение неявной схемой.

    На каждом временном шаге строится трёхдиагональная СЛАУ для внутренних
    узлов. Граничные условия корректно включаются в крайние строки матрицы.
    Затем система решается функцией solve_tridiagonal.
    """
    validate_boundary_type(bc_type)
    if Nx < 2 or Nt < 1:
        raise ValueError("Требуется Nx >= 2 и Nt >= 1.")

    h = L / Nx
    tau = T_FINAL / Nt
    x = np.linspace(0.0, L, Nx + 1)
    t = np.linspace(0.0, T_FINAL, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1), dtype=float)
    u[0, :] = np.sin(x)

    sigma = A_DIFFUSION * tau / h**2
    number_of_unknowns = Nx - 1

    for n in range(Nt):
        t_new = t[n + 1]

        # Коэффициенты схемы для внутренних узлов:
        # -sigma*u_(i-1)^(n+1) +(1+2*sigma)*u_i^(n+1)
        # -sigma*u_(i+1)^(n+1) = u_i^n.
        lower = np.full(number_of_unknowns, -sigma, dtype=float)
        diagonal = np.full(number_of_unknowns, 1.0 + 2.0 * sigma, dtype=float)
        upper = np.full(number_of_unknowns, -sigma, dtype=float)
        rhs = u[n, 1:Nx].copy()

        # Подставляем выбранные граничные формулы в первую и последнюю строки.
        apply_boundary_to_system(
            lower, diagonal, upper, rhs,
            sigma, h, tau, t_new, bc_type, u[n]
        )

        # Решаем систему и записываем найденные внутренние значения.
        u[n + 1, 1:Nx] = solve_tridiagonal(lower, diagonal, upper, rhs)

        # После решения СЛАУ вычисляем граничные значения нового слоя.
        set_boundary_values(u[n + 1], u[n], h, tau, t_new, bc_type)

    return x, t, u


# ============================================================================
# БЛОК 8. СХЕМА КРАНКА - НИКОЛСОНА
# ============================================================================
def crank_nicolson_scheme(Nx, Nt, bc_type="two_point_first"):
    """
    Решить уравнение схемой Кранка - Николсона.

    Пространственная вторая производная усредняется между старым и новым
    временными слоями. Схема имеет второй порядок по времени и пространству.
    На каждом шаге также решается трёхдиагональная система.
    """
    validate_boundary_type(bc_type)
    if Nx < 2 or Nt < 1:
        raise ValueError("Требуется Nx >= 2 и Nt >= 1.")

    h = L / Nx
    tau = T_FINAL / Nt
    x = np.linspace(0.0, L, Nx + 1)
    t = np.linspace(0.0, T_FINAL, Nt + 1)
    u = np.zeros((Nt + 1, Nx + 1), dtype=float)
    u[0, :] = np.sin(x)

    sigma = A_DIFFUSION * tau / (2.0 * h**2)
    number_of_unknowns = Nx - 1

    for n in range(Nt):
        t_new = t[n + 1]

        # Левая часть системы относится к новому временному слою.
        lower = np.full(number_of_unknowns, -sigma, dtype=float)
        diagonal = np.full(number_of_unknowns, 1.0 + 2.0 * sigma, dtype=float)
        upper = np.full(number_of_unknowns, -sigma, dtype=float)

        # Правая часть содержит старый слой и его вторую разность по x.
        rhs = (
            u[n, 1:Nx]
            + sigma * (u[n, 2:Nx + 1] - 2.0 * u[n, 1:Nx] + u[n, 0:Nx - 1])
        )

        # Границы на новом слое включаются в матрицу так же,
        # как в неявной схеме, но с коэффициентом sigma Кранка - Николсона.
        apply_boundary_to_system(
            lower, diagonal, upper, rhs,
            sigma, h, tau, t_new, bc_type, u[n]
        )

        # Решаем СЛАУ и заполняем новый временной слой.
        u[n + 1, 1:Nx] = solve_tridiagonal(lower, diagonal, upper, rhs)
        set_boundary_values(u[n + 1], u[n], h, tau, t_new, bc_type)

    return x, t, u


# ============================================================================
# БЛОК 9. ВЫЧИСЛЕНИЕ ПОГРЕШНОСТИ
# ============================================================================
def compute_error(x, t, numerical_solution):
    """Вернуть массив |u_num-U_exact| для всех узлов и всех временных слоёв."""
    exact = np.array([exact_solution(x, tn) for tn in t])
    return np.abs(numerical_solution - exact)


def print_time_errors(t, error, fractions=(0.0, 0.25, 0.5, 0.75, 1.0)):
    """Напечатать максимальную по x ошибку в нескольких моментах времени."""
    print("    Погрешность в выбранные моменты времени:")
    for fraction in fractions:
        index = int(round(fraction * (len(t) - 1)))
        print(f"      t={t[index]:.4f}: max_x |u-U| = {np.max(error[index, :]):.6e}")


# ============================================================================
# БЛОК 10. ОСНОВНОЙ ЭКСПЕРИМЕНТ: 3 СХЕМЫ x 3 ГРАНИЧНЫХ АППРОКСИМАЦИИ
# ============================================================================
def run_comparison(Nx=40, Nt=400, make_plots=True):
    """Запустить девять комбинаций и вывести максимальные погрешности."""
    schemes = {
        "Явная": explicit_scheme,
        "Неявная": implicit_scheme,
        "Кранка - Николсона": crank_nicolson_scheme,
    }
    boundary_types = [
        ("two_point_first", "двухточечная, 1-й порядок"),
        ("three_point_second", "трёхточечная, 2-й порядок"),
        ("two_point_second", "двухточечная, 2-й порядок"),
    ]

    print("Лабораторная работа № 1. Вариант 4")
    print(f"a={A_DIFFUSION}, L=pi, T={T_FINAL}, Nx={Nx}, Nt={Nt}")
    print(f"h={L/Nx:.6f}, tau={T_FINAL/Nt:.6f}, sigma_explicit={A_DIFFUSION*(T_FINAL/Nt)/(L/Nx)**2:.6f}")
    print("Важно: для явной схемы sigma должно быть не больше 0.5.\n")

    results = {}
    for scheme_name, solver in schemes.items():
        for bc_code, bc_name in boundary_types:
            x, t, u = solver(Nx, Nt, bc_code)
            error = compute_error(x, t, u)
            max_error = float(np.max(error))
            results[(scheme_name, bc_code)] = {
                "x": x, "t": t, "u": u, "error": error,
                "max_error": max_error,
            }
            print(f"{scheme_name:22s} | {bc_name:32s} | max error = {max_error:.6e}")
            print_time_errors(t, error)

    # Графики: сравним три схемы при одном варианте границы.
    if make_plots:
        bc_code = "three_point_second"
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        for ax, (scheme_name, _) in zip(axes, schemes.items()):
            item = results[(scheme_name, bc_code)]
            ax.plot(item["x"], item["u"][-1, :], "o-", ms=3, label="Численное")
            ax.plot(item["x"], exact_solution(item["x"], T_FINAL), "--", label="Точное")
            ax.set_title(scheme_name)
            ax.set_xlabel("x")
            ax.set_ylabel("u(x,T)")
            ax.grid(True, alpha=0.3)
            ax.legend()
        fig.suptitle("Сравнение схем при трёхточечной аппроксимации границ")
        fig.tight_layout()
        fig.savefig("lab1_comparison.png", dpi=150)
        plt.close(fig)

        # График погрешности на последнем временном слое для той же границы.
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for scheme_name in schemes:
            item = results[(scheme_name, bc_code)]
            ax.semilogy(item["x"], np.maximum(item["error"][-1, :], 1e-16), label=scheme_name)
        ax.set_xlabel("x")
        ax.set_ylabel("Абсолютная ошибка при t=T")
        ax.set_title("Погрешность численных схем")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig("lab1_error.png", dpi=150)
        plt.close(fig)
        print("\nГрафики сохранены: lab1_comparison.png, lab1_error.png")

    return results


# ============================================================================
# БЛОК 11. ИССЛЕДОВАНИЕ ВЛИЯНИЯ ПРОСТРАНСТВЕННОГО И ВРЕМЕННОГО ШАГОВ
# ============================================================================
def convergence_study():
    """Оценить, как меняется ошибка схемы Кранка - Николсона при измельчении сетки."""
    bc_type = "three_point_second"

    print("\nЗависимость ошибки от пространственного шага (tau примерно фиксирован):")
    for nx in (10, 20, 40, 80):
        nt = 1000
        x, t, u = crank_nicolson_scheme(nx, nt, bc_type)
        error = compute_error(x, t, u)
        print(f"Nx={nx:3d}, h={L/nx:.6f}, max error={np.max(error):.6e}")

    print("\nЗависимость ошибки от временного шага (Nx=100):")
    nx = 100
    for nt in (50, 100, 200, 400, 800):
        x, t, u = crank_nicolson_scheme(nx, nt, bc_type)
        error = compute_error(x, t, u)
        print(f"Nt={nt:4d}, tau={T_FINAL/nt:.6f}, max error={np.max(error):.6e}")


# ============================================================================
# БЛОК 12. ТОЧКА ВХОДА В ПРОГРАММУ
# ============================================================================
if __name__ == "__main__":
    # Nx=40, Nt=400 выбраны так, чтобы явная схема удовлетворяла sigma <= 0.5.
    run_comparison(Nx=40, Nt=400, make_plots=True)
    convergence_study()
