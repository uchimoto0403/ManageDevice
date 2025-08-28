from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_admin import AdminForm
from Device.models import UserMst
import logging

#------------------------------------------------------------------------------------------------#

#管理者管理
#引　数：リクエスト　ユーザー種類
#戻り値：なし

#def manage_admin(request, intUsr):