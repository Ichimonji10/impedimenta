# coding=utf-8
"""A CLI tool to to predict a column's values using other columns."""
import argparse
import math
import statistics

from pp import predict, utils
from pp.constants import STD_DATA_TABLES, STD_TRAINING_TABLE
from pp.db import read


def main() -> None:
    """Parse arguments and call business logic."""
    parser = argparse.ArgumentParser(description="Predict a column's values.")
    parser.add_argument(
        'column',
        help='The column for which to predict values.',
    )
    default = STD_TRAINING_TABLE
    parser.add_argument(
        '--table',
        help=f'The table for which to predict values. Defaults to {default}.',
        default=default,
        choices=STD_DATA_TABLES,
    )
    parser.add_argument(
        '--denormalize',
        help="""
        Denormalize printed values. By default, normalized values are printed.
        Normalized values indicate the number of sample standard deviations
        away from the mean for that column. In other words, a value of 0
        indicates "the mean for this column," a value of 1 indicates "one
        standard deviation above the mean for this column," a value of -1
        indicates "one standard deviation below the mean for this column," and
        so on.
        """,
        action='store_true',
    )

    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--mean-error',
        help='Print the mean error of the predictions as a whole.',
        action='store_true',
    )
    group.add_argument(
        '--mean-squared-error',
        help='Print the mean squared error of the predictions as a whole.',
        action='store_true',
    )
    group.add_argument(
        '--median-error',
        help='Print the median error of the predictions as a whole.',
        action='store_true',
    )

    args = parser.parse_args()
    if args.mean_error:
        handle_mean_error(args)
    elif args.mean_squared_error:
        handle_mean_squared_error(args)
    elif args.median_error:
        handle_median_error(args)
    else:
        handle_values(args)


def handle_mean_error(args: argparse.Namespace) -> None:
    """Print the mean error of the predicted values."""
    data_table = utils.get_data_table(args.table)
    std_dev = read.std_dev(data_table, args.column)

    preds = predict.predict(args.table, args.column)
    val = statistics.mean(math.fabs(pred.error) for pred in preds)
    if args.denormalize:
        val *= std_dev
    print(val)


def handle_mean_squared_error(args: argparse.Namespace) -> None:
    """Print the mean squared error of the predicted values."""
    data_table = utils.get_data_table(args.table)
    std_dev = read.std_dev(data_table, args.column)

    preds = predict.predict(args.table, args.column)
    val = statistics.mean(pred.error ** 2 for pred in preds)
    if args.denormalize:
        val *= std_dev
    print(val)


def handle_median_error(args: argparse.Namespace) -> None:
    """Print the median error of the predicted values."""
    data_table = utils.get_data_table(args.table)
    std_dev = read.std_dev(data_table, args.column)

    preds = predict.predict(args.table, args.column)
    val = statistics.median(math.fabs(pred.error) for pred in preds)
    if args.denormalize:
        val *= std_dev
    print(val)


def handle_values(args: argparse.Namespace) -> None:
    """Print the predicted values."""
    data_table = utils.get_data_table(args.table)
    mean = read.mean(data_table, args.column)
    std_dev = read.std_dev(data_table, args.column)

    preds = predict.predict(args.table, args.column)
    for pred in preds:
        actual = pred.actual
        prediction = pred.prediction
        if args.denormalize:
            actual = std_dev * actual + mean
            prediction = std_dev * prediction + mean
        difference = prediction - actual
        print(
            f'actual: {actual: .4f}  '
            f'prediction: {prediction: .4f}  '
            f'difference: {difference: .4f}'
        )
