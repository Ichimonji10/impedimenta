# coding=utf-8
"""Constants for use by the entire application."""
from pathlib import PurePath
from typing import Mapping, Sequence


###############################################################################
# Filesystem
###############################################################################

XDG_DIR: PurePath = PurePath('price-predictor')
"""The basename of this application's directories.

For more information, see the `XDG Base Directory Specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
"""

ARCHIVES_DIR: PurePath = PurePath(XDG_DIR, 'archives')
"""The basename of an archives directory.

A dataset archive shouldn't be placed directly in an :data:`XDG_DIR`, as doing
so can cause name conflicts. It's better to place such files in a dedicated
directory.
"""

DATASETS_DIR: PurePath = PurePath(XDG_DIR, 'datasets')
"""The basename of the paths that contain datasets.

A dataset shouldn't be placed directly in an :data:`XDG_DIR`, as doing so can
cause name conflicts. It's better to place such files in a dedicated directory.
"""

DATA_FILE: str = 'data.csv'
"""The name of the file from an installed dataset which contains data."""

METADATA_FILE: str = 'metadata.csv'
"""The name of the file from an installed dataset which contains metadata."""

DB_FILE = PurePath(XDG_DIR, 'db.db')
"""The path to the database."""

###############################################################################
# Database
###############################################################################

TRAINING_TABLE: str = 'training'
"""The name of the database table in which training data is kept."""

DEVELOPMENT_TABLE: str = 'development'
"""The name of the database table in which development data is kept."""

TESTING_TABLE: str = 'testing'
"""The name of the database table in which testing data is kept."""

DATA_TABLES: Sequence[str] = (TRAINING_TABLE, DEVELOPMENT_TABLE, TESTING_TABLE)
"""The database tables that hold training, development and testing data.

This must be a sequence instead of a set so that, all other things (like seed)
being equal, :func:`pp.db.init.cpop_data_tables` assigns rows to tables in a
consistent manner.
"""

DATA_TABLE_WEIGHTS: Sequence[int] = (3, 1, 1)
"""The (approximate) ratio for assigning rows to data tables.

When rows are read from a dataset into the database, each row is assigned to
one of the :data:`DATA_TABLES`. Each time a row is read in, a random number
generator uses these weights to probabilistically select the target table.

.. WARN:: This must be the same length as :data:`DATA_TABLES`.
"""

assert len(DATA_TABLES) == len(DATA_TABLE_WEIGHTS)

_STD_SUFFIX = '_std_scores'

STD_TRAINING_TABLE: str = TRAINING_TABLE + _STD_SUFFIX
"""Standard scores for the :data:`pp.constants.TRAINING_TABLE`."""

STD_DEVELOPMENT_TABLE: str = DEVELOPMENT_TABLE + _STD_SUFFIX
"""Standard scores for the :data:`pp.constants.DEVELOPMENT_TABLE`."""

STD_TESTING_TABLE: str = TESTING_TABLE + _STD_SUFFIX
"""Standard scores for the :data:`pp.constants.TESTING_TABLE`."""

STD_DATA_TABLES: Sequence[str] = (
    STD_TRAINING_TABLE,
    STD_DEVELOPMENT_TABLE,
    STD_TESTING_TABLE,
)
"""Tables containing partially normalized data.

These tables mirror the similarly named :data:`pp.constants.DATA_TABLES`. When
these tables are populated, categorical columns are copied verbatim, and
continuous columns are normalized with the `standard score`_ normalization
technique. These tables are only partially normalized because they still
contain categorical data.

What is a standard score? In short:

*   Values are centered around zero.
*   The absolute value of a cell determines how many standard deviations it is
    away from the mean. For example, a cell that has a value of 2 is two
    standard deviations above the mean, and a cell that has a value of -2 is
    two standard deviations below the mean.

.. WARN:: This must be the same length as :data:`DATA_TABLES`.

.. _standard score: https://en.wikipedia.org/wiki/Standard_score
"""

assert len(DATA_TABLES) == len(STD_DATA_TABLES)

MEANS_TABLE: str = 'means'
"""The name of the database table containing means.

The name of the database table containing the means of the continuous columns
from the :data:`pp.constants.TRAINING_TABLE`.
"""

STD_DEVS_TABLE: str = 'std_devs'
"""The name of the database table containing sample standard deviations.

The name of the database table containing the sample standard deviations of the
continuous columns from the :data:`pp.constants.TRAINING_TABLE`.
"""

MODELS_TABLE: str = 'models'
"""Table containing linear equations that model columns.

A "model" is a linear equation that, given some input (independent) variables,
will predict an output (dependent) variable. This table contains models for
predicting a column given other columns.
"""

CATEGORICAL_TYPE: str = 'categorical'
"""The label used to refer to categorical data."""

CONTINUOUS_TYPE: str = 'continuous'
"""The label used to refer to continuous data."""

COLUMN_TYPES: Mapping[str, str] = {
    CATEGORICAL_TYPE: 'TEXT',
    CONTINUOUS_TYPE: 'NUMERIC',
}
"""A mapping from data types to column types.

Each column of data in the :data:`pp.constants.DATA_TABLES` is either
continuous or categorical data. This distiction is made because the two types
of data require different types of analysis. This mapping defines what SQLite
column types are used to represent the two types of data.
"""

TEST_SEED: int = 2
"""A seed to use when loading a dataset into the database.

Some of the functional tests load data into the database. Rows are assigned to
tables with a weighted random number generator. If only zero or one rows are
assigned to a table, then certain analyses (like standard deviation) will fail.
There are two ways to combat this: make the data sets larger, or control
row-to-table assignments. The former is problmatic in that small data sets are
nice for testing. Thus, the latter is preferred. This seed can be used to seed
the weighted random number generator.
"""

###############################################################################
# Other
###############################################################################

LAMBDA: float = 0.01
"""Used when calculating the cost of a model.

When comparing different models for predicting an attribute, the following
function is used::

    cost = error(model) + λ × complexity(model)

What do these terms mean?

model
    A linear equation which models a set of columns.

cost
    The figurative cost of using a specific linear equation. A model with a
    lower cost is better than a model with a higher cost.

error
    The inaccuracy of the model. In this case, a model which perfectly models a
    set of columns has an error of zero. A typical measure of error is sum of
    squared errors, divided by the number of data points.

complexity
    A measure of how complex a model is. Overly complex models run the risk of
    over-fitting the training data used to generate that model.

λ
    Lambda. A tunable constant used to adjust the cost of model complexity.
    Raising the value rewards simplicity; lowering the value rewards accuracy.

.. NOTE:: A user should be able to override this value via a user interface
    (like CLI).
"""
