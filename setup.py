from setuptools import setup

setup(
    name='folio_curl',
    version='0.1.0',
    description='A command-line tool that wraps curl and adds some convenience features for working with FOLIO APIs',
    py_modules=['folio_curl'],
    install_requires=[
        'requests',
    ],
    entry_points={'console_scripts': ['folio_curl=folio_curl:main']},
)
