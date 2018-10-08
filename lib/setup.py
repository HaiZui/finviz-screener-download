# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='invest_dw',
    version='0.1.0',
    description='Data warehousing module for trading and investing',
    url='https://github.com/HaiZui/invest-dw',
    author='Teemu Parviainen',
    author_email='parviainen.teemu@gmail.com',
    license='Teemu Parviainen',
    classifiers=[
    ],

    # What does your project relate to?
    keywords='dw',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages=find_packages(),


    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pandas', 'numpy', 'datetime', 'mysql', 'bs4',],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]

)