import requests
import json
from qaviton.drivers.xml_driver import XMLDriver
from qaviton.locator import Locator


def get_firefox_versions():
    r = requests.get("https://ftp.mozilla.org/pub/firefox/releases/")
    lines = r.text.split("/pub/firefox/releases/")
    del lines[0]
    versions = []
    for line in lines:
        version = line.split("/")[0]
        if version.endswith('.0') and len(version.split(".")) == 2:
            versions.append(line.split("/")[0])
    return versions


def get_chrome_versions():
    r = requests.get("https://en.wikipedia.org/wiki/Google_Chrome_version_history")
    driver = XMLDriver(r.text)
    versions = driver.get_text(Locator.xpath("//td[@style='white-space:nowrap; background:salmon;']"))
    return [version.replace("\n", "") for version in versions]


def get_ie_versions():
    r = requests.get("https://en.wikipedia.org/wiki/Internet_Explorer_version_history")
    driver = XMLDriver(r.text)
    versions = driver.get_text(Locator.xpath("//table[@class='wikitable'][2]//tr/th/a"))
    return [version.replace("Version ", "") for version in versions]


def get_opera_versions():
    r = requests.get("https://www.opera.com/docs/history/")
    lines = r.text\
        .split('id="historyTable">')[1]\
        .split("</tbody>")[0]\
        .split("<tbody>")[0].replace("</tr>", "").replace("\n", "")\
        .split("<tr>")
    del lines[0]
    return [line.split("Opera ")[1].split("<")[0] for line in lines if '<th colspan="2"' in line and "Opera " in line]


if __name__ == "__main__":
    versions = dict(
        chrome_versions=get_chrome_versions(),
        ie_versions=get_ie_versions(),
        firefox_versions=get_firefox_versions(),
        opera_versions=get_opera_versions()
    )
    with open('versions.json', 'w') as fp:
        json.dump(versions, fp, indent=4)
