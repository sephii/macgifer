#!/usr/bin/env python
from setuptools import find_packages, setup


install_requires = [
    'click>=6.0',
    'dropbox>=3.41',
    'requests>=2.9.1',
    'xerox>=0.4.1',
]


setup(
    name='macgifer',
    version='1.0.0',
    packages=find_packages(),
    description='MacGifer',
    author='Sylvain Fankhauser',
    author_email='sylvain.fankhauser@liip.ch',
    url='https://github.com/sephii/macgifer',
    install_requires=install_requires,
    license='wtfpl',
    tests_require=[],
    include_package_data=False,
    package_data={
    },
    entry_points={
        'console_scripts': 'macgifer = macgifer.commands:cli'
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
