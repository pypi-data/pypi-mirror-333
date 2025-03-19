from scipy import stats
import numpy as np


def correlation_coefficient(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """
    Считает коэффициент корреляции Пирсона и p-значение.

    Коэффициент корреляции Пирсона измеряет линейную зависимость между двумя наборами данных.
    Изменяется в диапазоне от -1 до +1, где 0 означает отсутствие корреляции.
    Корреляция, равная -1 или +1, означает точную линейную зависимость.
    Положительная корреляция означает, что по мере увеличения x увеличивается и y.
    Отрицательная корреляция означает, что по мере увеличения x уменьшается и y.

    p-значение - это вероятность того, что некоррелированная система создаст наборы данных,
    корреляция Пирсона в которых будет как минимум такой же сильной, как в этих наборах данных.

    Parameters
    ----------
    x: np.ndarray
        1D массив значений.
    y: np.ndarray
        1D массив значений.

    Returns
    -------
    tuple[float, float]
        Коэффициент корреляции и вероятность получения наблюдаемых результатов.
    """

    assert x.ndim == 1, "x: Ожидался 1D массив"
    assert y.ndim == 1, "y: Ожидался 1D массив"
    assert x.shape == y.shape, "x и y должны иметь одинаковую длину"

    result = stats.pearsonr(x, y)
    corr_coef = result.statistic
    p_value = result.pvalue
    return corr_coef, p_value


def spearman_correlation_coefficient(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """
    Считает коэффициент корреляции Спирмена и p-значение.

    Коэффициент корреляции Спирмена — это непараметрическая мера монотонности взаимосвязи между двумя наборами данных.
    Изменяется в диапазоне от -1 до +1, где 0 означает отсутствие корреляции.
    Корреляция, равная -1 или +1, означает точную монотонную взаимосвязь.
    Положительная корреляция означает, что по мере увеличения x увеличивается и y.
    Отрицательная корреляция означает, что по мере увеличения x уменьшается и y.

    p-значение - это вероятность того, что некоррелированная система создаст наборы данных,
    корреляция Спирмена в которых будет как минимум такой же сильной, как в этих наборах данных.

    Parameters
    ----------
    x: np.ndarray
        1D массив значений.
    y: np.ndarray
        1D массив значений.

    Returns
    -------
    tuple[float, float]
        Коэффициент корреляции и вероятность получения наблюдаемых результатов.
    """

    assert x.ndim == 1, "x: Ожидался 1D массив"
    assert y.ndim == 1, "y: Ожидался 1D массив"
    assert x.shape == y.shape, "x и y должны иметь одинаковую длину"

    result = stats.spearmanr(x, y)
    corr_coef = result.statistic
    p_value = result.pvalue
    return corr_coef, p_value


def correlation_coefficients_matrix(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Считает матрицу корреляции Пирсона и матрицу p-значений.

    Коэффициент корреляции Пирсона измеряет линейную зависимость между двумя наборами данных.
    Изменяется в диапазоне от -1 до +1, где 0 означает отсутствие корреляции.
    Корреляция, равная -1 или +1, означает точную линейную зависимость.
    Положительная корреляция означает, что по мере увеличения x увеличивается и y.
    Отрицательная корреляция означает, что по мере увеличения x уменьшается и y.

    p-значение - это вероятность того, что некоррелированная система создаст наборы данных,
    корреляция Пирсона в которых будет как минимум такой же сильной, как в этих наборах данных.

    Parameters
    ----------
    data: np.ndarray
        Массив значений, размера (N, M).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Матрица корреляции(размера (N, N)) и матрица вероятностей получения наблюдаемых результатов(размера (N, N)).
    """

    assert data.ndim == 2, "data: Ожидался 2D массив"
    assert data.shape[1] >= 2, "data: Ожидался массив с элементами длинной не менее 2"

    matrix = np.zeros((data.shape[0], data.shape[0]), dtype=float)
    p_matrix = np.zeros((data.shape[0], data.shape[0]), dtype=float)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            matrix[i, j], p_matrix[i, j] = correlation_coefficient(data[i], data[j])
    return matrix, p_matrix


def spearman_correlation_coefficients_matrix(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Считает матрицу корреляции Спирмена и матрицу p-значений.

    Коэффициент корреляции Спирмена — это непараметрическая мера монотонности взаимосвязи между двумя наборами данных.
    Изменяется в диапазоне от -1 до +1, где 0 означает отсутствие корреляции.
    Корреляция, равная -1 или +1, означает точную монотонную взаимосвязь.
    Положительная корреляция означает, что по мере увеличения x увеличивается и y.
    Отрицательная корреляция означает, что по мере увеличения x уменьшается и y.

    p-значение - это вероятность того, что некоррелированная система создаст наборы данных,
    корреляция Спирмена в которых будет как минимум такой же сильной, как в этих наборах данных.

    Parameters
    ----------
    data: np.ndarray
        Массив значений, размера (N, M).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Матрица корреляции(размера (M, M)) и матрица вероятностей получения наблюдаемых результатов(размера (M, M)).
    """

    assert data.ndim == 2, "data: Ожидался 2D массив"
    assert data.shape[1] >= 2, "data: Ожидался массив с элементами длинной не менее 2"

    matrix = np.zeros((data.shape[0], data.shape[0]), dtype=float)
    p_matrix = np.zeros((data.shape[0], data.shape[0]), dtype=float)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            matrix[i, j], p_matrix[i, j] = spearman_correlation_coefficient(data[i], data[j])
    return matrix, p_matrix
