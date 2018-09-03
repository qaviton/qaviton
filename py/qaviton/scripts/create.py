import os
from qaviton.utils import filer
from qaviton.utils import path
from qaviton.utils.operating_system import s


cwd = os.getcwd()
examples = path.of(__file__)('examples')


def web(tests_dir='tests'):
    filer.copy_directory(examples+s+'simple_web', cwd+s+tests_dir)
    if tests_dir != 'tests':
        filer.find_replace(cwd+s+tests_dir, 'from tests.', 'from '+tests_dir+'.', "*.py")
    os.system('cd '+tests_dir+' & pip install virtualenv & virtualenv env')
    os.system('cd '+tests_dir+' & source env/bin/activate')
    os.system('cd '+tests_dir+' & env\Scripts\\activate')
    os.system('cd '+tests_dir+' & pip install -r requirements.txt')
