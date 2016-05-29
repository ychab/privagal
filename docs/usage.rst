Usage
=====

Tokens
------

Generating tokens
`````````````````
All galleries are protected by a password set in the parent timeline page. The
default timeline's password is the one defined in the setting
``PRIVAGAL_TIMELINE_INITIAL_PASSWORD``.

If you want to avoid your visitors to remember this password, you can give
them a page link with a token instead.

By default, there is no token generated. You must do it in the Wagtail
backoffice at ``/admin``.

Once logged in, click on "settings" on the left sidebar and then click on the
*Token* icon. From this page, you can manage token (create/edit/delete).

.. note:: a key is generated for purpose when creating a new token

Using tokens
````````````
When you are in the Wagtail's backoffice (``/admin``) on the listing page of
galleries (``/admin/pages/add/gallery/gallery/3/``), you have a more page link
*Token link* available in the drop-down of a gallery when you hovering it.
Just copy the address to share it!

.. warning::
    For the moment, tokens have no expiration date. Thus, you may change it
    manually.

Forcing tokens authentification
```````````````````````````````
You can disable the password login page authentification by setting:

.. code-block:: python

    PRIVAGAL_AUTH_TOKEN_REQUIRED = True

Creating your first gallery
---------------------------

Log in into the Wagtail backoffice at ``/admin``. In the explorer section,
click on the *timeline* page. The timeline is the parent page of all galleries.

This is from this page that you will create sub-pages, the gallery's pages.
The direct url is ``/admin/pages/add/gallery/gallery/3/``.

From this page, just click on *Add a sub-page* to create a gallery. Don't
forgot to publish it (instead of saving it as a draft).

Then if you go the the frontend timeline page, you should see the gallery.

For more detail about Wagtail, you can take a look at the `Editor's guide`_.

.. _`Editor's guide`: http://docs.wagtail.io/en/latest/editor_manual/index.html

Demo
----

To have a quick overview, you can execute the following Django command to
generate some galleries::

    ./manage.py genfactories --limit=10 --purge

.. warning::
    The ``purge`` option will remove all previous galleries
