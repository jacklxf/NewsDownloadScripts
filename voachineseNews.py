# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:33:26 2018

@author: xiaofeng.li
"""

import requests
from bs4 import BeautifulSoup
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
import re
import numpy as np
import pandas as pd
from datetime import datetime
from variables import *

def voachinese():
    url="https://www.voachinese.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}
    html=requests.get(url,headers).text
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('li',{'class':'col-xs-12 col-sm-6 col-md-6 col-lg-6'})
    newsTitle=[i.text for i in newsList]
    newsURL=['https://www.voachinese.com'+i.find('a').get('href') for i in newsList]
    print(newsTitle)
    print(newsURL)
    
    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).text
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('div',{'class':'wsw'})
        words=''.join(i.text for i in newsList)
        content.append(words)
        
    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())
    
    
    data.to_sql('voa_chinese',engine,if_exists='replace')
    print('voa_chinese is done.')

if __name__ == '__main__':
    voachinese()

