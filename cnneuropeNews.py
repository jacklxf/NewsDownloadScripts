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

def cnneurope():
    url='https://edition.cnn.com/europe'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers).text
    #html=html.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('h3',{'class':'cd__headline'})
    newsTitle=[i.text for i in newsList][:14]
    newsURL=['https://edition.cnn.com'+i.find('a').get('href') for i in newsList][:14]
    print(newsTitle)
    print(newsURL)

    content=[]
    for i in newsURL[:14]:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).text
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('div',{'class':'zn-body__paragraph'})
        words = ''.join(i.text for i in newsList)
        content.append(words)
    #print(content)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('cnn_europe',engine,if_exists='replace')
    print('cnn_europe is done.')

if __name__ == '__main__':
    cnneurope()