from django.urls import path
from Device.viewslist import views_login, views_home
urlpatterns = [
    #--- 申請一覧 ---#
    path('', views_login.login, name='login'),

    path('home_admin/<int:intUsr>/', views_home.home_admin, name='home_admin'),
    
    path('home_customer/<int:intUsr>', views_home.home_customer, name='home_customer'),

 

]