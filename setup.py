'''
RESTfly Package
'''
from setuptools import setup, find_packages

with open('restfly/version.py', 'r') as vfile:  # noqa PLW1514
    exec(vfile.read())  # noqa PLW0122

long_description = '''
RESTfly: Simplifying API Libraries
==================================

**RESTfly** (pronounced restfully) is a framework for building libraries to
easily interact with RESTful APIs.

.. image:: https://travis-ci.org/librestfly/restfly.svg?branch=master
   :target: https://travis-ci.org/librestfly/restfly
.. image:: https://img.shields.io/pypi/v/restfly.svg
   :target: https://pypi.org/project/restfly/
.. image:: https://img.shields.io/pypi/pyversions/restfly.svg
.. image:: https://img.shields.io/pypi/dm/restfly.svg
.. image:: https://img.shields.io/github/license/librestfly/restfly.svg
   :target: https://github.com/librestfly/restfly/blob/master/LICENSE
.. image:: https://sonarcloud.io/api/project_badges/measure?project=librestfly_restfly&metric=alert_status
   :target: https://sonarcloud.io/summary/overall?id=librestfly_restfly


.. image:: https://restfly.readthedocs.io/en/latest/_static/logo.png

RESTfly is a simple library designed to provide the scaffolding to make API
interaction libraries for just about any RESTful API.  With an emphasis on
simplicity and readability of the resulting library code thats written, the
idea here is provide something that is not only useful for folks to use, but
can also serve as a reference implementation of the given APIs.

Please refer to the full documentation at https://restfly.readthedocs.io.
'''  # noqa E501

setup(
    name='restfly',
    version=VERSION,  # noqa: F821,PLE0602
    description='A library to make API wrappers creation easier',
    author='Steve McGrath',
    long_description=long_description,
    author_email='steve@chigeek.com',
    url='https://github.com/librestfly/restfly',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='rest api library',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'requests>=2.26.0',
        'python-box>=5.3.0',
        'arrow>=1.0.3',
    ],
)
