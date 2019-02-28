# coding=utf-8
"""Tools for working with datasets."""
import abc
import csv
import importlib
import os
import pkgutil
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePath
from typing import List, Mapping, Optional

from xdg import BaseDirectory

from pp import exceptions
from pp.constants import ARCHIVES_DIR, DATASETS_DIR, DATA_FILE, METADATA_FILE


class DS(abc.ABC):
    """A dataset.

    A dataset is a collection of house sale records. A dataset is "installed"
    if it has been extracted, cleaned up and copied to one of
    ``${{XDG_DATA_DIRS}}/{DATASETS_DIR}``. The only supported real-world
    dataset is "House Sales in `King County`_, USA."

    .. _King County: https://www.kaggle.com/harlfoxem/housesalesprediction
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return this dataset's name.

        This name is used when generating filesystem path names. As a result,
        it's strongly recommended to use a restricted set of characters, such
        as ``a-zA-Z-_.``.
        """

    @abc.abstractmethod
    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        The exact procedure for installing a dataset varies depending on the
        dataset at hand. Subclasses (which represent specific datasets) must
        provide this logic. As an example, a subclass might implement the
        following installation procedure:

        1. Check if the dataset is already installed. If so, return. (See
           :func:`pp.datasets.installed`.)
        2. If an ``archive`` hasn't been provided, download one into an
           :data:`pp.constants.ARCHIVES_DIR`.
        3. Extract the archive into a :data:`pp.constants.DATASETS_DIR`.

        :param archive: The path to a archive containing the dataset.
        """

    def installed(self) -> bool:
        """Tell whether this dataset is installed.

        :return: True if this dataset is installed, false otherwise.
        """
        try:
            self.install_path()
        except exceptions.DatasetNotFoundError:
            return False
        return True

    def install_path(self) -> Path:
        """Return the path to where this dataset is installed.

        :return: The path to where this dataset is installed.
        :raise pp.exceptions.DatasetNotFoundError: If the dataset is not
            installed.
        """
        importlib.reload(BaseDirectory)
        for datasets_dir in BaseDirectory.load_data_paths(DATASETS_DIR):
            candidate_path = Path(datasets_dir, self.name)
            if candidate_path.exists():
                return candidate_path
        raise exceptions.DatasetNotFoundError(
            f"Dataset {self.name} isn't installed."
        )

    def uninstall(self) -> None:
        """Uninstall this dataset.

        :raise pp.exceptions.DatasetNotFoundError: If the dataset to uninstall
            is not currently installed.
        """
        shutil.rmtree(self.install_path())


class FixtureDS(DS):  # pylint:disable=abstract-method
    """An abstract base class for fixture datasets."""

    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        :param archive: **Ignored.**
        :raise DatasetInstallError: If this dataset is already installed; or if
            unable to locate or load the package containing this dataset's
            files.
        """
        if self.name in installed():
            raise exceptions.DatasetInstallError(
                f'{self.name} already installed.'
            )
        importlib.reload(BaseDirectory)
        dst = Path(BaseDirectory.save_data_path(DATASETS_DIR), self.name)
        assert not dst.exists()

        # Prepare files, then atomically install.
        tmp = tempfile.mkdtemp()
        try:
            for basename in (DATA_FILE, METADATA_FILE):
                in_path = PurePath('static', self.name, basename)
                in_data = pkgutil.get_data('pp', str(in_path))
                if in_data is None:
                    raise exceptions.DatasetInstallError(
                        f"Can't locate or load package containing {in_path}."
                    )
                out_path = Path(tmp, basename)
                with open(out_path, 'wb') as handle:
                    handle.write(in_data)
            shutil.move(tmp, dst)
        except:
            shutil.rmtree(tmp)
            raise


class FixtureSimpleDS(FixtureDS):
    """A simple valid fixture."""

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'fixture-simple'


class FixtureColumnNameMismatchDS(FixtureDS):
    """An invalid fixture.

    There is a column name mismatch between :data:`pp.constants.DATA_FILE` and
    :data:`pp.constants.METADATA_FILE`.
    """

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'fixture-column-name-mismatch'


class FixtureMissingFileDS(FixtureDS):
    """A bogus dataset, for testing purposes.

    :data:`pp.constants.METADATA_FILE` is missing.
    """

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'fixture-missing-file'


