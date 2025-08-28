from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_device import DeviceForm
from Device.models import DeviceMst
import logging

#------------------------------------------------------------------------------------------------#

#機器管理  
#引　数：リクエスト　ユーザー種類　機器種類
#戻り値：なし

#def device_manage(request, intUsr, intDvc):
    

#機器登録
#引　数：リクエスト　ユーザー種類　
#戻り値：なし

#def create_device(request, intUsr):

#機器編集
#引　数：リクエスト　ユーザー種類　機器ID
#戻り値：なし

#def edit_device(request, intUsr, strDvcID):

#詳細
#引　数：リクエスト　ユーザー種類　機器ID
#戻り値：なし   
#def detail_device(request, intUsr, strDvcID):