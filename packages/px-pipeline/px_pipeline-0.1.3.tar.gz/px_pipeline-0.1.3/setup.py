import os
import re
import setuptools


with open('README.md', 'r') as rf:
    with open('CHANGELOG.md', 'r') as cf:
        long_description = rf.read() + cf.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()

    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('px_pipeline')


setuptools.setup(
    name='px-pipeline',
    version=version,
    author='Alex Tkachenko',
    author_email='preusx.dev@gmail.com',
    license='MIT License',
    description='Pipeline runner.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    extras_require={
        'dev': (
            'pytest',
            'pytest-watch>=4.2,<5.0',
            'coverage==6.4.2',
            'twine',
        ),
    },
    packages=setuptools.find_packages(exclude=('tests', 'tests.*')),
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',

        'Programming Language :: Python :: 3',
        'Framework :: Django',

        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
