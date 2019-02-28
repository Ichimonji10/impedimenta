# coding=utf-8
"""A CLI tool to model Price Predictor's database."""
import argparse
import sys
from typing import Callable, Iterable, Optional, Sequence

from pp import exceptions, model
from pp.cli import utils
from pp.constants import CONTINUOUS_TYPE, LAMBDA
from pp.db import read

_LIN_REG_SUBCMD = 'lin-reg'


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(description='Model database.')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_modelable(subparsers)
    add_lin_reg(subparsers)
    args = parser.parse_args()
    if args.subcommand == _LIN_REG_SUBCMD:
        if args.output_col in args.input_cols:
            parser.error(
                f'Do not predict a column (here, "{args.output_col}") with that '
                'same column. Doing so subverts the purpose of this program: to '
                'predict a column using other columns.'
            )
        if len(args.input_cols) > len(set(args.input_cols)):
            parser.error('Do not predict a column with redundant columns.')
    args.func(args)


def add_lin_reg(subparsers) -> None:
    """Add the ``lin-reg`` subcommand to an argparse subparsers object."""
    msg = 'Model the training table with a least squares linear regression.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        _LIN_REG_SUBCMD,
        help=msg,
        description=msg,
    )

    parser.add_argument(
        'output_col',
        metavar='output-col',
        help='The column being predicted.',
        type=_continuous_column_name,
    )
    parser.add_argument(
        'input_cols',
        metavar='input-cols',
        help="""
        The columns used to predict the output column. If omitted, all columns
        except the output column are used.
        """,
        type=_continuous_column_name,
        nargs='*',
    )
    parser.add_argument(
        '--combinations',
        help="""
        Model varying combinations of the input columns. For example, if the
        input columns are a and b, then columns [a, b], [a], and [b] would be
        modeled.
        """,
        action='store_true',
    )
    parser.add_argument(
        '--lambda',
        dest='lambda_',
        help=f"""
        A tunable constant used when calculating the cost of a model. Raising
        the value rewards simple, inaccurate models; lowering the value rewards
        complex, accurate models. Lowering this value too much runs the risk of
        over-fitting. Default: {LAMBDA}
        """,
        type=float,
        default=LAMBDA,
    )
    utils.add_jobs_flag(parser)
    utils.add_progress_flags(parser)
    func: Callable[[argparse.Namespace], None] = handle_lin_reg
    parser.set_defaults(func=func)


def add_modelable(subparsers) -> None:
    """Add the ``modelable`` subcommand to an argparse subparsers object."""
    msg = 'Print which columns may be modeled.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'modelable',
        help=msg,
        description=msg,
    )
    func: Callable[[argparse.Namespace], None] = handle_modelable
    parser.set_defaults(func=func)


def handle_lin_reg(args: argparse.Namespace) -> None:
    """Model the training table with a least squares linear regression."""
    reporter: Optional[Callable]
    if args.progress:
        reporter = utils.report_progress
    else:
        reporter = None

    input_cols: Sequence[str]
    if args.input_cols:
        input_cols = args.input_cols
    else:
        input_cols = tuple(set(_get_modelable()) - {args.output_col})

    try:
        model.lin_reg(
            args.output_col,
            input_cols,
            args.lambda_,
            args.combinations,
            jobs=args.jobs,
            reporter=reporter,
        )
    except exceptions.ModelingError as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_modelable(args: argparse.Namespace) -> None:  # pylint:disable=unused-argument
    """Print which columns may be modeled."""
    for column_name in _get_modelable():
        print(column_name)


def _get_modelable() -> Iterable[str]:
    yield from read.meta_column_names(CONTINUOUS_TYPE)


def _continuous_column_name(arg):
    if arg not in _get_modelable():
        raise ValueError(f'{arg} not one of {_get_modelable()}')
    return arg
