import requests
from bs4 import BeautifulSoup
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
import re
import numpy as np
import pandas as pd
from datetime import datetime
from variables import *

def finance():
    url='http://finance.eastmoney.com/news/cgnjj.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}


    html=requests.get(url,headers).content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('p',{'class':'title'})
    newsTitle=[i.text for i in newsList]
    newsURL=[i.find('a').get('href') for i in newsList]
    print(newsTitle)
    print(newsURL)

    contents=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers).content.decode('utf-8')
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('p')
        words = ''.join(i.get_text() for i in newsList[:-2])
        contents.append(words)
    #print(contents)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':contents}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('finance_news',engine,if_exists='replace')
    print('finance_news is done.')

if __name__ == '__main__':
    finance()