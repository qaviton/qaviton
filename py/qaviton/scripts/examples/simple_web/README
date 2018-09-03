this should be changed to a custom README file for your project
you have a nice starting point from here.

requirements
------------
python 3.7 and above
pytest latest


testing examples
----------------
checkout under execute_tests/end_to_end_tests to see testing examples.


model-based examples
--------------------
check out the pages directory for page model examples
and services/app for a model-based-app service for testing.


conftest & pytest.ini
---------------------
look at the conftest.py to see how to add model-based fixtures
you can set parallel testing & reporting with pytest.ini file


setup your hub
--------------
check out in the data dir to set your secret user key and remote hub
and customize your supported platforms under the data/supported_platfoms.py file.


local hub
---------
install docker:
https://docs.docker.com/install/

install selenoid:
go to option 2 to install with docker
https://github.com/aerokube/selenoid/blob/master/docs/quick-start-guide.adoc

go to your secret file and change your hub url to local host:
/project/tests/data/secret.py
hub='http://localhost:4444/wd/hub'


run tests examples
------------------
cd to your project(in my case it's called myapp and my tests are under tests) and simply
(env) C:\Users\user\PycharmProjects\myapp>python -m pytest tests

or run with pycharm:
https://www.jetbrains.com/pycharm/download/#section=windows
https://www.jetbrains.com/help/pycharm/pytest.html