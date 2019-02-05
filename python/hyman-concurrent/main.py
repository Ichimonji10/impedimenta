#!/usr/bin/env python3
# coding=utf-8
"""Implement Hyman's (flawed) concurrent lock acquisition algorithm.

This module implements Hyman's concurrent lock acquisition algorithm, as laid
out in his 1966 letter "Comments on a Problem in Concurrent Programming
Control."

The original problem is as follows: given a group of N computers working
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

In addition, Hyman notes that his algorithm works when there are only two
computers. The original code is poorly formatted and, to my eyes, illegible.
Furthermore, Knuth noted that "there are 15 syntactic ALGOL errors in 12 lines
of program!" The California State University, Stanislaus, has provided a
`translation`_. Here is a slightly cleaned-up rendition of that translation,
which I will use as the basis of my program:

    // Each of two processes, P0 and P1 executes the code below, P0 executes
    // Protocol(0,1), and P1 executes Protocol(1,0).

    int turn = 0;
    int flag[2] = false;
    void Protocol (int me, int you) {
        do {
            flag[me] = true;
            while (turn != me) {
                while (flag[you]) {
                    /* do nothing */;
                }
                turn = me;
            }
            CriticalSection(me);
            flag[me] = false;
            RemainderSection(me);
        } while (true);
    }

For an example of how this procedure can fail, consider the following
scenario:

#. Worker 1 raises flag 1.
#  Worker 1 notes that it is not their turn to do work.
#. Worker 1 notes that flag 0 is down.
#. Worker 0 raises his flag.
#. Worker 0 notes that it is his turn to do work, and proceeds into the
    critical section.
#. Worker 1 declares that it is his turn to do work, and proceeds into the
    critical section.

.. _translation:
    https://www.cs.csustan.edu/~john/Classes/Previous_Semesters/CS3750_OperatingSys_I/2009_04_Fall/hymanProb.html
"""
from threading import Thread
from typing import Callable, List

WORKERS = 2

turn: int = 0
flags: List[bool] = [False, False]


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
    global turn  # pylint:disable=global-statement,invalid-name
    global flags  # pylint:disable=global-statement,invalid-name

    other_worker_id = 1 - worker_id
    flags[worker_id] = True
    while turn != worker_id:
        while flags[other_worker_id]:
            pass
        turn = worker_id
    print(f'Worker {worker_id} has acquired the lock.')
    function(*args, **kwargs)
    print(f'Worker {worker_id} is releasing the lock.')
    flags[worker_id] = False


if __name__ == '__main__':
    main()
