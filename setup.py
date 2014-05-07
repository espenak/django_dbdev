from setuptools import setup, find_packages

execfile('django_dbdev/version.py')


setup(
    name = 'django_dbdev',
    description = 'Makes it easy to create and manage databases during development.',
    license='BSD',
    version = __version__,
    url = 'http://github.com/espenak/django_dbdev',
    author = 'Espen Angell Kristiansen',
    long_description='See https://github.com/espenak/django_dbdev',
    packages=find_packages(exclude=[]),
    install_requires = [
        'Django',
        'sh'
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
