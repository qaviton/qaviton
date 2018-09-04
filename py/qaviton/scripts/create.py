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

        # to install your requirements on a new machine:
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


def install(tests_dir):
    os.system('cd ' + tests_dir + ' & pip install virtualenv & virtualenv env')
    os.system('cd ' + tests_dir + ' & pip install -r requirements.txt')
    install_is_done(tests_dir)


@initial_msg
def web(tests_dir='tests'):
    filer.copy_directory(examples+s+'simple_web', cwd+s+tests_dir)
    if tests_dir != 'tests':
        filer.find_replace(cwd+s+tests_dir, 'from tests.', 'from '+tests_dir+'.', "*.py")
    install(tests_dir)
