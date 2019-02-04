Dijkstra - Concurrent
=====================

A PROMELA model of Dijkstra's concurrent lock acquisition algorithm.

This application models Dijkstra's concurrent lock acquisition algorithm as
described in "Solution of a Problem in Concurrent Programming Control."

To compile and execute the verifier:

.. code-block:: sh

    make
    ./pan

All assertions should pass. If the verifier finds tha any assertions fail, it
will generate a ``.trail`` file. Spin can then be invoked in guided mode and
told to follow the trail:

.. code-block:: sh

    spin -p -k spec.pml.trail spec.pml
