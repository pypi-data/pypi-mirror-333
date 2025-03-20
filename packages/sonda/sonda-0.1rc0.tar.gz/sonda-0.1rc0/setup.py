# Create a simple setup.py file to install the package call sonda

from setuptools import setup

setup(
    name='sonda',
    version='0.1rc',
    packages=['sonda'],
    entry_points={
        'console_scripts': [
            'sonda = sonda.__main__:main'
        ]
    })