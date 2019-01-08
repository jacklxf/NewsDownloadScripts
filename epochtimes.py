import requests
import pandas as pd
from bs4 import BeautifulSoup
from variables import *
from datetime import datetime
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'

def epochtimes():
    url='http://www.epochtimes.com/gb/nimpart.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.103 Safari/537.36'}

    html=requests.get(url,headers)
    html=html.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    newsList=soup.find_all('div',{'class':'arttitle column'})
    newsTitle=[i.get_text() for i in newsList]
    newsURL=[i.find('a').get('href') for i in newsList]
    print(newsTitle,newsURL)

    content=[]
    for i in newsURL:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/55.0.2883.103 Safari/537.36'}
        html=requests.get(i,headers)
        html=html.content.decode('utf-8')
        soup=BeautifulSoup(html,'lxml')
        newsList=soup.find_all('p')
        words=''.join(w.get_text() for w in newsList)
        content.append(words)

    dic={'ftitle':newsTitle,'furl':newsURL,'fcontent':content}
    data=pd.DataFrame.from_dict(dic)
    data.set_index('ftitle', inplace=True)
    data['fdate']=pd.to_datetime(datetime.now().date())


    data.to_sql('epochtimes',engine,if_exists='replace')
    print('epochtimes is done.')

if __name__ == '__main__':
    epochtimes()