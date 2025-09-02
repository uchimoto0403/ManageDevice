from django.urls import path
from Device.viewslist import views_device, views_login, views_home, views_admin, views_customer
urlpatterns = [
    #--- 申請一覧 ---#
    path('', views_login.login, name='login'),

    path('home_admin/<int:intUsr>/', views_home.home_admin, name='home_admin'),
    
    path('home_customer/<int:intUsr>', views_home.home_customer, name='home_customer'),

    path('detail_device/<int:intUsr>/<int:intDevice>', views_device.detail_device, name='detail_device'),

    path('manage_admin/<int:intUsr>/', views_admin.manage_admin, name='manage_admin'),

    path('manage_device/<int:intUsr>/', views_device.manage_device, name='manage_device'),

    #path('create_device/<int:intUsr>/', views_device.create_device, name='create_device'),

    #path('edit_device/<int:intUsr>/', views_device.edit_device, name='edit_device'),

    path('manage_customer/<int:intUsr>/', views_customer.manage_customer, name='manage_customer'),



 

]