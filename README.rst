Qaviton
=======

The first open source project to facilitate a unified testing automation framework for Web, Mobile & IoT
with Machine Learning, AI and much more: https://www.qaviton.com

Inspired by Appium & Selenium, Qaviton is a play on words for Graviton.
In theories of quantum gravity, the graviton
is the hypothetical elementary particle that mediates the force of gravity.
Qaviton is like the Graviton in the sense that if it exists,
it will be the solution to a fundamental problem in its field.

Qaviton offers an easy framework to automate tests that can run against any driver or any testing scenario,
and is meant to be like the React Native of software testing.


Installing
----------

make sure you have python 3.7+ installed.

we recommend using venv:

.. code-block:: text

    python -m venv venv
    source venv/bin/activate || venv\\Scripts\\activate

Install and update using `pip`_:

.. code-block:: text

    pip install -U qaviton

to exit your virtual environment:

.. code-block:: text

    (venv) path/to/tests>deactivate


Simple Examples
---------------

.. code-block:: python

    python -m qaviton create web tests

.. code-block:: python

    python -m qaviton create web,mobile tests

.. code-block:: python

    python -m qaviton create web tests --example
    python -m pytest tests

.. code-block:: text

    $ python -m qaviton create tests
     * creating qaviton tests
     * your testing framework is done!
     * start testing like a boss ⚛
     *      ______________
     *    /   __________   \           ______
     *   /  /            \  \         / ____ \
     *  /  /   \      /   \  \       / /    \ \    __        __   _   ___________    _______    _     _
     *  | |   O \    / O   | |      / |______| \   \ \      / /  |_| |____   ____|  / _____ \  | \   | |
     *  | |                | |     |  ________  |   \ \    / /   |-|      | |      | |     | | |  \  | |
     *  \  \  \________/  /   \    | |        | |    \ \  / /    | |      | |      | |     | | | | \ | |
     *   \  \____________/  /\ \_  | |        | |     \ \/ /     | |      | |      | |_____| | | |\ \| |
     *    \________________/  \__| |_|        |_|      \__/      |_|      |_|       \_______/  |_| \___|


run tests with local hub
------------------------

install docker:
https://docs.docker.com/install/

install selenoid:
go to option 2 to install with docker

https://github.com/aerokube/selenoid/blob/master/docs/quick-start-guide.adoc

go to your secret file and change your hub url to local host:

/project/tests/data/secret.py

hub='http://localhost:4444/wd/hub'


Community
------------

Please checkout our public test repository at: https://github.com/qaviton/test_repository

The Qaviton team wants to contribute and share testing experience.
You can use our tests and utilities in your project 
and even share your own tests code, functions and experience.

Be part of something big.


Contributing
------------

For guidance on setting up a development environment and how to make a
contribution to Qaviton, see the `contributing guidelines`_.

.. _contributing guidelines: https://github.com/qaviton/qaviton/blob/master/CONTRIBUTING.rst


Donate
------

The Qaviton organization develops and supports qaviton and the libraries
it uses. In order to grow the community of contributors and users, and
allow the maintainers to devote more time to the projects, `please
donate today`_.

.. _please donate today: https://www.qaviton.com/donate


Links
-----

* Website: https://www.qaviton.com
* Documentation: https://github.com/qaviton/qaviton/blob/master/docs/
* License: `Apache License 2.0 <https://github.com/qaviton/qaviton/blob/master/LICENSE>`_
* Releases: https://pypi.org/project/qaviton/
* Code: https://github.com/qaviton/qaviton
* Issue tracker: https://github.com/qaviton/qaviton/issues
* Test status:

  * Linux, Mac: https://travis-ci.org/qaviton/qaviton
  * Windows: https://ci.appveyor.com/project/qaviton/qaviton

* Test coverage: https://codecov.io/gh/qaviton/qaviton


.. _pip: https://pip.pypa.io/en/stable/quickstart/
