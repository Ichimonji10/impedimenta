intersphinx-path-1
==================

Location: `root </>`_ → `plugin 1 </plugins/intersphinx-path-1/>`_

An object provided by this package is:

.. autoclass:: intersphinx_path_1.Foo

An object not provided by this package is:

.. class:: Quadricep

    A fantastically strong core muscle.

    Make sure to do your squats deep enough to balance out its development with
    the development of muscles such as the hamstrings, glutes, and adductors.
    Doing so helps to reduce stress on the ACLs.

I can reference objects in this package, such as :class:`intersphinx_path_1.Foo`
or :class:`Quadricep`. I can also include source code:

.. literalinclude:: ../intersphinx_path_1/__init__.py

I can also reference objects in a different package, such as
:class:`intersphinx_path_2.Bar` or :class:`Bicep`, though I can't directly
include their source code.

glossary
--------

Here's some glossary terms that can be referenced with the ``:term:`` role:

.. glossary::

    Eyeliner
        Not a food.

    Foundation.
        Also not a food.

If there's ambiguity, I can disambiguate with syntax like
:term:`Eyeliner` and :term:`intersphinx-path-2:Eyeliner`.
