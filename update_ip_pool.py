import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def scrape_ip_proxies(url):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--headless')
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    info_browser_list = browser.find_elements(by=By.CSS_SELECTOR, value='.layui-table > tbody > tr')
    info_list = []
    for info in info_browser_list:
        infoes = info.text.split(' ')[:4]
        if infoes[2] == '高匿' and infoes[3] == 'HTTP':
            print(infoes)
            info_list.append(infoes[0] + ':' + infoes[1])
    with open('ip_proxies_pool.json', 'w', encoding='utf-8') as f:
        json.dump(info_list, f, indent=4)
    browser.close()

def main():
    URL = 'https://ip.jiangxianli.com/country/{country}?country={country}'
    scrape_ip_proxies(url=URL.format(country='中国'))

if __name__ == '__main__':
    main()