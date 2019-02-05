#!/usr/bin/env python3
# coding=utf-8
"""Implement Dijkstra's concurrent lock acquisition algorithm.

This module implements Dijkstra's concurrent lock acquisition algorithm, as
laid out in his 1965 paper "Solution of a Problem in Concurrent Programming
Control." The problem is as follows: given a group of N computers working
together on some task, how can we ensure that only one works on a critical
portion fo the task at a time? Some requirements are as follows:

#. If two computers attempt to enter the critical section at the same time, the
   solution can *not* be to choose a winner based on some static property of
   the computers, such as their IDs
#. Assumptions may not be made about the relative speeds of the computers. The
   computers may change speed over time.
#. If a computer leaves the cluster while not in the critical section, the
   remaining computers must be able to continue working on the task.
#. Theoretically infinite waits are permissible, so long as they're
   statistically unlikely.

To understand the solution, imagine a pair of circular walls, where each wall
has N doors in it, labeled 0 through (N - 1). For example, if N is four::

    ┌──0──┐ ← outer wall
    │┌─0─┐│ ← inner wall
    33   11
    │└─2─┘│
    └──2──┘

There are also N workers, labeled 0 through (N - 1). Each worker may be in one
of the following locations:

* Outside
* In the outer doorway with the same number
* In the inner doorway with the same number
* Inside

At the start of the algorithm, all workers are outside, and all doors are
closed. If a worker wishes to work on the critical task, it must walk inside.
If a worker has the same number as a door, it may learn the open/closed state
of that door and change the open/closed state of that door. Otherwise, it may
only learn the open/closed state of that door. An open door is considered true,
and a closed door is considered false.

With all this in mind, you should be equipped to read the code and understand
it.
"""
from threading import Thread
from time import sleep
from typing import Callable, List


WORKERS = 3

candidate_id: int = 0
inner_wall_doors: List[bool] = [False for _ in range(WORKERS)]
outer_wall_doors: List[bool] = [False for _ in range(WORKERS)]


def main() -> None:
    """Spawn several threads."""
    threads = [Thread(target=do_work, args=(i,)) for i in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def do_work(worker_id: int) -> None:
    """Do bogus work.

    Do work, acquire the lock, do more work, release the lock, and do more
    work. (No work is actually done.)

    :param worker_id: A unique identifier for this thread. Used in lock
        management logic.
    """
    lock_and_call(worker_id, print, f'Worker {worker_id} doing critical work.')


def lock_and_call(worker_id: int, function: Callable, *args, **kwargs) -> None:
    """Acquire the global lock, call the given function, and release the lock.

    :param worker_id: A unique identifier for this thread. Used in lock
        management logic.
    :param function: A function to call once the lock is acquired.
    :param args: Passed to ``function``.
    :param kwargs: Passed to ``function``.
    """
    global outer_wall_doors  # pylint:disable=global-statement,invalid-name
    global inner_wall_doors  # pylint:disable=global-statement,invalid-name
    global candidate_id  # pylint:disable=global-statement,invalid-name

    # Imagine two workers, A and B, where they wish to do some work in the
    # critical section. The following occurs:
    #
    # 1. A and B walk into their outer doorways, respectively.
    # 2. A and B discover that they're not the current candidate.
    # 3. A and B discover the current candidate's outer door is closed, meaning
    #    that it has finished working in the critical section. They both decide
    #    to announce themselves as the current candidate.
    # 4. A announces itself as the current candidate. It restarts the loop and
    #    discovers that it is the current candidate. It walks into its inner
    #    doorway, and starts checking the state of all other inner doors.
    # 5. B announces itself as the current candidate. It restarts the loop and
    #    discovers that it's the current candidate. It walks into its inner
    #    doorway and starts checking the state of all of the other inner doors.
    # 6. One of the following will happen:
    #
    #    * Both candidates will notice that another inner door is open, and
    #      they abort their attempt to get into the critical area.
    #    * A finishes checking all the other inner doors and enters the
    #      critical area. B notices that A's inner door is open and aborts its
    #      attempt to get into the critical area.
    outer_wall_doors[worker_id] = True
    have_lock = False
    while not have_lock:
        have_lock = False
        if candidate_id != worker_id:
            inner_wall_doors[worker_id] = False
            if not outer_wall_doors[candidate_id]:
                candidate_id = worker_id
        else:
            have_lock = True  # maybe
            inner_wall_doors[worker_id] = True
            for i, inner_wall_door in enumerate(inner_wall_doors):
                if i == worker_id:
                    continue
                if inner_wall_door:
                    have_lock = False

    print(f'Worker {worker_id} has acquired the lock.')
    sleep(2)
    function(*args, **kwargs)
    print(f'Worker {worker_id} is releasing the lock.')
    inner_wall_doors[worker_id] = False
    outer_wall_doors[worker_id] = False


if __name__ == '__main__':
    main()
