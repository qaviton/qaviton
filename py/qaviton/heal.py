from qaviton.utils import filer
from qaviton.utils.operating_system import s
import gc


references_to_ignore = ('__module__', '__dict__', '__weakref__', '__doc__')


class Heal:
    heal_by = []
    locators = None
    workspace = None
    heal_directory = None

    @classmethod
    def config(cls, workspace, locators, heal_by=None, heal_directory='/tmp'):
        cls.heal_directory = heal_directory+s+'heal'
        cls.locators = locators
        cls.workspace = workspace
        if heal_by is not None:
            cls.heal_by = heal_by
        cls.signal_session_to_start(locators)

    @classmethod
    def signal_session_to_start(cls, locators):
        filer.create_directory(cls.heal_directory)
        filer.copy_file(locators, cls.heal_directory+s+locators.split(s)[-1])

    @classmethod
    def signal_session_to_stop(cls):
        filer.delete_directory(cls.heal_directory)

    @classmethod
    def heal_request(cls, locators_to_heal, locator):
        module = locator[:-3].split('/')
        module = module[-2] + '.' + module[-1]
        references = gc.get_referrers()
        request_is_done = False
        for reference in references:
            if '__module__' in reference:
                if reference['__module__'].endswith(module) or reference['__module__'] == module:
                    for k in reference:
                        if k not in references_to_ignore:
                            if not filer.os.path.exists(cls.heal_directory+s+k):
                                # TODO: should write the hole locator
                                try:
                                    with open(cls.heal_directory+s+k, 'w+') as f:
                                        f.write(locators_to_heal)
                                except Exception as e:
                                    if not filer.os.path.exists(cls.heal_directory+s+k):
                                        raise e
                            else:
                                # TODO: try to append?
                                pass
                            request_is_done = True
                            break
            if request_is_done:
                break

# TODO: change locators from file logic to object logic!!!