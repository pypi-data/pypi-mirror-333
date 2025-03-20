import os

from setuptools import find_packages
from setuptools import setup


def read(path):
    with open(os.path.join(path)) as f:
        return f.read()


setup(
    name='z3c.recipe.compattest',
    version='3.0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description='Buildout recipe to create testrunners for testing '
                'compatibility with other packages',
    url='https://github.com/zopefoundation/z3c.recipe.compattest',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/'
                          'z3c.recipe.compattest/issues'),
        'Sources': 'https://github.com/zopefoundation/z3c.recipe.compattest',
    },
    long_description=(
        read('README.rst')
        + '\n\n'
        + read('CHANGES.rst')
    ),
    keywords="zope setuptools egg kgs",
    classifiers=[
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    license='ZPL-2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout >= 2.0.0',
        'zc.recipe.testrunner >= 2.0.0',
    ],
    extras_require={
        'test': [
            # zope.dottedname is just used as a dummy package to demonstrate
            # things with, it's not actually imported
            'zope.dottedname',
            'zope.testing',
            'manuel',
        ],
    },
    entry_points={
        'zc.buildout': ['default = z3c.recipe.compattest.recipe:Recipe'],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
)
