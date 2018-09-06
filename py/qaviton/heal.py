import requests


class Heal:
    @classmethod
    def config(cls, workspace, locator, heal_by=None, heal_directory='/tmp/heal', signal_to_stop='stop'):
        requests.post(
            'https://www.qavitonsaasservice.com/heal-conf',
            json=dict(
                workspace=workspace,
                locator=locator,
                heal_by=heal_by,
                heal_directory=heal_directory,
                signal_to_stop=signal_to_stop))

    @classmethod
    def signal_session_to_start(cls):
        requests.get('https://www.qavitonsaasservice.com/heal-start')

    @classmethod
    def signal_session_to_stop(cls):
        requests.get('https://www.qavitonsaasservice.com/heal-done')

    @classmethod
    def heal_request(cls, locator, healed_locator):
        requests.post(
            'https://www.qavitonsaasservice.com/heal-loc',
            json=dict(locator=locator, healed_locator=healed_locator))
