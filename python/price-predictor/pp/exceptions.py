# coding=utf-8
"""Custom exeptions."""


class DatabaseAlreadyExistsError(Exception):
    """Indicates that a database already exists when it shouldn't.

    This might be raised if this application is asked to create a new database
    and one already exists.
    """


class DatabaseCPOPError(Exception):
    """An error occurred while creating or populating the database."""


class DatabaseNotFoundError(Exception):
    """Indicates that the database can't be found."""


class DatasetInstallError(Exception):
    """Indicates that a dataset can't be installed."""


class DatasetNotFoundError(Exception):
    """Indicates that a requested dataset can't be found."""


class DatasetParsingError(Exception):
    """Indicates an error occurred while parsing a dataset."""


class MissingValueError(Exception):
    """Indicates requested value is absent."""


class ModelingError(Exception):
    """Indicates a model can't be solved."""


class PredictionError(Exception):
    """Indicates an output column can't be predicted."""
