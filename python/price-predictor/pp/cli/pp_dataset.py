# coding=utf-8
"""A CLI tool to manage datasets."""
import argparse
import pathlib
import sys
from typing import Callable

from pp import datasets, exceptions
from pp.constants import DATASETS_DIR


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description='Manage datasets.',
        epilog=f"""\
        A dataset consists of two CSV files, one containing house sale records,
        and the other describing the semantics of the house sale records. For
        an example of what a valid dataset looks like, install and examine the
        "{datasets.FixtureSimpleDS().name}" dataset.
        """,
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_install(subparsers)
    add_installed(subparsers)
    add_manageable(subparsers)
    add_uninstall(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_install(subparsers) -> None:
    """Add the install subcommand to an argparse subparsers object."""
    helptext = 'Install a dataset.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'install',
        help=helptext,
        description=f"""
        {helptext} Return non-zero if it's already installed.
        """
    )
    parser.add_argument(
        'dataset',
        help='The dataset to install.',
        choices=datasets.manageable().keys(),
    )
    parser.add_argument(
        '--archive',
        help='Install from the given archive.',
        type=pathlib.Path,
    )
    func: Callable[[argparse.Namespace], None] = handle_install
    parser.set_defaults(func=func)


def add_installed(subparsers) -> None:
    """Add the "installed" subcommand to an argparse subparsers object."""
    helptext = 'List installed datasets.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'installed',
        help=helptext,
        description=f"""
        {helptext} A dataset is "installed" if its constituent CSV files have
        been cleaned up, and if a directory containing these files has been
        copied to one of ${{XDG_DATA_DIRS}}/{DATASETS_DIR}.
        """,
    )
    parser.add_argument(
        '--path',
        help='List the path to each dataset.',
        action='store_true',
    )
    func: Callable[[argparse.Namespace], None] = handle_installed
    parser.set_defaults(func=func)


def add_manageable(subparsers) -> None:
    """Add the manageable subcommand to an argparse subparsers object."""
    helptext = 'List manageable datasets.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'manageable',
        help=helptext,
        description=f"""
        {helptext} A dataset is considered manageable if procedures for
        installing and uninstalling that dataset have been defined internally
        within this app. Other datasets may be imported into the database,
        analyzed, and so on. But for those datasets, you are responsible for
        installing the dataset.
        """,
    )
    func: Callable[[argparse.Namespace], None] = handle_manageable
    parser.set_defaults(func=func)


def add_uninstall(subparsers) -> None:
    """Add the "uninstall" subcommand to an argparse subparsers object."""
    helptext = 'Uninstall a dataset.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'uninstall',
        help=helptext,
        description=f"""
        {helptext} Return non-zero if the target dataset doesn't exist.
        """,
    )
    parser.add_argument(
        'dataset',
        help='The dataset to uninstall.',
        choices=datasets.manageable().keys(),
    )
    func: Callable[[argparse.Namespace], None] = handle_uninstall
    parser.set_defaults(func=func)


def handle_install(args: argparse.Namespace) -> None:
    """Handle the "install" subcommand."""
    try:
        datasets.manageable()[args.dataset].install(archive=args.archive)
    except exceptions.DatasetInstallError as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_installed(args: argparse.Namespace) -> None:
    """Handle the "installed" subcommand."""
    installed_datasets = datasets.installed()
    if args.path:
        for dataset_path in installed_datasets.values():
            print(dataset_path)
    else:
        for dataset_name in installed_datasets:
            print(dataset_name)


def handle_manageable(_) -> None:
    """Handle the "manageable" subcommand."""
    for name in datasets.manageable():
        print(name)


def handle_uninstall(args: argparse.Namespace) -> None:
    """Handle the "uninstall" subcommand."""
    try:
        datasets.manageable()[args.dataset].uninstall()
    except exceptions.DatasetNotFoundError as err:
        print(err, file=sys.stderr)
        exit(1)
