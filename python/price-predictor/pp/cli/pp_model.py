# coding=utf-8
"""A CLI tool to model Price Predictor's database."""
import argparse
import sys
from typing import Callable, Optional, Sequence

# pylint:disable=wrong-import-position
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
# pylint:enable=wrong-import-position

from pp import exceptions, model
from pp.cli import utils
from pp.constants import COLUMN_TYPES, CONTINUOUS_TYPE, LAMBDA
from pp.db import read

_K_MEANS_SUBCMD = 'k-means'
_K_MEANS_ZIP_CODE_PRICE_SUBCMD = 'k-means-zip-code-price'
_LIN_REG_SUBCMD = 'lin-reg'


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(description='Model database.')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_columns(subparsers)
    add_k_means(subparsers)
    add_k_means_zip_code_price(subparsers)
    add_lin_reg(subparsers)
    args = parser.parse_args()
    if args.subcommand == _K_MEANS_SUBCMD:
        _do_k_means_subcmd_checks(parser, args)
    if args.subcommand == _LIN_REG_SUBCMD:
        _do_lin_reg_subcmd_checks(parser, args)
    args.func(args)


def _do_lin_reg_subcmd_checks(parser, args) -> None:
    if args.output_col in args.input_cols:
        parser.error(
            f'Do not predict a column (here, "{args.output_col}") with that '
            'same column. Doing so subverts the purpose of this program: to '
            'predict a column using other columns.'
        )
    if len(args.input_cols) > len(set(args.input_cols)):
        parser.error('Do not predict a column with redundant columns.')


def _do_k_means_subcmd_checks(parser, args) -> None:
    num_columns = len(args.column_names)
    if args.plot and num_columns != 2:
        parser.error(
            'This application can only plot 2 columns. However, this '
            f'application was asked to plot {num_columns}: '
            f'{", ".join(args.column_names)}'
        )


def add_k_means(subparsers) -> None:
    """Add the ``k-means`` subcommand to an argparse subparsers object."""
    msg = 'Model the training table with k-means clusters.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        _K_MEANS_SUBCMD,
        help=msg,
        description=msg,
    )
    parser.add_argument(
        'column_names',
        metavar='column-names',
        help='The columns (i.e. features) to consider when clustering points.',
        type=utils.column_name,
        nargs='+',
    )
    parser.add_argument(
        '-k',
        '--clusters',
        help='The number of clusters to create.',
        type=utils.positive_int,
        default=5,
    )
    parser.add_argument(
        '--plot',
        help="""
        Generate a graphical plot of the points and the clusters they belong
        to. Only valid if there are two input-cols.
        """,
        action='store_true',
    )
    func: Callable[[argparse.Namespace], None] = handle_k_means
    parser.set_defaults(func=func)


def add_k_means_zip_code_price(subparsers) -> None:
    """Add the ``k-means-zip-code-price`` subcommand to a subparser."""
    msg = 'Model zip code and price with k-means clusters.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        _K_MEANS_ZIP_CODE_PRICE_SUBCMD,
        help=msg,
        description=msg + (
            ' This subcommand is a hack, and it exists due to shortcomings in '
            'the normalization code. For most k-means modeling tasks, use the '
            f'{_K_MEANS_SUBCMD} subcommand.'
        ),
    )
    parser.add_argument(
        'zip_code',
        metavar='zip-code',
        help='The zip code to use in this plot.',
        type=utils.zip_code,
    )
    parser.add_argument(
        '-k',
        '--clusters',
        help='The number of clusters to create.',
        type=utils.positive_int,
        default=2,
    )
    parser.add_argument(
        '--plot',
        help="""
        Generate a graphical plot of the points and the clusters they belong
        to.
        """,
        action='store_true',
    )
    func: Callable[[argparse.Namespace], None] = handle_k_means_zip_code_price
    parser.set_defaults(func=func)


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
        type=utils.continuous_column_name,
    )
    parser.add_argument(
        'input_cols',
        metavar='input-cols',
        help="""
        The columns used to predict the output column. If omitted, all columns
        except the output column are used.
        """,
        type=utils.continuous_column_name,
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


def add_columns(subparsers) -> None:
    """Add the ``columns`` subcommand to an argparse subparsers object."""
    msg = 'Print which columns may be modeled.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'columns',
        help=msg,
        description=msg,
    )
    parser.add_argument(
        '--type',
        help='Print a type of column, instead of all columns.',
        choices=COLUMN_TYPES,
    )
    func: Callable[[argparse.Namespace], None] = handle_columns
    parser.set_defaults(func=func)


def handle_k_means(args: argparse.Namespace) -> None:
    """Model the training table with k-means clusters."""
    columns, codebook, distortion = model.k_means(
        args.column_names,
        args.clusters,
    )
    if args.plot:
        plt.title(f'Distortion: {distortion:.2f}')
        plt.xlabel(args.column_names[0])
        plt.ylabel(args.column_names[1])
        plt.scatter(columns[:, 0], columns[:, 1])
        plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
        plt.savefig(sys.stdout)
    else:
        print('Columns:')
        print(columns)
        print()
        print('Codebook:')
        print(codebook)
        print()
        print('Distortion:')
        print(distortion)


def handle_k_means_zip_code_price(args: argparse.Namespace) -> None:
    """Model zip code and price with k-means clusters."""
    columns, codebook, distortion = model.k_means_zip_code_price(
        args.zip_code,
        args.clusters,
    )
    if args.plot:
        plt.title(f'Distortion: {distortion:.2f}')
        plt.xlabel('zipcode')
        plt.ylabel('price')
        plt.scatter(columns[:, 0], columns[:, 1])
        plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
        plt.savefig(sys.stdout)
    else:
        print('Columns:')
        print(columns)
        print()
        print('Codebook:')
        print(codebook)
        print()
        print('Distortion:')
        print(distortion)


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
        input_cols = tuple(
            set(read.meta_column_names(CONTINUOUS_TYPE)) - {args.output_col}
        )

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


def handle_columns(args: argparse.Namespace) -> None:
    """Print which columns may be modeled."""
    for column_name in read.meta_column_names(args.type):
        print(column_name)
