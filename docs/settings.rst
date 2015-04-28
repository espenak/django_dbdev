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


.. data:: DBDEV_POSTGRES_PG_DUMP_EXECUTABLE

    Path to the ``pg_dump`` executable.
    Defaults to ``pg_dump``.

.. data:: DBDEV_POSTGRES_PORT

    The port to bind the postgres server to. Defaults to ``20021``.


**********************
MySQL backend settings
**********************

.. data:: DBDEV_MYSQL_INSTALL_DB_EXECUTABLE

    Path to the ``mysql_install_db`` executable.
    Defaults to ``mysql_install_db``.

.. data:: DBDEV_MYSQLD_EXECUTABLE

    Path to the ``mysqld_safe`` executable.
    Defaults to ``mysqld_safe``.

.. data:: DBDEV_MYSQLADMIN_EXECUTABLE

    Path to the ``mysqladmin`` executable.
    Defaults to ``mysqladmin``.

.. data:: DBDEV_MYSQL_EXECUTABLE

    Path to the ``mysql`` executable.
    Defaults to ``mysql``.

.. data:: DBDEV_MYSQLDUMP_EXECUTABLE

    Path to the ``mysqldump`` executable.
    Defaults to ``mysqldump``.

.. data:: DBDEV_MYSQL_BASEDIR

    The path to the mysql *basedir* (where mysql default data is installed).
    You may have to set this if your MySQL/MariaDB is not configured correctly.

    Can also be set as an environment variable, which is probably a better
    choice for projects with more than one developer.

    Defaults to ``None``.

.. data:: DBDEV_MYSQL_PORT

    The port to bind the mysql server to. Defaults to ``20022``.
