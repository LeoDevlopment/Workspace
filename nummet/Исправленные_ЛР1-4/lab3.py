# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА № 3
Решение краевой задачи для эллиптического уравнения.
Вариант 1 из задания:

    u_xx + u_yy = 0,       0 < x < 1, 0 < y < 1
    u(0,y) = y
    u(1,y) = 1+y
    u(x,0) = x
    u(x,1) = 1+x

Точное решение: U(x,y)=x+y.

Дискретная задача решается тремя итерационными методами:
  1) простые итерации (Якоби / Либмана);
  2) метод Зейделя;
  3) метод верхней релаксации (SOR).

Важное исправление по сравнению с исходником: метод Якоби теперь действительно
использует только значения предыдущей итерации. В исходном коде массив
перезаписывался сразу, поэтому "jacobi" фактически работал как метод Зейделя.
Также добавлена корректная формула для прямоугольной сетки hx != hy.
"""

# ============================================================================
# БЛОК 1. БИБЛИОТЕКИ И НАСТРОЙКИ ЗАДАЧИ
# ============================================================================
import numpy as np
import matplotlib.pyplot as plt

X_LEFT, X_RIGHT = 0.0, 1.0
Y_BOTTOM, Y_TOP = 0.0, 1.0


# ============================================================================
# БЛОК 2. ТОЧНОЕ РЕШЕНИЕ И ГРАНИЧНЫЕ УСЛОВИЯ
# ============================================================================
def exact_solution(X, Y):
    """Точное решение варианта 1: U(x,y)=x+y."""
    return X + Y


def apply_boundary_conditions(u, x, y):
    """
    Записать значения функции на четырёх сторонах квадрата.

    Внутри массива u[i,j]:
      i отвечает за координату x;
      j отвечает за координату y.
    """
    u[0, :] = y                    # левая сторона: u(0,y)=y
    u[-1, :] = 1.0 + y             # правая сторона: u(1,y)=1+y
    u[:, 0] = x                    # нижняя сторона: u(x,0)=x
    u[:, -1] = 1.0 + x             # верхняя сторона: u(x,1)=1+x

    # В углах два граничных условия должны давать одно и то же число.
    # Для варианта 1 они согласованы, поэтому порядок присваивания не меняет ответ.


# ============================================================================
# БЛОК 3. ФОРМУЛА ДЛЯ ОДНОГО ВНУТРЕННЕГО УЗЛА
# ============================================================================
def laplace_update(u, i, j, hx, hy):
    """
    Вычислить новое значение в узле (i,j) из пятиузловой разностной схемы.

    При hx=hy это обычное среднее четырёх соседей.
    При hx != hy соседние значения взвешиваются с учётом разных шагов.

    Формула:
      u[i,j] = ((u[i-1,j]+u[i+1,j])/hx^2
              + (u[i,j-1]+u[i,j+1])/hy^2)
               / (2/hx^2 + 2/hy^2).
    """
    wx = 1.0 / hx**2
    wy = 1.0 / hy**2
    return (
        wx * (u[i - 1, j] + u[i + 1, j])
        + wy * (u[i, j - 1] + u[i, j + 1])
    ) / (2.0 * (wx + wy))


# ============================================================================
# БЛОК 4. ОСНОВНОЙ ИТЕРАЦИОННЫЙ РЕШАТЕЛЬ
# ============================================================================
def solve_elliptic(nx=20, ny=20, tol=1e-8, max_iter=100000,
                   method="sor", omega=None):
    """
    Решить уравнение Лапласа одним из трёх итерационных методов.

    nx, ny   - количество отрезков сетки по x и y;
    tol      - остановка, когда максимальное изменение за итерацию меньше tol;
    max_iter - максимальное количество итераций;
    method   - 'jacobi', 'seidel' или 'sor';
    omega    - коэффициент релаксации для SOR (0 < omega < 2).

    Возвращаются координатные сетки, численное и точное решения,
    число итераций и история максимальных изменений.
    """
    if nx < 2 or ny < 2:
        raise ValueError("Для внутреннего узла требуется nx >= 2 и ny >= 2.")
    if tol <= 0 or max_iter < 1:
        raise ValueError("tol должен быть положительным, max_iter >= 1.")
    if method not in ("jacobi", "seidel", "sor"):
        raise ValueError("method должен быть 'jacobi', 'seidel' или 'sor'.")

    # ------------------------------------------------------------
    # 4.1. Построение равномерной сетки
    # ------------------------------------------------------------
    x = np.linspace(X_LEFT, X_RIGHT, nx + 1)
    y = np.linspace(Y_BOTTOM, Y_TOP, ny + 1)
    hx = (X_RIGHT - X_LEFT) / nx
    hy = (Y_TOP - Y_BOTTOM) / ny
    X, Y = np.meshgrid(x, y, indexing="ij")

    # ------------------------------------------------------------
    # 4.2. Начальное приближение и граничные значения
    # ------------------------------------------------------------
    u = np.zeros((nx + 1, ny + 1), dtype=float)
    apply_boundary_conditions(u, x, y)
    U_exact = exact_solution(X, Y)

    # ------------------------------------------------------------
    # 4.3. Подбор параметра релаксации для метода SOR
    # ------------------------------------------------------------
    if method == "sor":
        if omega is None:
            # Оценка оптимального omega для прямоугольной равномерной сетки.
            # Для квадратной сетки nx=ny=N получается классическая формула
            # omega=2/(1+sin(pi/N)).
            wx = 1.0 / hx**2
            wy = 1.0 / hy**2
            rho_j = (
                wx * np.cos(np.pi / nx) + wy * np.cos(np.pi / ny)
            ) / (wx + wy)
            omega = min(1.999999, 2.0 / (1.0 + np.sqrt(max(0.0, 1.0 - rho_j**2))))
        if not (0.0 < omega < 2.0):
            raise ValueError("Для SOR необходимо 0 < omega < 2.")
    else:
        omega = 1.0

    # ------------------------------------------------------------
    # 4.4. Главный итерационный цикл
    # ------------------------------------------------------------
    changes = []
    converged = False

    for iteration in range(1, max_iter + 1):
        # Сохраняем предыдущее приближение для оценки изменения.
        old = u.copy()

        if method == "jacobi":
            # МЕТОД ЯКОБИ:
            # каждое новое значение считается только по массиву old.
            # Ни одно значение текущей итерации не используется раньше времени.
            new = old.copy()
            for i in range(1, nx):
                for j in range(1, ny):
                    new[i, j] = laplace_update(old, i, j, hx, hy)
            u = new

        elif method == "seidel":
            # МЕТОД ЗЕЙДЕЛЯ:
            # обновляем массив u прямо во время обхода сетки.
            # Поэтому часть соседей уже относится к новой итерации,
            # а часть - ещё к старой. Это ускоряет сходимость по сравнению с Якоби.
            for i in range(1, nx):
                for j in range(1, ny):
                    u[i, j] = laplace_update(u, i, j, hx, hy)

        elif method == "sor":
            # МЕТОД ВЕРХНЕЙ РЕЛАКСАЦИИ:
            # сначала вычисляем значение, как в методе Зейделя,
            # затем делаем шаг omega раз больше обычного изменения.
            for i in range(1, nx):
                for j in range(1, ny):
                    gauss_seidel_value = laplace_update(u, i, j, hx, hy)
                    u[i, j] = (
                        (1.0 - omega) * u[i, j]
                        + omega * gauss_seidel_value
                    )

        # Измеряем, насколько изменилось решение за одну итерацию.
        max_change = float(np.max(np.abs(u - old)))
        changes.append(max_change)

        # Если изменения стали меньше заданного допуска, останавливаемся.
        if max_change < tol:
            converged = True
            break

    if not converged:
        print(f"Предупреждение: {method} не достиг допуска {tol:g} за {max_iter} итераций.")

    return X, Y, u, U_exact, iteration, changes


# ============================================================================
# БЛОК 5. ОЦЕНКА ОШИБКИ ЧИСЛЕННОГО РЕШЕНИЯ
# ============================================================================
def compute_error(numerical, exact):
    """Вернуть максимальную и среднеквадратичную абсолютные ошибки."""
    error = np.abs(numerical - exact)
    max_error = float(np.max(error))
    rms_error = float(np.sqrt(np.mean(error**2)))
    return max_error, rms_error, error


# ============================================================================
# БЛОК 6. СРАВНЕНИЕ МЕТОДОВ ЯКОБИ, ЗЕЙДЕЛЯ И SOR
# ============================================================================
def compare_methods(nx=20, ny=20, tol=1e-8, make_plot=True):
    """Запустить три итерационных метода на одной и той же сетке."""
    methods = ("jacobi", "seidel", "sor")
    results = {}

    print("\nСравнение итерационных методов")
    print(f"Сетка: nx={nx}, ny={ny}; tol={tol:g}")
    for method in methods:
        X, Y, u, exact, iterations, changes = solve_elliptic(
            nx=nx, ny=ny, tol=tol, method=method
        )
        max_error, rms_error, error = compute_error(u, exact)
        results[method] = {
            "X": X, "Y": Y, "u": u, "exact": exact, "error": error,
            "iterations": iterations, "changes": changes,
            "max_error": max_error, "rms_error": rms_error,
        }
        print(
            f"{method:8s}: итераций={iterations:6d}, "
            f"max error={max_error:.3e}, RMS error={rms_error:.3e}"
        )

    # График показывает уменьшение максимального изменения от итерации к итерации.
    if make_plot:
        fig, ax = plt.subplots(figsize=(8, 5))
        for method in methods:
            ax.semilogy(results[method]["changes"], label=method)
        ax.set_xlabel("Номер итерации")
        ax.set_ylabel("Максимальное изменение решения")
        ax.set_title("Сходимость методов решения уравнения Лапласа")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig("lab3_convergence.png", dpi=150)
        plt.close(fig)

    return results


# ============================================================================
# БЛОК 7. РИСУНОК ЧИСЛЕННОГО РЕШЕНИЯ И ОШИБКИ
# ============================================================================
def visualize_solution(nx=20, ny=20, method="sor"):
    """Построить поверхности численного решения и абсолютной ошибки."""
    X, Y, u, exact, iterations, _ = solve_elliptic(
        nx=nx, ny=ny, method=method
    )
    max_error, rms_error, error = compute_error(u, exact)
    print(
        f"\nВизуализация {method}: итераций={iterations}, "
        f"max error={max_error:.3e}, RMS error={rms_error:.3e}"
    )

    fig = plt.figure(figsize=(13, 5))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(X, Y, u, cmap="viridis", edgecolor="none")
    ax1.set_title("Численное решение u(x,y)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("u")

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.plot_surface(X, Y, error, cmap="hot", edgecolor="none")
    ax2.set_title("Абсолютная ошибка |u-U|")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("Ошибка")

    fig.tight_layout()
    fig.savefig("lab3_solution_and_error.png", dpi=150)
    plt.close(fig)


# ============================================================================
# БЛОК 8. ИССЛЕДОВАНИЕ СЕТКИ И КОЛИЧЕСТВА ИТЕРАЦИЙ
# ============================================================================
def study_grid_dependence(method="sor", tol=1e-10):
    """
    Повторить расчёт на сетках разной плотности.

    Для варианта U=x+y центральная разностная схема воспроизводит линейное
    решение очень точно. Поэтому ошибка здесь в основном связана с допуском
    итераций и машинным округлением, а не с погрешностью аппроксимации.
    """
    print(f"\nЗависимость ошибки от сетки, метод {method}")
    rows = []
    for n in (5, 10, 20, 40, 80):
        X, Y, u, exact, iterations, _ = solve_elliptic(
            nx=n, ny=n, tol=tol, method=method
        )
        max_error, rms_error, _ = compute_error(u, exact)
        h = 1.0 / n
        rows.append((h, max_error, rms_error, iterations))
        print(
            f"N={n:3d}, h={h:.5f}, max error={max_error:.3e}, "
            f"RMS error={rms_error:.3e}, iterations={iterations}"
        )

    # Рисуем изменение максимальной ошибки при уменьшении шага h.
    hs = np.array([row[0] for row in rows])
    errors = np.array([row[1] for row in rows])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(hs, np.maximum(errors, 1e-16), "o-")
    ax.set_xlabel("Шаг сетки h")
    ax.set_ylabel("Максимальная ошибка")
    ax.set_title(f"Зависимость ошибки от h ({method})")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig("lab3_error_vs_h.png", dpi=150)
    plt.close(fig)

    return rows


def study_iterations_vs_n(methods=("jacobi", "seidel", "sor"),
                          n_values=(5, 10, 20, 40), tol=1e-8):
    """Сравнить, сколько итераций нужно каждому методу на разных сетках."""
    fig, ax = plt.subplots(figsize=(8, 5))
    print("\nКоличество итераций в зависимости от размера сетки")
    for method in methods:
        counts = []
        for n in n_values:
            *_, iterations, _ = solve_elliptic(
                nx=n, ny=n, tol=tol, method=method
            )
            counts.append(iterations)
        print(f"{method:8s}: " + ", ".join(
            f"N={n}: {count}" for n, count in zip(n_values, counts)
        ))
        ax.loglog(n_values, counts, "o-", label=method)

    ax.set_xlabel("N")
    ax.set_ylabel("Количество итераций")
    ax.set_title("Зависимость числа итераций от размера сетки")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("lab3_iterations_vs_n.png", dpi=150)
    plt.close(fig)


# ============================================================================
# БЛОК 9. ГЛАВНЫЙ ЗАПУСК ПРОГРАММЫ
# ============================================================================
def main():
    """Выполнить все основные расчёты и сохранить графики."""
    results = compare_methods(nx=20, ny=20, tol=1e-8, make_plot=True)
    visualize_solution(nx=20, ny=20, method="sor")
    study_grid_dependence(method="sor", tol=1e-10)
    study_iterations_vs_n()

    print("\nИтог по сетке 20x20:")
    for method, result in results.items():
        print(
            f"{method:8s}: итераций={result['iterations']:6d}, "
            f"max error={result['max_error']:.3e}, "
            f"RMS error={result['rms_error']:.3e}"
        )
    print("\nСозданы файлы:")
    print("  lab3_convergence.png")
    print("  lab3_solution_and_error.png")
    print("  lab3_iterations_vs_n.png")
    print("  lab3_error_vs_h.png")


# ============================================================================
# БЛОК 10. ТОЧКА ВХОДА
# ============================================================================
if __name__ == "__main__":
    main()
