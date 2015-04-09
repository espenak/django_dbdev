import sys
from setuptools import setup, find_packages


if sys.version_info[0] == 2:
    execfile('django_dbdev/version.py')
else:
    exec(open('django_dbdev/version.py', 'r').read())


long_description = """
Do you want to make it easy to create and setup isolated
Postgres or MySQL database servers during development
of your Django project?

See https://github.com/espenak/django_dbdev
"""

setup(
    name = 'django_dbdev',
    description = 'Makes it easy to create and manage databases during development.',
    license='BSD',
    version = __version__,
    url = 'http://github.com/espenak/django_dbdev',
    author = 'Espen Angell Kristiansen',
    author_email='post@espenak.net',
    long_description=long_description,
    packages=find_packages(exclude=['dbdev_testproject']),
    install_requires = [
        'Django',
        'sh',
        'future'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
