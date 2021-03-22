import requests
import json

def test_url(url, proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, proxies=proxy)
    if res.status_code == 200:
        print(f'{proxy} OK !')
        return proxy
    else:
        print(f'{proxy} appear {res.status_code} error !')
        return None

def read_pool():
    with open('ip_proxies_pool.json', 'r', encoding='utf-8') as f:
        ip_data = json.load(f)
    return ip_data

def main(url):
    dict_data = read_pool()
    qualify_proxies = []
    for ip in dict_data:
        proxy = {
            'http': ip
        }
        if test_url(url=url, proxy=proxy) is not None:
            qualify_proxies.append(ip)
    print(len(qualify_proxies))
    if len(qualify_proxies) == 0:
        print(f'代理池中无{url}可用代理！')
        exit()
    with open('proxies_temp.json', 'w', encoding='utf-8') as f:
        json.dump(qualify_proxies, f, indent=4)


if __name__ == '__main__':
    # 测试要爬取网站的URL
    TEST_URL = 'http://fund.eastmoney.com'
    main(TEST_URL)
