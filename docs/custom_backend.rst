##############
Custom backend
##############

.. currentmodule:: django_dbdev.backends.base


Implementing a backend requires you to extend :class:`.BaseDbdevBackend` and override/implement the following methods:

- :meth:`.BaseDbdevBackend.init`
- :meth:`.BaseDbdevBackend.destroy`
- :meth:`.BaseDbdevBackend.run_database_server_in_foreground`
- :meth:`.BaseDbdevBackend.start_database_server`
- :meth:`.BaseDbdevBackend.stop_database_server`
- :meth:`.BaseDbdevBackend.backup`
- :meth:`.BaseDbdevBackend.restore`
- :meth:`.BaseDbdevBackend.serverinfo`

You must also:

- Create a template that the :meth:`.BaseDbdevBackend.guide` method can use.
- Add a DBSETTINGS dict to the module containing your backend (see the other backends).



Register your backend
=====================
You must register your backend some place that is always executed when Django
starts up. The most natural place is in your development ``settings.py``. Lets
say you have implemented an Oracle backend, you need to tell django_dbdev to use
your dbdev backend for the ``django.db.backends.oracle`` engine like this::

    from django_dbdev import backendregistry

    from mypackage.dbdev_backends.oracle import OracleBackend

    backendregistry.register('django.db.backends.oracle', OracleBackend)

.. note::

    You can replace the built in backends this way too. The registry is a dict
    mapping engine string to backend class, so registering a custom backend for
    an engine with a built in backend (like ``django.db.backends.mysql``) does
    not raise any errors.



BaseDbdevBackend docs
=====================

.. autoclass:: BaseDbdevBackend
    :members: