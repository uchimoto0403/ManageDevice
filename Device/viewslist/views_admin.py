from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from Device.formslist.forms_admin import AdminForm
from Device.models import UserMst
import logging
#------------------------------------------------------------------------------------------------#

# 管理者管理
# 引数：リクエスト　ユーザー種類
# 戻り値：なし

def manage_admin(request, struserid ):
    try:
            
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

                # 未入力がある場合
                if ( request.POST['chrLoginID']  == '' or 
                    request.POST['chrPassWord']  == '' or
                    request.POST['chrName']      == ''
                ):
                    
                    blnerror    = True

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage_admin.html', params )    

                objuser = None
                objuser = UserMst.objects.filter( usrLoginID  = request.POST[ 'chrLoginID' ], 
                                                    usrPassWord = request.POST[ 'chrPassWord' ], 
                                                    usrName     = request.POST['chrName'],
                                                    usrDelete   = False                            
                                            ).first()
                
                # 入力に不備がある場合
                if objuser is not None :   
                    blnerror  = True  

                    # パラメータ更新
                    params['DuplicateError'] = blnerror_d

                    return render( request, 'manage_admin.html', params )
                
                # 入力された名前が既に存在する場合
                objuser = UserMst.objects.filter( usrName    = request.POST[ 'chrName' ],
                                                  usrDelete  = False                            
                                                ).exists()   
                if objuser :
                    blnerror_d = True

                    # パラメータ更新
                    params['DuplicateError'] = blnerror_d
                    return render( request, 'manage_admin.html', params )
                
                # 入力されたログインIDが既に存在する場合
                objuser = UserMst.objects.filter( usrLoginID = request.POST[ 'chrLoginID' ],
                                                  usrDelete  = False                            
                                                ).exists()
                if objuser:
                    blnerror_d  = True

                    # パラメータ更新
                    params['DuplicateError'] = blnerror_d
                    return render( request, 'manage_admin.html', params )                       

                # 入力に不備がない場合
                else :
                    # トランザクション設定
                    with transaction.atomic():

                        # 管理者新規作成
                        objuser = UserMst()
                        objuser.usrName        = request.POST['chrName']
                        objuser.usrLoginID     = request.POST['chrLoginID']
                        objuser.usrPassWord    = request.POST['chrPassWord']
                        objuser.usrMail        = request.POST['chrMail']
                        objuser.usrKind        = 2
                        objuser.usrDelete      = False
                        objuser.save()
                        strurl = reverse( 'manage_admin', kwargs = { 'struserid' : struserid } )
                        return redirect( strurl )
                
            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:

                # 押下した顧客情報取得
                objuser = UserMst.objects.get( id = struserid )
                return render( request, 'manage_admin.html', params )
        
            # 保存ボタン押下時
            elif 'btnSave' in request.POST:

                # 入力内容に未入力があった場合
                if not request.POST['chrName'] or not request.POST['chrLoginID'] or not request.POST['chrPassWord']:
                    blnerror = True
                    params['InputError'] = blnerror
                    return render( request, 'manage_admin.html', params )
            
                # 入力内容に不備があった場合
                elif not request.POST['chrName'] or not request.POST['chrLoginID'] or not request.POST['chrPassWord']:
                    blnerror = True
                    params['InputError'] = blnerror     
                    return render( request, 'manage_admin.html', params )
                
                # 入力された管理者名がすでにDB(編集アカウント以外)に登録されている場合
                objuser = UserMst.objects.filter( usrName = request.POST[ 'chrName' ],
                                                    usrDelete = False ).exclude( id = struserid ).first()
                if objuser:
                    blnerror = True
                    params['InputError'] = blnerror
                    return render( request, 'manage_admin.html', params )
                
                # 入力されたログインIDがDB(編集アカウント以外)に登録されている場合
                objuser = UserMst.objects.filter( usrLoginID = request.POST[ 'chrLoginID' ],
                                                    usrDelete = False ).exclude( id = struserid ).first()
                if objuser:
                    blnerror = True
                    params['InputError'] = blnerror
                    return render( request, 'manage_admin.html', params )
                
                else :
                    with transaction.atomic():
                        objuser = UserMst.objects.get( id = struserid )
                        objuser.usrName      = request.POST['chrName']
                        objuser.usrLoginID   = request.POST['chrLoginID']
                        objuser.usrPassWord  = request.POST['chrPassWord']
                        objuser.usrMail      = request.POST['chrMail']
                        objuser.save()

                    strurl = reverse( 'manage_admin', kwargs = { 'struserid' : struserid } )

            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:
                # 削除される管理者が1人だけの時
                if UserMst.objects.filter( usrKind = 2, usrDelete = False ).count() <= 1 :
                    params['DeleteError'] = True
                    return render( request, 'manage_admin.html', params )
                else :

                    with transaction.atomic():
                        objuser = UserMst.objects.get(id=request.POST['delete_id'])
                        objuser.usrDelete = True
                        objuser.save()

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