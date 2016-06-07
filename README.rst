.. image:: https://travis-ci.org/ychab/privagal.svg
    :target: https://travis-ci.org/ychab/privagal

.. image:: https://coveralls.io/repos/ychab/privagal/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/ychab/privagal?branch=master

.. image:: https://requires.io/github/ychab/privagal/requirements.svg?branch=master
   :target: https://requires.io/github/ychab/privagal/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://readthedocs.org/projects/privagal/badge/?version=latest
    :target: http://privagal.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

Privagal
========

Overview
--------

Privagal (a.k.a private gallery) is a Web application to help you sharing your
private pictures.

Its basic usage is to have a site manager which create galleries and share them
in further ways :

* by giving a link to the page with a token
* by giving a password to fill in the form by the visitor

To have a quick and easy workflow, the following rules are applied:

* accessing to a page give a full access to all other pages
* no user account are required

All galleries are displayed on a main listing page : the timeline. From this
scrollable timeline (ajax), the galleries could be filtered (for e.g by title).
Then user can click on an gallery to see it in detail.

Behind the scene
----------------

This application aims to be minimalist. Thus, its source code is quite simple
and is mainly a glue codes between the following technologies:

* Backend:

    *   `Wagtail`_ CMS to manage pages and images of your galleries
    *   `django-sendfile`_ app to use differents backends to serve private
        images (`Xsendfile`_ with Apache or `X-Accel`_ with Nginx)

* Frontend :

    *   `Bootstrap`_ for theming
    *   `Packery`_ to have a funny layout for images
    *   `Infinite Ajax Scroll`_ to replace classic pager

.. _`Wagtail`: https://wagtail.io/
.. _`django-sendfile`: https://github.com/johnsensible/django-sendfile

.. _`Xsendfile`: https://tn123.org/mod_xsendfile/
.. _`X-Accel`: https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/

.. _`Bootstrap`: http://getbootstrap.com/
.. _`Packery`: http://packery.metafizzy.co/
.. _`Infinite Ajax Scroll`: http://infiniteajaxscroll.com/

Documentation
-------------

All documentation is available at http://privagal.readthedocs.org.
