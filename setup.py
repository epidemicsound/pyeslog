from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='pyeslog',
    version='0.0.1',
    description='Standard logging module',
    license='MIT',
    long_description=long_description,
    url='https://github.com/epidemicsound/pyeslog.git',
    packages=['eslog'],
    install_requires=['structlog']
)
