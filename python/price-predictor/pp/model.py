# coding=utf-8
"""Tools for modeling matrices."""
from typing import Callable, Iterator, Optional, Sequence

from pp import exceptions
from pp.db import calc, common, write


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
