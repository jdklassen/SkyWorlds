from setuptools import setup

setup(
    name='skyworlds',
    version='1.0',
    description='OpenShift App for the SkyWorlds Game',
    author='Josiah Klassen',
    author_email='jkla@telus.net',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=[
        'Django>=1.8.3',
        'psycopg2==2.6.1',
    ],
)
