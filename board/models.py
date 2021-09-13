from django.db import models
from pyexpat import model
from _datetime import datetime
from conda._vendor.auxlib.entity import IntegerField

# Create your models here.

#Board Table
class Board(models.Model):
    
    idx=models.AutoField(primary_key=True)#auto increment 같은거임
    writer=models.CharField(null=False, max_length=50)
    title=models.CharField(null=False, max_length=120)
    content=models.TextField(null=False)
    hit=models.IntegerField(default=0)#조회수 기본값 0 
    post_date=models.DateTimeField(default=datetime.now,blank=True)
    filename=models.CharField(null=True, blank=True, default="", max_length=500)
    filesize=models.IntegerField(default=0)
    down=models.IntegerField(default=0)
    
    #함수 만들기 void 같은거야
    def hit_up(self):
        self.hit+=1
        
    def down_up(self):
        self.down+=1
    
class Comment(models.Model):
    idx=models.AutoField(primary_key=True)
    board_idx=models.IntegerField(null=False)
    writer=models.CharField(null=False, max_length=50)
    content=models.TextField(null=False)
    post_date=models.DateTimeField(default=datetime.now, blank=True)
    
    
class Movie(models.Model):
    idx=models.AutoField(primary_key=True)
    title=models.CharField(null=False, max_length=500)
    content=models.TextField(null=True)
    point=models.IntegerField(default=0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
