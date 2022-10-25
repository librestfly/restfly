RESTfly: Simplifying API Libraries
==================================

Release v\ |version|.

**RESTfly** (pronounced restfully) is a framework for building libraries to
easily interact with RESTful APIs.

.. image:: https://github.com/librestfly/restfly/actions/workflows/testing.yml/badge.svg
   :target: https://github.com/librestfly/restfly/actions/workflows/testing.yml
.. image:: https://github.com/librestfly/restfly/actions/workflows/deploy.yml/badge.svg
   :target: https://github.com/librestfly/restfly/actions/workflows/deploy.yml
.. image:: https://img.shields.io/pypi/v/restfly.svg
   :target: https://pypi.org/project/restfly/
.. image:: https://img.shields.io/pypi/pyversions/restfly.svg
.. image:: https://img.shields.io/pypi/dm/restfly.svg
   :target: https://pypistats.org/packages/restfly
.. image:: https://img.shields.io/github/license/librestfly/restfly.svg
   :target: https://github.com/librestfly/restfly/blob/master/LICENSE
.. image:: https://sonarcloud.io/api/project_badges/measure?project=librestfly_restfly&metric=alert_status
   :target: https://sonarcloud.io/summary/overall?id=librestfly_restfly


.. image:: https://live.staticflickr.com/2815/10007461563_a02f26528f_c.jpg

The User Guide
--------------

This part of the documentation focuses on walking through usage of the library
in a step-by-step manner.

.. note::

    Please note that this section of the documentation is currently still being
    constructed, and should not be considered a complete walkthrough.

.. toctree::
    :maxdepth: 4

    user/intro
    user/install
    user/gettingstarted
    user/pagination


The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is what you're looking for.

.. toctree::
    :glob:

    api/*

Libraries Using RESTfly
-----------------------

RESTfly is a fairly new library based on the work of `Steve McGrath`_ within
the pyTenable project.  There are several other projects also leveraging
RESTfly listed below:

- `pyCheckpoint-API <https://github.com/LetMeR00t/pyCheckpoint-API>`_
- `python-Cybereason <https://github.com/psmiraglia/python-cybereason>`_
- `pyTenable <https://github.com/tenable/pyTenable>`_
- `pyZScaler <https://github.com/mitchos/pyZscaler>`_
- `python-SecurityTrails <https://github.com/SteveMcGrath/python-sectrails-lib>`_
- Various Tenable integrations:
  - `Azure Security Center Integration <https://github.com/tenable/integration-asc>`_
  - `Google CSCC Integration <https://github.com/tenable/integration-cscc>`_
  - `Jira Cloud Integration <https://github.com/tenable/integration-jira-cloud>`_
  - `Tenable.asm Asset Importer <https://github.com/tenable/asm-asset-importer>`_

.. _Steve McGrath: https://github.com/stevemcgrath
.. _pyTenable: https://pytenable.readthedocs.io
