# scrape_fund_data
Get some data from tiantian fund.  WEB URL: http://fund.eastmoney.com/fundguzhi.html

### 数据爬取目标如下：
collection information:
scrape_url.py

| 基金代码 | 基金名称 | 基金url  |  评论url   |
| :------: | :------: | :------: | :--------: |
|   code   |   name   | fund_url | review_url |

scrape_fund_baseInfo.py

|   指标名称   |    指标命名     |
| :----------: | :-------------: |
|   基金代码   |      code       |
|   基金名称   |      name       |
|    收益率    |   income_rate   |
|   基金规模   |    fund_size    |
|   基金经理   |  fund_mananger  |
| 基金管理公司 |  fund_company   |
|  基金成立日  | fund_setup_day  |
|  前十大持仓  | position_shares |

| 收益率指标 |  指标命名   |
| :--------: | :---------: |
|   近一月   |  one_month  |
|   近三月   | three_month |
|   近六月   |  six_month  |
|   近一年   |  one_year   |
|   近三年   | three_year  |
|   成立来   | since_setup |
