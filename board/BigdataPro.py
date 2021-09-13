'''
Created on 2021. 9. 13.

@author: Harudee
'''
import requests
from bs4 import BeautifulSoup
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import os
import pandas as pd
from py_board.settings import TEMPLATE_DIR



#크롤링이 안되는데 뭐야....? 오류도 안나오고...ㅎㅎㅎ
def movie_crwaling(data):
    for i in range(1, 101):
        base="https://movie.naver.com/movie/point/af/list.naver?&page="
        url=base+str(i)
        req=requests.get(url)
        if req.ok:
            html=req.text
            soup=BeautifulSoup(html, 'html.parser')
            titles=soup.select('.title> a.movie')
            points=soup.select('.title em')
            contents=soup.select('.title')
            n=len(titles)
            
            for i in range(n):
                title=titles[i].get_text()
                point=points[i].get_text()
                contentArr=contents[i].get_text().replace('신고').split('\n\n')
                content=contentArr[2].replace('\t','').replace('\n','')
                data.append([title, point, content])
                print(title, point, content)
                
#그림그리기 -> 응 안되네
def makeGraph(title, points):
    font_path="C:/Windows/Fonts/malgun.ttf"
    font_name=font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    plt.title("영화 평점")
    plt.xlabel("영화 제목")
    plt.grid(True)
    plt.bar(range(len(titles)), points, align='center')
    plt.xticks(range(len(titles)), list(titles), rotation=90)
    plt.savefig(os.path.join(STATIC_DIR,'images/fig01.png'), dpi=300)


def cctv_map():
    popup=[]
    data_lat_lng=[]
    a_path='C:\devtools\djangowork\data'
    df=pd.read_csv(os.path.join(a_path, 'CCTV.csv'), encoding='CP949')
    print(pd)
    for data in df.values:
        if data[4] > 0:
            popup.append(data[1])
            data_lat_lng.append(data[10], data[11])
    
    m=folium.Map([], zoom_start=14)
    plugins.MarkerCluster(data_lat_lng, popups=popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR, 'map/map01.html'))
                