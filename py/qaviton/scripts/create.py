import os
from qaviton.utils import filer
from qaviton.utils import path
from qaviton.utils.operating_system import s
from qaviton.version import __version__


cwd = os.getcwd()
examples = path.of(__file__)('examples')


def initial_msg(f):
    def dec(*args, **kwargs):
        print("""
            QAVITON VERSION {}
            creating qaviton framework and test examples
            
            """.format(__version__))
        f(*args, **kwargs)
    return dec


def install_is_done(tests_dir):
    print("""


            @@@@@@@@@@@@@@@@@@@@@
            @ installation done @
            @@@@@@@@@@@@@@@@@@@@@

        ------------------------------------------
        activate your testing virtual environment:
        ------------------------------------------
        """)
    print("linux\mac: path/to/project> cd {} & source env/bin/activate".format(tests_dir))
    print("~~windows: path/to/project> cd {} & env\\Scripts\\activate".format(tests_dir))
    print("""

        # to exit your virtual environment:
        (env) path/to/tests>deactivate

        # use pip install, uninstall & freeze 
        # to manage your dependencies:
        (env) path/to/tests> pip freeze > requirements.txt

        # to install your requirements on a new machine(consider using git):
        (env) path/to/tests> pip install -r requirements.txt

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

        """)


def add_readme(tests_dir):
    with open(cwd+s+tests_dir+s+'README.rst', 'w+') as f:
        f.write("this should be changed to a custom README file for your project\n"
                "you have a nice starting point from here.\n"
                "\n"
                "requirements\n"
                "------------\n"
                "python 3.7 and above\n"
                "pytest latest\n"
                "\n"
                "\n"
                "testing examples\n"
                "----------------\n"
                "checkout under execute_tests/end_to_end_tests to see testing examples.\n"
                "\n"
                "\n"
                "model-based examples\n"
                "--------------------\n"
                "check out the pages directory for page model examples\n"
                "and services/app for a model-based-app service for testing.\n"
                "\n"
                "\n"
                "conftest & pytest.ini\n"
                "---------------------\n"
                "look at the conftest.py to see how to add model-based fixtures\n"
                "you can set parallel testing & reporting with pytest.ini file\n"
                "\n"
                "\n"
                "setup your hub\n"
                "--------------\n"
                "check out in the data dir to set your secret user key and remote hub\n"
                "and customize your supported platforms under the data/supported_platfoms.py file.\n"
                "\n"
                "\n"
                "local hub\n"
                "---------\n"
                "install docker:\n"
                "https://docs.docker.com/install/\n"
                "\n"
                "install selenoid:\n"
                "go to option 2 to install with docker\n"
                "https://github.com/aerokube/selenoid/blob/master/docs/quick-start-guide.adoc\n"
                "\n"
                "go to your secret file and change your hub url to local host:\n"
                "/project/tests/data/secret.py\n"
                "hub='http://localhost:4444/wd/hub'\n"
                "\n"
                "\n"
                "run tests examples\n"
                "------------------\n"
                "cd to your project(in my case it's called myapp and my tests are under tests) and simply\n"
                "(env) C:\\Users\\user\\PycharmProjects\\myapp>python -m pytest tests\n"
                "\n"
                "or run with pycharm:\n"
                "https://www.jetbrains.com/pycharm/download/#section=windows\n"
                "https://www.jetbrains.com/help/pycharm/pytest.html")


def add_gitignore(tests_dir):
    if not filer.os.path.exists(cwd + s + '.gitignore'):
        with open(cwd + s + tests_dir + s + '.gitignore', 'w+') as f:
            f.write("# Byte-compiled / optimized / DLL files\n"
                    "__pycache__/\n"
                    "*.py[cod]\n"
                    "*$py.class\n"
                    "\n"
                    "# C extensions\n"
                    "*.so\n"
                    "\n"
                    "# Distribution / packaging\n"
                    ".Python\n"
                    "build/\n"
                    "develop-eggs/\n"
                    "dist/\n"
                    "downloads/\n"
                    "eggs/\n"
                    ".eggs/\n"
                    "lib/\n"
                    "lib64/\n"
                    "parts/\n"
                    "sdist/\n"
                    "var/\n"
                    "wheels/\n"
                    "*.egg-info/\n"
                    ".installed.cfg\n"
                    "*.egg\n"
                    "MANIFEST\n"
                    "\n"
                    "# PyInstaller\n"
                    "#  Usually these files are written by a python script from a template\n"
                    "#  before PyInstaller builds the exe, so as to inject date/other infos into it.\n"
                    "*.manifest\n"
                    "*.spec\n"
                    "\n"
                    "# Installer logs\n"
                    "pip-log.txt\n"
                    "pip-delete-this-directory.txt\n"
                    "\n"
                    "# Unit test / coverage reports\n"
                    "htmlcov/\n"
                    ".tox/\n"
                    ".coverage\n"
                    ".coverage.*\n"
                    ".cache\n"
                    "nosetests.xml\n"
                    "coverage.xml\n"
                    "*.cover\n"
                    ".hypothesis/\n"
                    ".pytest_cache/\n"
                    "\n"
                    "# Translations\n"
                    "*.mo\n"
                    "*.pot\n"
                    "\n"
                    "# Django stuff:\n"
                    "*.log\n"
                    "local_settings.py\n"
                    "db.sqlite3\n"
                    "\n"
                    "# Flask stuff:\n"
                    "instance/\n"
                    ".webassets-cache\n"
                    "\n"
                    "# Scrapy stuff:\n"
                    ".scrapy\n"
                    "\n"
                    "# Sphinx documentation\n"
                    "docs/_build/\n"
                    "\n"
                    "# PyBuilder\n"
                    "target/\n"
                    "\n"
                    "# Jupyter Notebook\n"
                    ".ipynb_checkpoints\n"
                    "\n"
                    "# pyenv\n"
                    ".python-version\n"
                    "\n"
                    "# celery beat schedule file\n"
                    "celerybeat-schedule\n"
                    "\n"
                    "# SageMath parsed files\n"
                    "*.sage.py\n"
                    "\n"
                    "# Environments\n"
                    ".env\n"
                    ".venv\n"
                    "env/\n"
                    "venv/\n"
                    "ENV/\n"
                    "env.bak/\n"
                    "venv.bak/\n"
                    "\n"
                    "# Spyder project settings\n"
                    ".spyderproject\n"
                    ".spyproject\n"
                    "\n"
                    "# Rope project settings\n"
                    ".ropeproject\n"
                    "\n"
                    "# mkdocs documentation\n"
                    "/site\n"
                    "\n"
                    "# mypy\n"
                    ".mypy_cache/\n"
                    "\n"
                    "# private\n"
                    "*secret*")


