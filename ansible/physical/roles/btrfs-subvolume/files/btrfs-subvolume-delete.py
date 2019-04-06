#!/usr/bin/env python3
# coding=utf-8
# pylint:disable=invalid-name
# It's OK for this module to have an invalid name. It's a shell script, not a
# module to be imported.
"""Delete old Btrfs subvolumes from a given path."""
import argparse
import datetime
import io
import pathlib
import subprocess
import textwrap


def main():
    """Parse arguments, and call other functions as needed."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Delete old btrfs subvolumes.',
        epilog=_get_epilog(),
    )
    parser.add_argument(
        'path',
        type=str,
        help='The base path to use when searching for snapshots.',
    )
    parser.add_argument(
        'days',
        type=int,
        help='The maximum age of snapshots, in days.',
    )
    parser.add_argument(
        'weeks',
        type=int,
        help='The maximum age of snapshots, in weeks.',
    )
    args = parser.parse_args()
    find_prune_snapshots(args.path, args.days, args.weeks)


def find_prune_snapshots(path, days, weeks):
    """Find and prune snapshots."""
    now = datetime.datetime.now(datetime.timezone.utc)
    ppath = pathlib.PosixPath(path).resolve()
    # For some reason, Pylint thinks that ppath is a PurePath object, instead
    # of a PosixPath object. And PurePath objects don't have a glob() method.
    snapshots = ppath.glob('*')  # pylint:disable=no-member
    for snapshot in snapshots:
        created = _get_datetime(snapshot.parts[-1])
        age = now - created
        if age <= datetime.timedelta(days=int(days)):
            continue
        elif (age <= datetime.timedelta(weeks=int(weeks)) and
              created.isoweekday() == 3):
            continue  # 1–7 == mon–sun
        else:
            subprocess.run(['btrfs', 'subvolume', 'delete', str(snapshot)])


def _get_datetime(timestamp):
    """Parse the given ISO 8601 datetime string.

    :param path: A string like ``2016-08-21T18:03-04:00``. The embedded
        timezone information, if present, may contain a colon (e.g.
        ``-04:00``).
    :returns: An "aware" ``datetime.datetime`` object.
    """
    if timestamp[-3] == ':':
        # root-2016-08-21T18:03-04:00 → root-2016-08-21T18:03-0400
        timestamp = timestamp[:-3] + timestamp[-2:]
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M%z')


def _get_epilog():
    """Return a string for use in argparse's epilog."""
    wrapper = textwrap.TextWrapper()
    with io.StringIO() as handle:
        handle.write(wrapper.fill(textwrap.dedent('''\
            When this script executes, it will search for files named `path-*`.
            Each file named `path-<iso-8601-string>` is assumed to be a btrfs
            subvolume of `path`, and is considered for deletion. <iso-8601-string>
            is assumed to describe when the snapshot was created. The deletion
            logic is as follows:
            ''')))

        handle.write('\n\n')
        wrapper.initial_indent = '1. '
        wrapper.subsequent_indent = '   '
        handle.write(wrapper.fill(
            'If the snapshot is not yet <days> old, it is kept.'
        ))

        handle.write('\n')
        wrapper.initial_indent = '2. '
        handle.write(wrapper.fill(textwrap.dedent('''\
            If the snapshot is not yet <weeks> old and was created on a
            Wednesday, it is kept.
            ''')))

        handle.write('\n')
        wrapper.initial_indent = '3. '
        handle.write(wrapper.fill('The snapshot is deleted.'))

        return handle.getvalue()


if __name__ == '__main__':
    exit(main())
