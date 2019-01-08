import pandas as pd
import requests
from bs4 import BeautifulSoup
from variables import *
from datetime import datetime
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'

def cnnchineseNews():
    url='https://www.bbc.com/zhongwen/simp/world'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers)
    html=html.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('span',{'class':'title-link__title-text'})
    newsTitle=[i.get_text() for i in newsList]
    newsList=soup.find_all('div',{'class':'eagle-item__body'})
    newsURL=['https://www.bbc.com/'+i.find('a').get('href') for i in newsList]
    print(newsTitle)
    print(newsURL)

    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers)
        html=html.content.decode('utf-8')
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('p')
        words=''.join(i.get_text() for i in newsList[17:])
        content.append(words)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('bbc_chinese',engine,if_exists='replace')
    print('bbcchineseNews is done.')

if __name__ == '__main__':
    cnnchineseNews()