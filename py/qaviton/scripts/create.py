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

        # use pip install, uninstall & freeze 
        # to manage your dependencies:
        (venv) path/to/project> pip freeze > requirements-test.txt

        # to install your requirements on a new machine(consider using git):
        (venv) path/to/project> pip install -r requirements-test.txt

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
    with open(cwd + s + tests_dir + s + 'README.rst', 'w+') as f:
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
    with open(cwd + s + tests_dir + s + 'pytest.ini', 'w+') as f:
        f.write("[pytest]\n"
                ";addopts = -n 3\n"
                ";addopts = --html=report.html\n"
                ";addopts = --junitxml=\path\\to\\reports\n"
                ";addopts = --collect-only\n"
                ";addopts = --cov=your_app")


def add_requirements(tests_dir):
    if not filer.os.path.exists(cwd + s + 'requirements-test.txt'):
        open(cwd + s + 'requirements-test.txt', 'w+').close()
        os.system('pip freeze > requirements-test.txt')


# TODO: add more content for different frameworks
@initial_msg
def framework(frameworks, tests_dir, params):
    if '--example' in params:
        filer.copy_directory(examples + s + 'simple_web', cwd + s + tests_dir)
        add_readme(tests_dir)

    else:
        filer.copy_directory(examples + s + 'new_project', cwd + s + tests_dir)

    if tests_dir != 'tests':
        filer.find_replace(cwd + s + tests_dir, 'from tests.', 'from ' + tests_dir + '.', "*.py")

    add_pytest_ini(tests_dir)
    add_gitignore(tests_dir)
    add_requirements(tests_dir)
    install_is_done(tests_dir)
