Price Predictor
===============

Predict the sale price of a house in King County.

To install, clone the source code, ``cd`` into its directory, and execute the
following:

.. code-block:: sh

    python3 -m venv ~/.venvs/price-predictor/
    source ~/.venvs/price-predictor/bin/activate
    pip install --upgrade pip flit

    # Add the --symlink flag to let code changes appear in current environment.
    flit install

You can now call the ``pp-*`` CLI utilities:

.. code-block:: sh

    pp-dataset install fixture-king-county
    pp-db cpop --overwrite fixture-king-county --seed 2
    pp-db normalize

    # Model "bathrooms" with non-null combinations of other columns.
    mapfile -t in_cols < <(
        pp-model columns --type continuous | grep -v bathrooms
    )
    pp-model lin-reg bathrooms "${in_cols[@]}" --combinations --progress

    pp-predict bathrooms --denormalize
    pp-predict bathrooms --mean-squared-error
    pp-predict bathrooms --mean-squared-error --table development_std_scores

For more interesting analyzes, install the actual `King County dataset`_. (Do
this with the ``pp-dataset install`` command.)

.. _king county dataset: https://www.kaggle.com/harlfoxem/housesalesprediction
