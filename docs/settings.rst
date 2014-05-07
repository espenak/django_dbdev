########
Settings
########

django_dbdev is configured using Django settings. The following settings is available.


.. currentmodule:: django.conf.settings


***********************
Common for all backends
***********************

.. data:: DBDEV_DATADIR

    The directory where we store the data for django_dbdev. Each
    backend creates its own subdirectory where they store settings,
    database-data etc. We also store backups in subdirectories of
    this directory.

    Defaults to ``dbdev_tempdata``.



************************
Posgres backend settings
************************

.. data:: DBDEV_POSTGRES_EXECUTABLE

    Path to the ``postgres`` executable.
    Defaults to ``postgres``.


.. data:: DBDEV_POSTGRES_PG_CTL_EXECUTABLE

    Path to the ``pg_ctl`` executable.
    Defaults to ``pg_ctl``.


.. data:: DBDEV_POSTGRES_PSQL_EXECUTABLE

    Path to the ``psql`` executable.
    Defaults to ``psql``.


.. data:: DBDEV_POSTGRES_CREATEDB_EXECUTABLE

    Path to the ``createdb`` executable.
    Defaults to ``createdb``.