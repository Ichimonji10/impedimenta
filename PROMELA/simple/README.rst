Simple
======

An extremely simple PROMELA application that just verifies the possible values
that a pair of counters can write to a memory cell. Derived from `a primer on
model checking`_, by Mordechai Ben-Ari.

To compile and execute the verifier:

.. code-block:: sh

    make
    ./pan

The verifier should find an assertion error. To execute spin in guided mode,
with the trail file as a guide, and with assignments printed out:

.. code-block:: sh

    spin -p -k spec.pml.trail spec.pml

.. WARNING:: The spin option parser is crude. Precisely follow the command
    syntax listed in its man page. Do not place options after the ``.pml`` file,
    e.g. ``spin spec.pml -p -k spec.pml.trail``. Do not combine options, e.g.
    ``spin -pk spec.pml.trail spec.pml``.

.. _a primer on model checking: http://spinroot.com/spin/Doc/p40-ben-ari.pdf
