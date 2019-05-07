from setuptools import setup, find_packages


long_description = 'Please refer to https://restfly.readthedocs.io'

setup(
    name='restfly',
    version='1.0.2',
    description='A library to make API wrappers creation easier',
    author='Steve McGrath',
    long_description=long_description,
    author_email='steve@chigeek.com',
    url='https://github.com/stevemcgrath/restfly',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
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