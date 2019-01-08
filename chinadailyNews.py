import pandas as pd
import requests
from bs4 import BeautifulSoup
from variables import *
from datetime import datetime
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'

def chinadailyNews():
    url='http://cn.chinadaily.com.cn/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers).text
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('h3')
    newsTitle=[i.text for i in newsList]
    newsURL=['https:'+i.find('a').get('href') for i in newsList]
    print(newsTitle,newsURL)

    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).text
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('div',{'id':'Content'})
        words=''.join(i.get_text() for i in newsList)
        content.append(words)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('china_daily',engine,if_exists='replace')
    print('china_daily is done.')

if __name__ == '__main__':
    chinadailyNews()