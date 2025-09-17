from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from Device.formslist.forms_admin import AdminForm
from Device.models import UserMst
from django.http import JsonResponse
import json
import re
import logging
#------------------------------------------------------------------------------------------------#

# 管理者管理
# 引数：リクエスト　ユーザー種類
# 戻り値：なし

def manage_admin(request, struserid ):
    try:
        # JSONリクエスト処理 (Ajax保存)
        if request.method == "POST" and request.content_type == "application/json":
            data = json.loads(request.body)
            if data.get("action") == "update":
                try:
                    user = UserMst.objects.get(id=data.get("id"), usrKind=2, usrDelete=False)

                    login_id = data.get("usrLoginID", user.usrLoginID)
                    password = data.get("usrPassWord", user.usrPassWord)

                    # 半角英数字チェック
                    if not re.match(r'^[A-Za-z0-9]+$', login_id) or not re.match(r'^[A-Za-z0-9]+$', password):
                        return JsonResponse({"success": False, "error": "ログインIDとパスワードは半角英数字のみです"})
                    
                    # ログインID重複チェック（自分以外）
                    if UserMst.objects.filter(
                        usrLoginID=login_id, usrDelete=False
                    ).exclude(id=user.id).exists():
                        return JsonResponse({"success": False, "error": "このログインIDは既に使用されています"})

                    # 名前重複チェック（自分以外）
                    if UserMst.objects.filter(
                        usrName=data.get("usrName", user.usrName), usrDelete=False
                    ).exclude(id=user.id).exists():
                        return JsonResponse({"success": False, "error": "この名前は既に使用されています"})

                    user.usrName = data.get("usrName", user.usrName)
                    user.usrLoginID = login_id
                    user.usrPassWord = password
                    user.usrMail = data.get("usrMail", user.usrMail)
                    user.save()
                    return JsonResponse({"success": True})
                except UserMst.DoesNotExist:
                    return JsonResponse({"success": False, "error": "対象の管理者が見つかりません"})
            return JsonResponse({"success": False, "error": "無効なアクション"})
            
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter( id = struserid )         
        if objuser.count() <= 0 :
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )    
                
        blnname         = True
        blnloginid      = True
        blnpassword     = True
        intkind         = True
        blnerror        = False
        blnerror_d      = False
        
        
        # 引数で渡すものを指定
        objuser = UserMst.objects.filter( id = struserid )   
        admins = UserMst.objects.filter(usrKind=2, usrDelete=False)

        # 共通パラメータ定義
        params = {
            'User'                      : objuser,              # ユーザー情報
            'Form'                      : AdminForm(),          # フォーム設定
            'Name'                      : blnname,              # アカウント名入力
            'LoginID'                   : blnloginid,           # ログインID入力
            'Password'                  : blnpassword,          # パスワード入力
            'Kind'                      : intkind,              # アカウント種類
            'RequiredError'             : blnerror,             # 入力値エラー表示
            'DuplicateError'            : blnerror_d,           # 重複エラー表示 
            'struserid'                 : struserid,            # ユーザーID
            'admins'                    : admins,               # 管理者情報
            }
        
        # GET時処理
        if request.method == 'GET':

            # 登録している管理者情報を取得
            objuser = UserMst.objects.get(id=struserid) 
            admins = UserMst.objects.filter(usrKind=2, usrDelete=False)

            # ホーム画面表示
            return render( request, 'manage_admin.html', params )    
        
        # POST時処理
        if request.method == 'POST':

            # 登録ボタン押下時
            if 'btnCreate' in request.POST:

                # 未入力チェック
                if not request.POST['chrLoginID'] or not request.POST['chrPassWord'] or not request.POST['chrName']:
                    params['RequiredError'] = True
                    return render(request, 'manage_admin.html', params)

                # ログインIDが既に存在するか確認
                if UserMst.objects.filter(usrLoginID=request.POST['chrLoginID'], usrDelete=False).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_admin.html', params)

                # 名前が既に存在するか確認
                if UserMst.objects.filter(usrName=request.POST['chrName'], usrDelete=False).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_admin.html', params)

                # 問題なければ登録
                with transaction.atomic():
                    objuser = UserMst()
                    objuser.usrName     = request.POST['chrName']
                    objuser.usrLoginID  = request.POST['chrLoginID']
                    objuser.usrPassWord = request.POST['chrPassWord']
                    objuser.usrMail     = request.POST['chrMail']
                    objuser.usrKind     = 2
                    objuser.usrDelete   = False
                    objuser.save()

                return redirect('manage_admin', struserid=struserid)
                
            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:

                edit_id = request.POST.get('btnEdit')   # 編集対象の管理者ID
                params['edit_id'] = int(edit_id)
                return render(request, 'manage_admin.html', params)
        
            # 保存ボタン押下時
            elif 'btnSave' in request.POST:
                edit_id = request.POST.get('edit_id')  # 編集対象の管理者ID

                # 入力内容に未入力があった場合
                if not request.POST['chrName'] or not request.POST['chrLoginID'] or not request.POST['chrPassWord']:
                    params['InputError'] = True
                    return render(request, 'manage_admin.html', params)

                # 名前重複チェック（自分以外）
                if UserMst.objects.filter(
                    usrName=request.POST['chrName'],
                    usrDelete=False
                ).exclude(id=edit_id).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_admin.html', params)

                # ログインID重複チェック（自分以外）
                if UserMst.objects.filter(
                    usrLoginID=request.POST['chrLoginID'],
                    usrDelete=False
                ).exclude(id=edit_id).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_admin.html', params)

                # 更新処理
                with transaction.atomic():
                    objuser = UserMst.objects.get(id=edit_id)
                    objuser.usrName     = request.POST['chrName']
                    objuser.usrLoginID  = request.POST['chrLoginID']
                    objuser.usrPassWord = request.POST['chrPassWord']
                    objuser.usrMail     = request.POST['chrMail']
                    objuser.save()

                return redirect('manage_admin', struserid=struserid)

            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:

                delete_id = request.POST.get('btnDelete')
                # 削除される管理者が1人だけの時
                if UserMst.objects.filter( usrKind = 2, usrDelete = False ).count() <= 1 :
                    params['DeleteError'] = True
                    return render( request, 'manage_admin.html', params )
                else :

                    with transaction.atomic():
                        user = UserMst.objects.get(id=delete_id, usrKind=2)
                        user.usrDelete = True
                        user.save()

                admins = UserMst.objects.filter(usrKind=2, usrDelete=False)
                params['admins'] = admins
                
                return render( request, 'manage_admin.html', params )
                
            # 戻るボタン押下時
            if 'btnBack' in request.POST:

                # ホーム_管理者画面に移行
                strurl = reverse( 'home_admin', kwargs = { 'struserid'  : struserid } )
                return redirect( strurl )
            
            # ログアウトボタン押下時
            elif 'btnLogout' in request.POST:

                # ログイン画面に移行
                strurl = reverse( 'login' )
                return redirect( strurl )
    
    except:
        # トレース設定
        import traceback

        # ログ出力
        logger = logging.getLogger(__name__)
        logger.error( request )
        logger.error( traceback.format_exc() )

    return render(request, 'manage_admin.html', params)