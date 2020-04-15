from setuptools import setup, find_packages


long_description = '''
RESTfly: Simplifying API Libraries
==================================

**RESTfly** (pronounced restfully) is a framework for building libraries to
easily interact with RESTful APIs.

.. image:: https://travis-ci.org/SteveMcGrath/restfly.svg?branch=master
   :target: https://travis-ci.org/SteveMcGrath/restfly
.. image:: https://img.shields.io/pypi/v/restfly.svg
   :target: https://pypi.org/project/restfly/
.. image:: https://img.shields.io/pypi/pyversions/restfly.svg
.. image:: https://img.shields.io/pypi/dm/restfly.svg
.. image:: https://img.shields.io/github/license/stevemcgrath/restfly.svg
   :target: https://github.com/SteveMcGrath/restfly/blob/master/LICENSE


.. image:: https://restfly.readthedocs.io/en/latest/_static/logo.png

RESTfly is a simple library designed to provide the scaffolding to make API
interaction libraries for just about any RESTful API.  With an emphasis on
simplicity and readability of the resulting library code thats written, the
idea here is provide something that is not only useful for folks to use, but
can also serve as a reference implimentation of the given APIs.

Please refer to the full documentation at https://restfly.readthedocs.io.
'''

setup(
    name='restfly',
    version='1.2.0',
    description='A library to make API wrappers creation easier',
    author='Steve McGrath',
    long_description=long_description,
    author_email='steve@chigeek.com',
    url='https://github.com/stevemcgrath/restfly',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tenable tenable_io securitycenter containersecurity',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'requests>=2.19',
    ],
)