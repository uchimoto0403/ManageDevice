from django.urls import path
from Device.viewslist import views_device, views_login, views_home, views_admin, views_customer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #--- 申請一覧 ---#
    path('', views_login.login, name='login'),

    path('home_admin/<int:struserid>/', views_home.home_admin, name='home_admin'),

    path('home_customer/<int:struserid>/', views_home.home_customer, name='home_customer'),

    path('detail_device/<int:struserid>/<int:strdevid>', views_device.detail_device, name='detail_device'),

    path('manage_admin/<int:struserid>/', views_admin.manage_admin, name='manage_admin'),

    path('manage_device/<int:struserid>/', views_device.manage_device, name='manage_device'),

    path('create_device/<int:struserid>/', views_device.create_device, name='create_device'),

    path('edit_device/<int:struserid>/', views_device.edit_device, name='edit_device'),

    path('manage_customer/<int:struserid>/', views_customer.manage_customer, name='manage_customer'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)