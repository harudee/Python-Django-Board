from django.shortcuts import render, redirect
from board.models import Board, Movie, Comment
from django.views.decorators.csrf import csrf_exempt

import os
import math
from django.db.models import Q
from django.utils.http import urlquote
from django.http.response import HttpResponse, HttpResponseRedirect

from pycurl import CONTENT_TYPE
from boto.beanstalk import response
from board import BigdataPro
from django.db.models.aggregates import Avg
import pandas as pd

# Create your views here.

#업로드 경로 설정
UPLOAD_DIR = 'C:/devtools/djangowork/upload/'

def home(request):
    return render(request, 'main.html')

#movie crawling
def movie_save(request):
    data=[]
    BigdataPro.movie_crwaling(data)
    for row in data:
        dto=Movie(title=row[0], point=row[1], content=row[2])
        dto.save()
    return redirect('/')

def chart(request):
    data=Movie.objects.values('title').annotation(point_avg=Avg('point')).order_by('point_avg')[0:20]
    df=pd.dataframe(data)
    BigdataPro.makeGraph(df.title, df.point_avg)
    return render(request,'bigdata_pro.html', )

# def wordcloud(requset):
#     return 
#


def cctv_map(request):
    BigdataPro.cctv_map()
    return render(request, 'map/map01.html')




# 리스트 만들었슴 사용하려면 url에 가서 설정 ㄱㄱ 
# def list(request):
#     boardCount=Board.objects.count()
#     boardList=Board.objects.all().order_by("-idx") # '-': 역순으로 정렬
#     return render(request, 'board/list.html',{'boardList':boardList, 'boardCount':boardCount})


#검색기능 추가 후 리스트 새로 만듭니다 @csrf 추가&& 검색어 추가
@csrf_exempt
def list(request):
    try:
        search_option=request.POST['search_option']
    except:
        search_option=''
        
    try:
        search = request.POST['search']
    except: 
        search=''
        
    if search_option =='all':
        boardCount=Board.objects.filter(Q(writer__contains=search)
                                        |Q(title__contains=search)
                                        |Q(content__contains=search).count())
    elif search_option =='writer':
        boardCount=Board.objects.filter(Q(writer__contains=search).count())
    elif search_option =='title':
        boardCount=Board.objects.filter(Q(title__contains=search).count())
    elif search_option =='content':
        boardCount=Board.objects.filter(Q(content__contains=search).count())
    else: 
        boardCount=Board.objects.count()
        
    
    try:
        start=int(request.GET['start'])
    except:
        start=0
        
    page_size=5
    block_size=5
    
    end=start+page_size
    
    total_page=math.ceil(boardCount/page_size)
    current_page=math.ceil((start+1)/page_size)
    start_page=math.floor((current_page-1)/block_size)*block_size+1
    end_page=start_page+block_size-1
    
    if end_page > total_page:
        end_page=total_page
    
    if start_page >= block_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
    
    if end_page < total_page:
        next_list = end_page*page_size
    else:
        next_list=0
    
    if search_option =='all':
        boardList=Board.objects.filter(Q(writer__contains=search)
                                        |Q(title__contains=search)
                                        |Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option =='writer':
        boardList=Board.objects.filter(Q(writer__contains=search)).order_by("-idx")[start:end]
    elif search_option =='title':
        boardList=Board.objects.filter(Q(title__contains=search)).order_by("-idx")[start:end]
    elif search_option =='content':
        boardList=Board.objects.filter(Q(content__contains=search)).order_by("-idx")[start:end]                                   
    else:
        boardList=Board.objects.all().order_by("-idx")[start:end]
    
    links=[]
    for i in range(start_page, end_page+1):
        page_start=(i-1)*page_size
        links.append("<a href='/list/?start="+str(page_start)+"'>"+str(i)+"</a>")
    
    return render(request, 'board/list.html',
                  {'boardList':boardList, 
                   'boardCount':boardCount,
                   'search_option':search_option,
                   'search':search,
                   'range':range(start_page-1, end_page),
                   'start_page':start_page,
                   'end_page':end_page,
                   'block_size':block_size,
                   'total_page':total_page,
                   'prev_list':prev_list,
                   'next_list':next_list,
                   'links':links})


def write(request):
    return render(request, 'board/write.html')

#sts에서 쟝고 쓰면 좀 느리니까 빨간줄 떠도 좀 기다려봐라잉
@csrf_exempt
def insert(request):
    fname=''
    fsize=0
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fsize=file.size 
        
        fp=open("%s%s"%(UPLOAD_DIR, fname), 'wb') #바이너리 쓰기 경로래
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        
    w=request.POST['writer']
    t= request.POST['title']
    c= request.POST['content']
    
    dto=Board(writer=w, title=t, content=c, filename=fname, filesize = fsize )
    dto.save()
    
    return redirect('/list/')

def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path=UPLOAD_DIR+dto.filename
    filename=os.path.basename(path)
    filename=urlquote(filename)
    with open(path, 'rb') as file:
        response=HttpResponse(file.read(), content_type='application/octect-stream')
        response['Content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)
        
        dto.down_up() #다운로드 수 증가
        dto.save()
        
        return response
    
    
def detail(request):
    id=request.GET['idx'] ##여기서 오류가 나는걸???
    dto=Board.objects.get(idx=id)
    dto.hit_up() #조회수 증가
    dto.save()
    commentList=Comment.objects.filter(board_idx=id).order_by('idx')
    
    # filesize = "%0.2f"%(dto.filesize / 1024) 키로바이트 단위 파일사이즈
    filesize="%.2f" %(dto.filesize)
    
    return render(request, "board/detail.html", 
                  {'dto':dto, 
                   'filesize':filesize, 
                   'commentList':commentList})
       
#수정기능 
@csrf_exempt    
def update(request):
    id=request.POST['idx']
    dto_src=Board.objects.get(idx=id) #기존파일 받고 시작
    fname=dto_src.filename
    fsize=0
    
    #새로 업로드 되면 처리
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fp=open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        
    fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto_new=Board(idx=id, 
                  writer=request.POST['writer'],
                  title=request.POST['title'],
                  content=request.POST['content'],
                  filename=fname, filesize=fsize)
    
    dto_new.save()
    
    return redirect("/detail/")

#삭제기능
@csrf_exempt
def delete(request):
    id=request.POST['idx']
    Board.objects.get(idx=id).delete()
    return redirect('/list/')

#댓글작성
@csrf_exempt
def reply_insert(request):
    id= request.POST['idx']
    dto=Comment(board_idx=id, 
                writer=request.POST['writer'],
                content=request.POST['content'] )
    dto.save()
    return HttpResponseRedirect("/detail?idx="+id)
    
        
        
        
         
        
        
        
        
        
        
        
        
        
        