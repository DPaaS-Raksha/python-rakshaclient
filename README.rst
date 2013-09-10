Python bindings to the OpenStack Raksha API
===========================================

This is a client for the OpenStack Raksha API. There's a Python API (the
``rakshaclient`` module), and a command-line script (``raksha``). Each
implements 100% of the OpenStack Raksha API.

See the `OpenStack CLI guide`_ for information on how to use the ``raksha``
command-line tool. You may also want to look at the
`OpenStack API documentation`_.

.. _OpenStack CLI Guide: http://docs.openstack.org/cli/quick-start/content/
.. _OpenStack API documentation: http://docs.openstack.org/api/

The project is hosted on `Launchpad`_, where bugs can be filed. The code is
hosted on `Github`_. Patches must be submitted using `Gerrit`_, *not* Github
pull requests.

.. _Github: https://github.com/DPaaS-Raksha/python-rakshaclient
.. _Launchpad: https://launchpad.net/python-rakshaclient
.. _Gerrit: http://wiki.openstack.org/GerritWorkflow

This code a fork of `Jacobian's python-cloudservers`__ If you need API support
for the Rackspace API solely or the BSD license, you should use that repository.
python-rakshaclient is licensed under the Apache License like the rest of OpenStack.

__ http://github.com/jacobian/python-cloudservers

.. contents:: Contents:
   :local:

Command-line API
----------------

Installing this package gets you a shell command, ``raksha``, that you
can use to interact with any Rackspace compatible API (including OpenStack).

You'll need to provide your OpenStack username and password. You can do this
with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=openstack
    export OS_PASSWORD=yadayada
    export OS_TENANT_NAME=myproject

You will also need to define the authentication url with ``--os-auth-url``
and the version of the API with ``--version``.  Or set them as an environment
variables as well::

    export OS_AUTH_URL=http://example.com:8774/v1.1/
    export OS_VOLUME_API_VERSION=1

If you are using Keystone, you need to set the RAKSHA_URL to the keystone
endpoint::

    export OS_AUTH_URL=http://example.com:5000/v2.0/

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-region-name`` (or
``export OS_REGION_NAME``). It defaults to the first in the list returned.

You'll find complete documentation on the shell by running
``raksha help``::

    usage: raksha [--debug] [--os-username <auth-user-name>]
                  [--os-password <auth-password>]
                  [--os-tenant-name <auth-tenant-name>] [--os-auth-url <auth-url>]
                  [--os-region-name <region-name>] [--service-type <service-type>]
                  [--service-name <service-name>]
                  [--endpoint-type <endpoint-type>]
                  [--os-cacert <ca-certificate>] [--retries <retries>]
                  <subcommand> ...

    Command-line interface to the OpenStack Raksha API.

    Positional arguments:
      <subcommand>
        help                Display help about this program or one of its
                            subcommands.
        list-extensions     List all the os-api extensions that are available.

    Optional arguments:
      --debug               Print debugging output
      --os-username <auth-user-name>
                            Defaults to env[OS_USERNAME].
      --os-password <auth-password>
                            Defaults to env[OS_PASSWORD].
      --os-tenant-name <auth-tenant-name>
                            Defaults to env[OS_TENANT_NAME].
      --os-auth-url <auth-url>
                            Defaults to env[OS_AUTH_URL].
      --os-region-name <region-name>
                            Defaults to env[OS_REGION_NAME].
      --service-type <service-type>
                            Defaults to compute for most actions
      --service-name <service-name>
                            Defaults to env[RAKSHA_SERVICE_NAME]
      --endpoint-type <endpoint-type>
                            Defaults to env[RAKSHA_ENDPOINT_TYPE] or publicURL.
      --os-cacert <ca-certificate>
                            Specify a CA bundle file to use in verifying a TLS
                            (https) server certificate. Defaults to env[OS_CACERT]
      --retries <retries>   Number of retries.

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start using keystone::

    # use v2.0 auth with http://example.com:5000/v2.0/")
    >>> from rakshaclient.v1 import client
    >>> nt = client.Client(USER, PASS, TENANT, AUTH_URL, service_type="volume")
    >>> nt.volumes.list()
    [...]
