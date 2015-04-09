####################
Develop django_dbdev
####################


************************
Install the requirements
************************
Install the following:

#. Python:)
#. PIP_
#. VirtualEnv_
#. virtualenvwrapper_
#. MySQL (you will need the development headers to build the Python module)
#. PostgreSQL (you will need the development headers to build the Python module)


***********************************************
Install required Python modules in a virtualenv
***********************************************
Create a virtualenv::

    $ mkvirtualenv django_dbdev

Install the development requirements::

    $ cd djangoproject/
    $ pip install -r requirements_development.txt



********************
Run the test project
********************

Navigate to the testproject::

    $ cd dbdev_testproject/

Test with postgres using::

    $ DJANGO_SETTINGS_MODULE=dbdev_testproject.develop.settings.postgres python manage.py

Test with mysql using::

    $ DJANGO_SETTINGS_MODULE=dbdev_testproject.develop.settings.mysql python manage.py



**************
Submit a patch
**************
#. Fork the `GitHub repository <https://github.com/espenak/django_dbdev>`_.
#. If you are making a major change, you should create an issue where you explain the change and the motivation. This will make it far less likely that the patch will be rejected.
#. When the patch is ready, send a pull request to ``espenak``.


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
