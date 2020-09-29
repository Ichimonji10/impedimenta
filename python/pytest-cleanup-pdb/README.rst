pytest-cleanup-pdb
==================

Muck around with pytest to see how it handles cleanup with the ``--pdb`` flag.

Let's say that you write a test that invokes some clean-up code via a fixture,
like so:

.. code-block:: python

    @pytest.fixture(scope="function")
    def cleaned_up_fixture():
        print("set-up work")
        yield "special value"
        print("tear-down work")

Secondly, let's say that the test case which makes use of this method contains a
failing assertion.

Thirdly, let's say that pytest is invoked with the ``--pdb`` option, which
causes it to spawn a PDB debugger if an assertion fails.

Question: when is the PDB debugger invoked? Is it invoked immediately when the
assertion fails? Or is tear-down code run before PDB is invoked?

The test code in this Python module explores this hypothetical. You can find out
the results for yourself by running the test code:

.. code-block:: sh

    poetry install
    poetry run pytest --pdb --capture=no

The results indicate that PDB is immediately invoked when a test fails, and
before tear-down code executes.
