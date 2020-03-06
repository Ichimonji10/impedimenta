intersphinx-path-2
==================

Location: `root </>`_ → `plugin 2 </plugins/intersphinx-path-2/>`_

An object provided by this package is:

.. autoclass:: intersphinx_path_2.Bar

An object not provided by this package is:

.. class:: Bicep

    A delightful vanity muscle.

I can reference objects in this package, such as :class:`intersphinx_path_2.Bar`
or :class:`Bicep`. I can also include source code:

.. literalinclude:: ../intersphinx_path_2/__init__.py

I can also reference objects in a different package, such as
:class:`intersphinx_path_1.Foo` or :class:`Quadricep`.

glossary
--------

Here's some glossary terms that can be referenced with the ``:term:`` role:

.. glossary::

    Eyeliner
        Still not a food.

    Mascara
        Just go to the grocery store already.

If there's ambiguity, I can disambiguate with syntax like
:term:`intersphinx-path-1:Eyeliner` and :term:`Eyeliner`.
