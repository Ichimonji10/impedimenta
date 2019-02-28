# coding=utf-8
"""A CLI tool to manage Price Predictor's database."""
import argparse
import sys
from pathlib import Path
from typing import Callable, Optional

from pp import datasets, exceptions
from pp.cli import utils
from pp.constants import DATA_TABLES, DATA_TABLE_WEIGHTS
from pp.db import common, init


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(description='Manage database.')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_load_path(subparsers)
    add_save_path(subparsers)
    add_cpop(subparsers)
    add_normalize(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_cpop(subparsers) -> None:
    """Add the "cpop" subcommand to an argparse subparsers object."""
    msg = 'Create and populate a database.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'cpop',
        help=msg,
        description=msg,
    )
    parser.add_argument(
        'dataset',
        help='The dataset to use when populating the database.',
        choices=datasets.installed().keys(),
    )
    utils.add_overwrite_flags(
        parser,
        'Overwrite an existing database if one exists.'
    )
    parser.add_argument(
        '--seed',
        help=f"""
        Rows are assigned to tables {DATA_TABLES} in approximately the ratio
        {DATA_TABLE_WEIGHTS}. The exact row-to-table assignments are controlled
        by a random number generator. If one wishes to produce consistent
        row-to-table assignments, a consistent seed should be provided.
        """,
        type=int,
    )
    func: Callable[[argparse.Namespace], None] = handle_cpop
    parser.set_defaults(func=func)


def add_load_path(subparsers) -> None:
    """Add the "load-path" subcommand to an argparse subparsers object."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'load-path',
        help='Search for a database file.',
        description="""\
        Search several paths for a database file, in order of preference. If a
        file is found, print its path. Otherwise, return a non-zero exit code.
        """,
    )
    func: Callable[[argparse.Namespace], None] = handle_load_path
    parser.set_defaults(func=func)


def add_save_path(subparsers) -> None:
    """Add the "save-path" subcommand to an argparse subparsers object."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'save-path',
        help='Print the path to where a new database will be created.',
        description="""\
        Print the path to where a new database will be created when the 'cpop'
        subcommand is executed. As a side effect, create all directories in the
        path that don't yet exist.
        """,
    )
    func: Callable[[argparse.Namespace], None] = handle_save_path
    parser.set_defaults(func=func)


def add_normalize(subparsers) -> None:
    """Add the ``normalize`` subcommand to an argparse subparsers object."""
    msg = 'Normalize data in the database.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'normalize',
        help=msg,
        description=msg + (
            ' To "normalize" means to walk through each cell in a continuous '
            'column, find the corresponding standard score, and to update the '
            "cell's contents. This command may be safely re-executed. For "
            'more on standard scores, see: '
            'https://en.wikipedia.org/wiki/Standard_score'
        ),
    )
    utils.add_jobs_flag(parser)
    utils.add_progress_flags(parser)
    func: Callable[[argparse.Namespace], None] = handle_normalize
    parser.set_defaults(func=func)


def handle_cpop(args: argparse.Namespace) -> None:
    """Handle the 'cpop' subcommand."""
    if args.overwrite:
        path = Path(common.get_save_path())
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    try:
        init.cpop_db(args.dataset, args.seed)
    except exceptions.DatabaseAlreadyExistsError as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_load_path(_) -> None:
    """Handle the "load-path" subcommand."""
    try:
        print(common.get_load_path())
    except exceptions.DatabaseNotFoundError:
        exit(1)


def handle_save_path(_) -> None:
    """Handle the 'save-path' subcommand."""
    print(common.get_save_path())


def handle_normalize(args: argparse.Namespace) -> None:
    """Normalize the training table."""
    reporter: Optional[Callable]
    if args.progress:
        reporter = utils.report_progress
    else:
        reporter = None
    init.normalize(jobs=args.jobs, reporter=reporter)
