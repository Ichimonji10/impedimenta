#!/usr/bin/env python3
# coding=utf-8
import random

import numpy as np
from sklearn import linear_model


def main():
    training_guides = gen_training_guides()
    training_target = gen_training_target()
    print(training_guides)
    print(training_target)

    matrix_clf = linear_model.LinearRegression()
    matrix_clf.fit(training_guides, training_target)
    print('matrix prediction:')
    print(matrix_clf.predict(training_guides))

    sgd_clf = linear_model.SGDRegressor(max_iter=1000, tol=1e-3)
    sgd_clf.fit(training_guides, training_target)
    print('SGD prediction:')
    print(sgd_clf.predict(training_guides))


def gen_training_guides():
    col_0_gen = sequential_ints()
    col_1_gen = random_ints()
    return np.array(
        [[next(col_0_gen), next(col_1_gen)] for _ in range(10)],
        np.int_,
    )


def gen_training_target():
    col_gen = sequential_ints()
    return np.array(
        [next(col_gen) for _ in range(10)],
        np.int_,
    )


def sequential_ints():
    i = 0
    while True:
        yield i
        i += 1


def random_ints():
    while True:
        yield random.randint(-1000, 1000)


if __name__ == '__main__':
    main()
