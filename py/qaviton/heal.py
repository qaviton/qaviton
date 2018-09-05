from qaviton.utils import filer
from qaviton.utils.operating_system import s
import inspect
# import gc


# references_to_ignore = ('__module__', '__dict__', '__weakref__', '__doc__')


heal_directory = '/tmp'
signal_to_stop = 'signal_to_stop_1111_2222_3333_4444_5555_6666'


class Heal:
    heal_by = []
    locator = None
    workspace = None
    heal_directory = None
    locator_src_file = None
    locator_file = None

    @classmethod
    def config(cls, workspace, locator, heal_by=None, heal_directory=heal_directory, signal_to_stop=signal_to_stop):
        cls.heal_directory = heal_directory+s+'heal'
        cls.locator = locator
        cls.locator_src_file = inspect.getfile(locator)
        cls.workspace = workspace
        if heal_by is not None:
            cls.heal_by = heal_by
        filer.create_directory(cls.heal_directory)
        cls.signal_session_to_start()

    @classmethod
    def signal_session_to_start(cls):
        cls.locator_file = cls.locator_src_file.split(s)[-1]
        if not filer.os.path.exists(cls.locator_file):
            filer.copy_file(cls.locator_src_file, cls.heal_directory + s + cls.locator_src_file.split(s)[-1])
            try:
                pass
            except: pass

    @classmethod
    def signal_session_to_stop(cls):
        filer.create_file(cls.heal_directory+s+'Heal_signal_session_to_stop')
        # filer.delete_directory(cls.heal_directory)

    @classmethod
    def heal_request(cls, locators_to_heal, locator):
        pass
        # module = locator[:-3].split('/')
        # module = module[-2] + '.' + module[-1]
        # references = gc.get_referrers()
        # request_is_done = False
        # for reference in references:
        #     if '__module__' in reference:
        #         if reference['__module__'].endswith(module) or reference['__module__'] == module:
        #             for k in reference:
        #                 if k not in references_to_ignore:
        #                     if not filer.os.path.exists(cls.heal_directory+s+k):
        #                         # TODO: should write the hole locator
        #                         try:
        #                             with open(cls.heal_directory+s+k, 'w+') as f:
        #                                 f.write(locators_to_heal)
        #                         except Exception as e:
        #                             if not filer.os.path.exists(cls.heal_directory+s+k):
        #                                 raise e
        #                     else:
        #                         # TODO: try to append?
        #                         pass
        #                     request_is_done = True
        #                     break
        #     if request_is_done:
        #         break

# TODO: change locators from file logic to object logic!!!