def add_pytest_ini(tests_dir):
    with open(cwd+s+tests_dir+s+'pytest.ini', 'w+') as f:
        f.write("[pytest]\n"
                ";addopts = -n 3\n"
                ";addopts = --html=report.html\n"
                ";addopts = --junitxml=\path\\to\\reports\n"
                ";addopts = --collect-only\n"
                ";addopts = --cov=your_app")
    

def add_create_env(tests_dir):
    if not filer.os.path.exists(cwd+s+'create_env.sh'):
        with open(cwd+s+tests_dir+s+'create_env.sh', 'w+') as f:
            f.write("#!/bin/bash\n"
                    "\n"
                    "\n"
                    "## Requirements\n"
                    "## gcc, make, Python 3.7+, python-pip, virtualenv\n"
                    "\n"
                    "## Instalation\n"
                    "## Create a virtualenv, and activate this:\n"
                    "python -m pip install --upgrade pip\n"
                    "pip install virtualenv\n"
                    "\n"
                    "virtualenv env\n"
                    "\n"
                    "source env/bin/activate || env\Scripts\\activate\n"
                    "\n"
                    "# use:\n"
                    "# pip freeze > requirements.txt\n"
                    "# to update your requirements\n"
                    "pip install -r requirements.txt\n"
                    "\n"
                    "\n")
        return True
        

def add_requirements(tests_dir):
    if not filer.os.path.exists(cwd + s + 'requirements.txt'):
        with open(cwd+s+tests_dir+s+'requirements.txt', 'w+') as f:
            f.write("apipkg==1.5\n"
                    "Appium-Python-Client==0.28\n"
                    "atomicwrites==1.1.5\n"
                    "attrs==18.1.0\n"
                    "certifi==2018.8.24\n"
                    "chardet==3.0.4\n"
                    "colorama==0.3.9\n"
                    "coverage==4.5.1\n"
                    "execnet==1.5.0\n"
                    "Faker==0.8.17\n"
                    "gitdb2==2.0.4\n"
                    "idna==2.7\n"
                    "imageio==2.3.0\n"
                    "jsondiff==1.1.2\n"
                    "keyboard==0.13.2\n"
                    "more-itertools==4.3.0\n"
                    "mouse==0.7.0\n"
                    "numpy==1.15.0\n"
                    "Pillow==5.2.0\n"
                    "pkginfo==1.4.2\n"
                    "pluggy==0.7.1\n"
                    "psutil==5.4.6\n"
                    "py==1.5.4\n"
                    "pytest==3.7.1\n"
                    "pytest-cov==2.5.1\n"
                    "pytest-forked==0.2\n"
                    "pytest-lazy-fixture==0.4.1\n"
                    "pytest-metadata==1.7.0\n"
                    "pytest-ordering==0.5\n"
                    "pytest-rerunfailures==4.1\n"
                    "pytest-xdist==1.22.5\n"
                    "python-dateutil==2.7.3\n"
                    "PyYAML==3.13\n"
                    "requests==2.19.1\n"
                    "requests-toolbelt==0.8.0\n"
                    "selenium==3.14.0\n"
                    "six==1.11.0\n"
                    "smmap2==2.0.4\n"
                    "text-unidecode==1.2\n"
                    "threaders==0.2.12\n"
                    "tqdm==4.25.0\n"
                    "twine==1.11.0\n"
                    "urllib3==1.23\n"
                    "virtualenv==16.0.0\n")
        return True
        
        
def install(tests_dir, create_env, create_requirements):
    if create_env:
        os.system('cd ' + tests_dir + ' & pip install virtualenv & virtualenv env')
        if create_requirements:
            os.system('cd ' + tests_dir + ' & pip install -r requirements.txt')
        else:
            os.system('pip install -r requirements.txt')
    install_is_done(tests_dir)


@initial_msg
def web(tests_dir='tests'):
    filer.copy_directory(examples+s+'simple_web', cwd+s+tests_dir)
    if tests_dir != 'tests':
        filer.find_replace(cwd+s+tests_dir, 'from tests.', 'from '+tests_dir+'.', "*.py")
    add_readme(tests_dir)
    add_pytest_ini(tests_dir)
    add_gitignore(tests_dir)
    create_env = add_create_env(tests_dir)
    create_requirements = add_requirements(tests_dir)
    install(tests_dir, create_env, create_requirements)
