#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import io
from qaviton.version import __version__ as version

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

from setuptools import setup


setup(
    name='qaviton',
    version=version,
    description='python implementation of qaviton',
    keywords=['qaviton'],
    author='Yehonadav Bar Elan',
    author_email='yehonadav@Qaviton.com',
    url='https://qaviton.com/',
    packages=['qaviton'],
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers, Testers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'Appium-Python-Client>=0.28',
        'selenium>=3.14.0',
        'Faker>=0.8.17',
        'keyboard>=0.13.2',
        'mouse>=0.7.0',
        'imageio>=2.3.0',
        'pytest>=3.7.1',
        'pytest-xdist>=1.22.5',
        'pytest-cov>=2.5.1',
        'pytest-ordering>=0.5',
        'pytest-forked>=0.2',
        'threaders>=0.2.12',
        'PyYAML>=3.13'
    ]
)
