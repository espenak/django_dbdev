from setuptools import setup, find_packages


setup(
    name = 'dbdev_testproject',
    description = 'Test project for django_dbdev.',
    license='BSD',
    version = '1.0',
    packages=find_packages(exclude=[]),
    install_requires = [
        'Django',
    ],
    include_package_data=True,
    zip_safe=False
)
