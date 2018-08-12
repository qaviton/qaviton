import os
import platform


class System:
    name = os.nameplatform_system = platform.system()
    platform_release = platform.release()
    slash = '/'
    if name == 'nt' or name == 'Windows':
        slash = '\\'


s = System.slash
