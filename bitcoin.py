import os
import argparse
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Process

def get_selenium(url: str) -> WebDriver:
    """
    url을 입력받아 WebDriver 객체를 반환합니다.
    selenium 라이브러리를 사용해 JS 기반의 동적이 웹페이지 크롤링이 가능합니다.
    WebDriver.click() 함수 호출 이후, time.sleep(1) 실행이 권장됩니다.

    :param url: 크롤링할 페이지의 url입니다."""
    driver_loc = os.popen("which chromedriver").read().strip()
    if len(driver_loc) == 0:
        raise Exception("ChromeDriver를 다운로드한 후 다시 시도해주세요.")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    webdriver_service = Service(driver_loc)
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get(url)

    return browser

def process_task(url, print_flag):
    if print_flag:
        print(url)
    else:
        browser = get_selenium(url)
        title = browser.find_element(By.TAG_NAME, 'title').get_attribute('textContent')
        print(title.split('|')[0])
        browser.quit()

def main():
    parser = argparse.ArgumentParser(description='Bitcoin price checker.')
    parser.add_argument('-u', '--url', action='store_true', help='print the URL')
    parser.add_argument('-e', '--examples', action='store_true', help='Print example coin ticker (SHIB, DOGE)')
    parser.add_argument('-w', '--watchlist', type=str, default='BTC', help='comma separated list of symbols to watch (Default = BTC)')
    args = parser.parse_args()

    if args.examples:
        print("Example coin ticker: SHIB, DOGE")
        return
    coins = args.watchlist.split(',')
    if coins == ['a']:
        coins=["BTC", "SHIB", "DOGE"]
    processes = []
    for ticker in coins:
        url = f"https://upbit.com/exchange/CRIX.UPBIT.KRW-{ticker}"
        p = Process(target=process_task, args=(url, args.url))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

main()

