import os
import platform


class System:
    name = os.nameplatform_system = platform.system()
    platform_release = platform.release()
    slash = '/'
    if name in ('Windows', 'nt'):
        slash = '\\'


s = System.slash
