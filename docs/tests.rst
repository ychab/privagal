Tests
=====

Using Tox
---------

You can use `Tox`_. You need to install it globally (generally, use *pip* as
root user) and execute it from the project root directory::

    tox

.. _`Tox`: http://tox.readthedocs.org

Manually
--------

1.  install dependencies if not using ``requirements/test.txt``::

        pip install -r requirements/test.txt

2.  then execute tests::

        ./manage.py test --settings=privagal.settings.test privagal
