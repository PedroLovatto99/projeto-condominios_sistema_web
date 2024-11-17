from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", BlocosListView.as_view(), name='blocos_lista' ),
    path("blocos/<int:pk>/", BlocoDetail.as_view(), name='bloco'),
    path("login/", login_view, name='login'), 
    path("logout/", logout_view, name='logout'),
    path('bloco/<int:bloco_id>/gerar_excel/', gerar_excel, name='gerar_excel'), 
    path('gerar_excel_todos_blocos/', gerar_excel_todos_blocos, name='gerar_excel_todos_blocos'),
] 
