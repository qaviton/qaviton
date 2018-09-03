import os
from qaviton.utils import filer
from qaviton.utils import path
from qaviton.utils.operating_system import s
from qaviton.version import __version__


cwd = os.getcwd()
examples = path.of(__file__)('examples')


def pretty(f):
    def dec(*args, **kwargs):
        print("""
            QAVITON VERSION {}
            creating qaviton framework and test examples
            
            """.format(__version__))
        f(*args, **kwargs)
        print("""

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
    return dec


def install(tests_dir):
    os.system('cd ' + tests_dir + ' & pip install virtualenv & virtualenv env')
    os.system('cd ' + tests_dir + ' & source env/bin/activate')
    os.system('cd ' + tests_dir + ' & env\Scripts\\activate')
    os.system('cd ' + tests_dir + ' & pip install -r requirements.txt')


@pretty
def web(tests_dir='tests'):
    filer.copy_directory(examples+s+'simple_web', cwd+s+tests_dir)
    if tests_dir != 'tests':
        filer.find_replace(cwd+s+tests_dir, 'from tests.', 'from '+tests_dir+'.', "*.py")
    install(tests_dir)
