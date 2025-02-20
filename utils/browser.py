from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVE_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVE_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(options=chrome_options, service=chrome_service)

    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://udemy.com/')
    browser.quit()
