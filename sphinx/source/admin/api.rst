API
===

.. toctree::

Description: :doc:`/technical/api`

**Public** (default=off)
------------------------

    * If turned off, the API can still be accessed by

        * A browser used by a logged in user
        * A request is using a :ref:`valid token`
        * If the IP of the request-computer is on the **IP Whitelist**

    * If turned on the API and linked files with a license can be accessed without being logged in. This might be useful if you want to allow other systems to use your data without restrictions.


**API token**
-------------

API Tokens can be created to query the API if it is turned off. Only Admins
are allowed to create, revoke and delete tokens. Available options are:

    * **Generate**: :ref:`generate` a new token
    * **Revoke all tokens**: Revoke all available tokens
    * **Authorize all tokens**: All revoked tokens will be valid again
    * **Delete revoked tokens**: All revoked tokens will be deleted
    * **Delete invalid tokens**: All invalid tokens will be deleted (see :ref:`valid token`)

.. _valid token:

**Valid token**
*****************

A token is valid if:

    * **valid from** is greater than current date
    * **revoked** is *false*, meaning the token is not revoked
    * :doc:`/admin/user` is active

.. _generate:

**Generate**
************

* **Expiration**:
    Set how long a token is valid. Entered numbers are days. 0 means no expiration date.
* **Token name**:
    To better distinguish between tokens, a individual name can be entered.
* **User**:
    Select a :doc:`/admin/user` for which the token will be created.

After the *Generate* button is clicked, the site will reload and a grey box appears.
In this box the token string will be visible and is copied on click.

**Be aware**, this is the only time, the token will be visible!
