from qaviton.common import WebPlatforms
from qaviton import crosstest
from qaviton.utils import path
from tests.data.count_functions import from_zero_to_hero


app = [
    # web
    'file://' + path.of(__file__)('../../apps/ContactManager/ContactManager.html'),
    # mobile
    path.of(__file__)('../../apps/ContactManager/ContactManager.apk')
]

platforms = crosstest.Platforms()
platforms.web(WebPlatforms.chrome(app[0]))
platforms.web(WebPlatforms.firefox(app[0], size="800x1200"))
platforms.web(WebPlatforms.internetExplorer(app[0], size="min"))
platforms.mobile(dict(
    platformName="Android",
    platformVersion="6.0",
    deviceName="emulator-5554",
    app=app[1],
    appPackage='com.example.android.contactmanager',
    appActivity='.ContactManager'))

TESTS = crosstest.Models(platforms, data=[from_zero_to_hero]).get()
