from setuptools import setup, find_packages
import esus

setup(
    name = 'esus',
    version = esus.__versionstr__,
    description = 'Esus', # TODO: REPLACE
    long_description = '\n'.join((
        'Esus',
        '',
        'discussion software for Django',
    )),
    author = 'Lukáš Linhart',
    author_email='bugs@almad.net',
    license = 'BSD', # TODO: REPLACE
    url='http://git.netcentrum.cz/projects/django/GIT/esus/', # TODO: REPLACE

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    # TODO: REPLACE
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'setuptools>=0.6b1',
    ],
)

