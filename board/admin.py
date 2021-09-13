from django.contrib import admin
from board.models import Board

# Register your models here.


@admin.register(Board) #이거 둘중에 한개만 써야함
class BoardAdmin(admin.ModelAdmin):
    list_display=('idx', 'writer', 'title','content') ##리스트에서 테이블 내용중에 뭐 보여줄지 설정
    
#admin.site.regiser(Board, BoardAdmin) 이거나 어노어노
