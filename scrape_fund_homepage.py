import requests
from pyquery import PyQuery as pq
import logging
import re

base_url = 'http://fund.eastmoney.com'

proxies = {
    'http': '116.117.134.135:80'
}
# son_headers 基金显示页的请求头
son_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'fund.eastmoney.com',
    'Referer': 'http://fund.eastmoney.com/fundguzhi.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

def scrape_fund_info(url):
    '''
    获取单个基金的以下信息：
    基金代码 / 基金名称 / 收益率【近一月 / 近三月 / 近六月 / 近一年 / 近三年 / 成立来】 / 基金规模 / 基金经理 / 基金管理公司 / 基金成立日 / 股票前十大持仓
    '''
    fund_res = requests.get(url=url, headers=son_headers, proxies=proxies)
    if fund_res.status_code != 200:
        print('Appear {} error ! exit code !'.format(str(fund_res.status_code)))
        exit()
    html = pq(fund_res.content)
    name, code = html('div.fundDetail-tit div:first-child').text().split('(')
    if len(code) != 6:
        logging.error('Fund code information error!')
        exit()
    one_month = html('dl.dataItem01 dd:nth-child(3) span:nth-child(2)').text().replace('%', '')
    three_month = html('dl.dataItem02 dd:nth-child(3) span:nth-child(2)').text().replace('%', '')
    six_month = html('dl.dataItem03 dd:nth-child(3) span:nth-child(2)').text().replace('%', '')
    one_year = html('dl.dataItem01 dd:nth-child(4) span:nth-child(2)').text().replace('%', '')
    three_year = html('dl.dataItem02 dd:nth-child(4) span:nth-child(2)').text().replace('%', '')
    since_setup = html('dl.dataItem03 dd:nth-child(4) span:nth-child(2)').text().replace('%', '')
    
    def just_rate(rate):
        if bool(re.search(r'\d', rate)):
            return float(rate)/100
        else:
            return rate
    income_rate = {
        'one_month': just_rate(one_month),
        'three_month': just_rate(three_month),
        'six_month': just_rate(six_month),
        'one_year': just_rate(one_year),
        'three_year': just_rate(three_year),
        'since_setup': just_rate(since_setup)
    }
    fund_size = html('div.infoOfFund tr:first-child td:nth-child(2)').text()
    fund_mananger = html('div.infoOfFund tr:first-child td:nth-child(3)').text()
    fund_company = html('div.infoOfFund tr:last-child td:nth-child(2)').text()
    fund_setup_day = html('div.infoOfFund tr:last-child td:first-child').text()

    info = re.search('：(.*?)（', fund_size).group(1)
    if re.search('[\u4e00-\u9fa5]+', info).group() == '亿元':
        fund_size = float(re.search('[^\u4e00-\u9fa5]+', info).group()) * 100000000
    elif re.search('[\u4e00-\u9fa5]+', info).group() == '千万元':
        fund_size = float(re.search('[^\u4e00-\u9fa5]+', info).group()) * 10000000
    elif re.search('[\u4e00-\u9fa5]+', info).group() == '百万元':
        fund_size = float(re.search('[^\u4e00-\u9fa5]+', info).group()) * 1000000
    elif re.search('[\u4e00-\u9fa5]+', info).group() == '万元':
        fund_size = float(re.search('[^\u4e00-\u9fa5]+', info).group()) * 10000
    else:
        print(fund_size)
        print('match error !')
        exit()
    
    fund_mananger = re.search('：(.*)', fund_mananger).group(1)  # 基金经理
    fund_company = re.search('：(.*)', fund_company).group(1)  # 基金管理公司
    fund_setup_day = re.search('：(.*)', fund_setup_day).group(1)  # 基金成立日
    # 股票前十大持仓
    position_shares = {}
    alignLeft = list(html('#position_shares div table tr td.alignLeft a').items())
    if len(alignLeft) >= 2:
        keys = []; values = []
        for L in alignLeft:
            keys.append(L.attr.title)
        alignRight = list(html('#position_shares div table tr td.alignRight').items())
        for i in range(0, len(alignRight), 2):
            values.append(round(float(alignRight[i].text().replace('%', ''))/100, 4))
        for i in range(len(keys)):
            position_shares[keys[i]] = values[i] 
    
    fund_data = {
        'code': code,
        'name': name,
        'income_rate': income_rate,
        'fund_size': fund_size,
        'fund_mananger': fund_mananger,
        'fund_company': fund_company,
        'fund_setup_day': fund_setup_day,
        'position_shares': position_shares
    }
    print(fund_data)

def read_urls():
    pass

def save_data():
    pass

def main():
    jijin_url = 'http://fund.eastmoney.com/005968.html'
    scrape_fund_info(jijin_url)
    for url in read_urls:
        scrape_fund_info(url)

if __name__ == '__main__':
    main()
