from setuptools import setup, find_packages

setup(
    name='dep-mismatch',
    version='0.0.1',
    author='Jeremy Audet',
    license='public domain',
    packages=find_packages(),
    install_requires=['python-dateutil<2.8.1'],
    extras_require={
        'dev': [
            'pylint',
        ],
    },
    entry_points={
        'console_scripts': [
            'dep-mismatch = dep_mismatch.__init__:main',
        ],
    },
)
