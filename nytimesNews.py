# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
import re
import numpy as np
import pandas as pd
from datetime import datetime
from variables import *

def nytimes():
    url='https://www.nytimes.com/section/world'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers).text
    #html=html.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('h2',{'class':'headline'})
    newsTitle=[i.text for i in newsList[:10]]
    newsURL=[i.find('a').get('href') for i in newsList[:10]]
    print(newsTitle)
    print(newsURL)



    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).text
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('p',{'class':'css-1ebnwsw e2kc3sl0'})
        words=''.join(i.text for i in newsList)
        content.append(words)
    #print(content)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())

    data.to_sql('nytimes_news',engine,if_exists='replace')
    print('nytimes_news is done.')

if __name__ == '__main__':
    nytimes()