class KingCountyDS(DS):
    """The `King County`_ dataset.

    .. _king county: https://www.kaggle.com/harlfoxem/housesalesprediction
    """

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'king-county'

    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        :param archive: The path to a zip archive containing the dataset.
        :raise DatasetInstallError: If this dataset is already installed, or if
            no ``archive`` is provided.
        """
        if self.name in installed():
            raise exceptions.DatasetInstallError(
                f'{self.name} already installed.'
            )
        importlib.reload(BaseDirectory)
        dst_dir = Path(BaseDirectory.save_data_path(DATASETS_DIR), self.name)

        # Munge and atomically install the dataset.
        if not archive:
            archive = self.__get_cached_archive()
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            with zipfile.ZipFile(archive, 'r') as handle:
                handle.extractall(tmp_dir)
            self.__create_data_file(tmp_dir)
            self.__create_metadata_file(tmp_dir)
            shutil.move(tmp_dir, dst_dir)
        except:
            shutil.rmtree(tmp_dir)
            raise

    def __get_cached_archive(self) -> Path:
        archive = Path(
            BaseDirectory.xdg_cache_home,
            ARCHIVES_DIR,
            self.name + '.zip',
        )
        if not archive.exists():
            raise exceptions.DatasetInstallError(
                'No archive explicitly provided, and none found at '
                f"{archive}. Can't install this dataset."
            )
        return archive

    @staticmethod
    def __create_data_file(tmp_dir: Path) -> None:
        """Create the data file from ``kc_house_data.csv``."""
        in_path = Path(tmp_dir, 'kc_house_data.csv')
        out_path = Path(tmp_dir, DATA_FILE)
        with open(in_path) as in_handle:
            with open(out_path, 'w') as out_handle:
                reader = csv.reader(in_handle)
                writer = csv.writer(out_handle)

                # header row
                row: List[str] = next(reader)
                row.pop(0)  # id column
                row.pop(0)  # date column
                row = ['year', 'month', 'day'] + row
                writer.writerow(row)

                # data rows
                date_matcher = re.compile(r'^(\d{4})(\d{2})(\d{2})T\d{6}$')
                for row in reader:
                    row.pop(0)  # id column
                    date = row.pop(0)
                    match = date_matcher.match(date)  # date column
                    if match is None:
                        raise exceptions.DatasetInstallError(
                            f'Malformed date found in {in_path}: {date}'
                        )
                    row = [match.group(i) for i in range(1, 4)] + row
                    writer.writerow(row)
        os.unlink(in_path)

    def __create_metadata_file(self, tmp_dir: Path) -> None:
        """Create the metadata file."""
        in_path = PurePath('static', self.name, METADATA_FILE)
        in_data = pkgutil.get_data('pp', str(in_path))
        if in_data is None:
            raise exceptions.DatasetInstallError(
                f"Can't find asset for {self.name}. Please contact the "
                'developers.'
            )
        out_path = Path(tmp_dir, METADATA_FILE)
        with open(out_path, 'wb') as handle:
            handle.write(in_data)


class FixtureKingCountyDS(KingCountyDS):
    """A snippet of the King County dataset.

    If you wish to analyze the King County dataset, please use
    :class:`pp.datasets.KingCountyDataset`. This dataset exists for testing
    purposes. More specifically, :meth:`pp.datasets.KingCountyDataset.install`
    is complex, and this dataset exists so that functional tests can push a
    small amount of data through that method without needing to download any
    data.
    """

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'fixture-king-county'

    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset."""
        with tempfile.NamedTemporaryFile() as tmp:
            with zipfile.ZipFile(tmp, 'x') as handle:
                in_path = PurePath('static', self.name, DATA_FILE)
                in_data = pkgutil.get_data('pp', str(in_path))
                if in_data is None:
                    raise exceptions.DatasetInstallError(
                        f"Can't find asset for {self.name}. Please contact the "
                        'developers.'
                    )
                handle.writestr('kc_house_data.csv', in_data)
            super().install(Path(tmp.name))


class FixtureKingCountyMalformedDateDS(FixtureKingCountyDS):
    """A malformed version of :class:`pp.datasets.KingCountyFixtureDS`."""

    @property
    def name(self) -> str:
        """Return this dataset's name."""
        return 'fixture-king-county-malformed-date'


def installed() -> Mapping[str, Path]:
    """Get currently installed datasets.

    :return: A mapping in the form ``{dataset_name: dataset_path}``.
    """
    result = {}
    importlib.reload(BaseDirectory)
    for datasets_dir in BaseDirectory.load_data_paths(DATASETS_DIR):
        for dataset_dir in Path(datasets_dir).glob('*'):
            result[dataset_dir.name] = dataset_dir
    return result


def manageable() -> Mapping[str, DS]:
    """Get manageable datasets.

    :return: A mapping in the form ``datset_name: dataset_obj}``.
    """
    return {obj.name: obj for obj in (
        FixtureColumnNameMismatchDS(),
        FixtureKingCountyDS(),
        FixtureKingCountyMalformedDateDS(),
        FixtureMissingFileDS(),
        FixtureSimpleDS(),
        KingCountyDS(),
    )}
