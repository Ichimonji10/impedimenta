# coding=utf-8
"""Tools for predicting matrix values."""
from typing import Iterator, NamedTuple, Tuple

from pp import exceptions
from pp.db import common, read


class Prediction(NamedTuple):
    """A predicted value for one cell of a table."""
    actual: float
    prediction: float

    @property
    def error(self):
        """The difference between the predicted and actual value."""
        return self.prediction - self.actual


def predict(table_name: str, column_name: str) -> Iterator[Prediction]:
    """Predict a column's values.

    :param column_name: The column for which to predict values.
    :param table_name: The table for which to predict values.
    :return: An iterator that returns predictions, one per cell.
    """
    try:
        model: common.ModelsRow = read.model(column_name)
    except exceptions.PredictionError as err:
        print(err)
        exit(1)

    in_col_names: Tuple[str, ...] = tuple(model.input_columns)
    out_col_name: str = model.output_column
    for row in read.table(table_name, in_col_names + (out_col_name,)):
        pred = model.offset
        for in_col_name, cell in zip(in_col_names, row):
            coef = model.input_columns[in_col_name]
            pred += coef * cell
        actual = row[-1]
        yield Prediction(actual, pred)
