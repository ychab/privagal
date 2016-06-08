Deployment
==========

Backend
-------

The deployment is the same as any other Wagtail projects:

1.  install required system packages. For example on Debian::

        apt-get install python3 python3-dev postgresql-9.4 libpq-dev virtualenv libjpeg-dev zlib1g-dev

    .. note::
        Please note that Wagtail needs ``Pillow`` librarie which needs
        *libjpeg* and *zlib* libraries.

2.  create a PostgreSQL database in a cluster with role and owner

3.  create a virtualenv::

        virtualenv <NAME> -p python3

4.  install dependencies with pip depending on your environment (i.e :
    production or local or test). For example::

        pip install -r requirements/production.txt  # For production

5.  override the settings by copying ``privagal/settings/local.dist`` to
    ``privagal/settings/local.py`` and editing it::

        cp privagal/settings/local.dist privagal/settings/local.py

    The following *Django* settings are **required**:

        * ``SECRET_KEY``
        * ``DATABASES``
        * ``ALLOWED_HOSTS``

    And the following *Privagal* settings are **required**:

        * ``PRIVAGAL_TIMELINE_INITIAL_PASSWORD``: a password to access the timeline, i.e: could be changed later
        * ``PRIVAGAL_SITE_HOSTNAME``: the hostname of the site

    All other settings are here for purpose only.

6.  on production, export the ``DJANGO_SETTINGS_MODULE`` to easily use the
    ``manage.py`` with the proper production setting. For example, export it in
    a ``.bashrc`` file to be persistent::

        export DJANGO_SETTINGS_MODULE="privagal.settings.production"

    .. warning::
        Don't forgot to reload it with::

            source ~/.bashrc

7.  on production, execute the Django check command and apply fixes if needed::

        ./manage.py check --deploy

8.  import the SQL schema::

        ./manage.py migrate

9.  create a super user::

        ./manage.py createsuperuser

.. note::
    ``wsgi.py`` script will use the ``production.py`` settings, whereas
    ``manage.py`` will use the ``local.py`` by default.

Frontend
--------
On production, you will need at least `Bower`_ to install JS libraries. The
easier way to have it is to install it with npm.

1.  install `npm`_ (embed with nodejs)

2.  install Bower from the project root directory::

        npm install --production

3.  install JS libraries with `Bower`_ from project root directory too::

        ./node_modules/bower/bin/bower install --production

4.  re-active virtualenv if needed and collect statics files::

        ./manage.py collectstatic

.. note::
    Of course in development, omit the ``--production``

.. _`Bower`: http://bower.io
.. _`npm`: https://www.npmjs.com

Development
```````````

`Gulp`_ is used to build dist files.

By default, it will compile and minified JS and LESS files::

    ./node_modules/gulp/bin/gulp.js

Because executing it every time is painful, you can watch changes with the
following command::

    ./node_modules/gulp/bin/gulp.js watch

.. _`Gulp`: http://gulpjs.com/

Internationalization
--------------------

For the moment, there is only support for French. Any contributions are
welcome!

Settings
````````
In ``privagal.settings.local`` settings file, don't forgot to set
``LANGUAGE_CODE`` to the desired language.

Compiling
`````````
Translations must be compiled to be used. To do so, execute the following
commands from the project root directory::

    cd privagal  # go to this sub-folder to avoid compiling other Python files!
    ../manage.py compilemessages


Serving private files
---------------------

Private files are delivered with the `django-sendfile`_ app. You are strongly
encourage to use Nginx (other backends are untested). Thus, Nginx is the
default backend assume in ``privagal.settings.production`` and you may take a
look at `its documentation`_ for more detail.

.. _`django-sendfile`: https://github.com/johnsensible/django-sendfile

.. _`its documentation`: https://github.com/johnsensible/django-sendfile#nginx-backend

In this project, the whole directory ``media`` **must** be protected. If you
keep the default nginx configuration set in ``privagal.settings.production``,
you must set a similar entry in your nginx conf::

    location /protected/ {
        internal;
        alias /<PATH>/media;
    }
