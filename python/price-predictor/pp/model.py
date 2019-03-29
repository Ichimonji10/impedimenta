# coding=utf-8
"""Tools for modeling matrices."""
from typing import Any, Callable, Iterator, Optional, Sequence, Tuple

import numpy as np
from scipy.cluster.vq import kmeans

from pp import exceptions
from pp.constants import STD_TRAINING_TABLE
from pp.db import calc, common, read, write


def lin_reg(
        output_col: str,
        input_cols: Sequence[str],
        lambda_: float,
        combinations: bool = False,
        *,
        jobs: Optional[int] = None,
        reporter: Optional[Callable] = None) -> None:
    """Model a dependent column with sets of independent columns.

    Create each model using a least-squares linear matrix equation.

    :param output_col: The column to predict.
    :param input_cols: The columns to use to formulate a prediction.
    :param lambda_: See :data:`pp.constants.LAMBDA`.
    :param combinations: Model varying combinations of the input columns. For
        example, if the input columns are a and b, then columns [a, b], [a],
        and [b] would be modeled.
    """
    models_: Iterator[common.ModelsRow] = calc.models(
        output_col,
        input_cols,
        lambda_,
        combinations,
        jobs=jobs,
        reporter=reporter,
    )
    try:
        best_model: common.ModelsRow = next(models_)
    except StopIteration as err:
        raise exceptions.ModelingError(f'Unable to model {output_col}') from err
    for model in models_:
        if model.cost < best_model.cost:
            best_model = model
    write.models((best_model,))


def k_means(column_names: Sequence[str], k: int) -> Tuple[Any, Any, Any]:
    """Model the training table with k-means clusters.

    :param column_names: The columns (i.e. features) to consider when
        clustering points.
    :param k: The number of clusters to create.
    :return: A tuple in the form ``(columns, codebook, distortion)``, where:

        *   ``columns`` is the numpy array being analyzed. Each row represents
            one observation.
        *   ``codebook`` and ``distortion`` are the same as for
            `scipy.cluster.vq.kmeans`_.

    .. _scipy.cluster.vq.kmeans:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html
    """
    columns = np.array(
        tuple(read.table(STD_TRAINING_TABLE, column_names)),
        np.float_,
    )
    codebook, distortion = kmeans(columns, k)
    return columns, codebook, distortion


def k_means_zip_code_price(zip_code: str, k: int) -> Tuple[Any, Any, Any]:
    """Model zip code and price with k-means clusters."""
    columns = np.array(tuple(read.zip_code_price(zip_code)), np.float_)
    codebook, distortion = kmeans(columns, k)
    return columns, codebook, distortion
