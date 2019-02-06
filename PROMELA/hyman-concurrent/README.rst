Dijkstra - Concurrent
=====================

A PROMELA model of Hyman's (flawed) concurrent lock acquisition algorithm.

This application models Hyman's (flawed) concurrent lock acquisition algorithm,
as laid out in his 1966 letter "Comments on a Problem in Concurrent Programming
Control."

To compile and execute the verifier:

.. code-block:: sh

    make
    ./pan

An assertion should fail, and the verifier will generate a ``.trail`` file.
Spin can then be invoked in guided mode and told to follow the trail:

.. code-block:: sh

    spin -p -k spec.pml.trail spec.pml
