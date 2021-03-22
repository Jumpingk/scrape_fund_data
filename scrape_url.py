import requests
from requests import urllib3
from pyquery import PyQuery as pq
import time
from urllib import parse
import re
import json
import random
import pymongo
from tqdm import tqdm
urllib3.disable_warnings()

base_url = 'http://fund.eastmoney.com'
api_base_url = 'http://api.fund.eastmoney.com'
guba_base_url = 'http://guba.eastmoney.com'

def get_proxies():
    with open('proxies_temp.json', 'r', encoding='utf-8') as f:
        ip_data = json.load(f)
    proxies = []
    for ip in ip_data:
        proxies.append({'http': ip})
    return proxies

# parent_headers 基金列表页的请求头
parent_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'api.fund.eastmoney.com',
    'Pragma': 'no-cache',
    'Referer': 'http://fund.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

def axis_info(category):
    data = {
        '全部': {'type': 1},
        '股票型': {'type': 2},
        '混合型': {'type': 3},
        '债券型': {'type': 4},
        '指数型': {'type': 5},
        'QDII': {'type': 6},
        'ETF联接': {'type': 7},
        'LOF': {'type': 8},
        '场内交易基金': {'type': 9}
    }
    return data[category]

def params_info(type_info, pageIndex, callback):
    params = {
        "type": type_info,
        "sort": 3,
        "orderType": 'desc',
        "canbuy": 0,
        "pageIndex": pageIndex,
        "pageSize": 200,
        "callback": callback,
        "_": int(time.time() * 1000)
    }
    return params

def scrape_data(params_infoes, proxies):
    fund_list_res = requests.get(url=parse.urljoin(api_base_url, 'FundGuZhi/GetFundGZList'), headers=parent_headers, proxies=proxies, params=params_infoes, timeout=20)
    if fund_list_res.status_code == 200:
        text_data = re.search('\{(.*)\}', fund_list_res.text, re.S)
        json_data = json.loads(text_data.group())
        jijin_list = []
        for jijin_data in json_data.get('Data').get('list'):
            data = {
                'code': jijin_data.get('bzdm'),
                'name': jijin_data.get('jjjc'),
                'fund_url': parse.urljoin(base_url, jijin_data.get('bzdm') + '.html'),
                'review_url': parse.urljoin(guba_base_url, 'list,of' + jijin_data.get('bzdm') + '.html')
            }
            jijin_list.append(data)
        return jijin_list
    else:
        print('Appear {} error ! exit code !'.format(str(fund_list_res.status_code)))
        exit()

def main(total_pages, data_category):
    jQuery_version = '1.8.3'
    CALL_BACK = 'jQuery' + (jQuery_version + str(random.random())).replace('.', '')  + '_' + str(int(time.time() * 1000))
    print('等待5秒钟......')
    time.sleep(5)
    proxies = get_proxies()
    for page in tqdm(range(1, total_pages + 1), desc='Processing '):
        params = params_info(type_info=axis_info(data_category).get('type'), pageIndex=page, callback=CALL_BACK)
        jijins = tqdm(scrape_data(params, random.choice(proxies)), desc='Data deal ')
        for jijin in jijins:
            collection.insert(jijin)


if __name__ == '__main__':

    CATEGORYS_AND_PAGES_INFO = {
        '股票型': 8, 
        '混合型': 25, 
        '债券型': 14, 
        '指数型': 7, 
        'QDII': 2, 
        'ETF联接': 2, 
        'LOF': 2, 
        '场内交易基金': 3
    }
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['tiantianjijin_data']

    for key, value in CATEGORYS_AND_PAGES_INFO.items():
        # 参数设定
        TOTAL_PAGES = value
        DATA_CATEGORY = key
        
        # 数据存储
        data_collection = DATA_CATEGORY + '基金简单信息'
        collection = db[data_collection]

        # 数据爬取
        print('开始爬取{}......'.format(data_collection))
        main(total_pages=TOTAL_PAGES, data_category=DATA_CATEGORY)

