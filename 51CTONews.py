# -*- coding: GB2312 -*-
"""
Created on Fri Dec 21 21:38:41 2018

@author: xiaofeng.li
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from variables import *
from datetime import datetime
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'

def ctoNews():
    url='http://ai.51cto.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers)
    html=html.content.decode('GBK')
    print(html)
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('div',{'class':'rinfo'})
    print(newsList)
    newsTitle=[i.text for i in newsList]
    newsURL=[i.find('a').get('href') for i in newsList]
    print(newsTitle)
    print(newsURL)

    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).content.decode('GB18030').encode('utf8')
        html=str(html,'utf-8')
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find('div',{'class':'zwnr'})
        newsList=newsList.find_all('p')[:-3]
        words=''.join(i.text for i in newsList)
        content.append(words)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('cto_chi',engine,if_exists='replace')
    print('51CTO is done.')

if __name__ == '__main__':
    ctoNews()