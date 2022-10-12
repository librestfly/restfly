'''
RESTfly Package
'''
from setuptools import setup, find_packages

with open('restfly/version.py', 'r') as vfile:  # noqa PLW1514
    exec(vfile.read())  # noqa PLW0122

with open('README.rst', 'r') as ldfile:  # noqa PLW1514
    long_description = ldfile.read()

setup(
    name='restfly',
    version=VERSION,  # noqa: F821,PLE0602
    description=DESCRIPTION,  # noqa: F821,PLE0602
    author=AUTHOR,  # noqa: F821,PLE0602
    long_description=long_description,
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
