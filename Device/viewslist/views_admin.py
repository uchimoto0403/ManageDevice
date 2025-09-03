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

def manage_admin(request, intUsr ):
    try:
            
            #不正アクセスが起きた場合
            objuser = UserMst.objects.filter(id=intUsr)        
            if objuser.count() <= 0 :
                
                # ログイン画面に移行
                request.session.flush()
                strurl = reverse( 'login' )
                return redirect( strurl )    
                    
            blnname         = True
            blnloginid      = True
            blnpassword     = True
            intkind         = True
            blnmail         = True
            blnerror        = False
            blnerror_d      = False
            
            # 引数で渡すものを指定
            objuser = UserMst.objects.filter( id = intUsr )   
    
            # 共通パラメータ定義
            params = {
                'User'                      : objuser,               # ユーザー情報
                'Form'                      : AdminForm(),          # フォーム設定
                'AccountName'               : blnname,              # アカウント名入力
                'LoginID'                   : blnloginid,           # ログインID入力
                'Password'                  : blnpassword,          # パスワード入力
                'Kind'                      : intkind,              # アカウント種類
                'Mail'                      : blnmail,              # メールアドレス
                'RequiredError'             : blnerror,             # 入力値エラー表示
                'DuplicateError'            : blnerror_d,           # 重複エラー表示      
                }
            
            # GET時処理
            if request.method == 'GET':
    
                # ホーム画面表示
                return render( request, 'Manage_Admin.html', params )    
            
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
    
                        return render( request, 'Manage_Admin.html', params )    
    
                    objuser = None
                    objuser = UserMst.objects.filter( usrLoginID  = request.POST[ 'chrLoginID' ], 
                                                      usrPassWord = request.POST[ 'chrPassWord' ], 
                                                      usrName     = request.POST['chrName'],
                                                      usrDelete   = False                            
                                                ).first()
                    
                    # 入力に不備がある場合
                    if objuser is None :   
                        blnerror  = True  
    
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
    
                        return render( request, 'Manage_Admin.html', params )
                    
                    # 入力された名前が既に存在する場合
                    objuser = UserMst.objects.filter( usrName    = request.POST[ 'chrName' ],
                                                      usrDelete  = False                            
                                                    ).first()   
                    if objuser.count() > 0 :
                        blnerror_d  = True

                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
                        return render( request, 'Manage_Admin.html', params )
                    
                    # 入力されたログインIDが既に存在する場合
                    objuser = UserMst.objects.filter( usrLoginID = request.POST[ 'chrLoginID' ],
                                                      usrDelete  = False                            
                                                    ).first()
                    if objuser.count() > 0 :
                        blnerror_d  = True

                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
                        return render( request, 'Manage_Admin.html', params )                       

                    # 入力に不備がない場合
                    else :
                        # トランザクション設定
                        with transaction.atomic():

                            # 管理者新規作成
                            objuser = UserMst()
                        
                        # 入力されたデータ登録
                        objuser.usrName        = request.POST['chrName']
                        objuser.usrLoginID     = request.POST['chrLoginID']
                        objuser.usrPassWord    = request.POST['chrPassWord']
                        objuser.usrMail        = request.POST['chrMail']
                        objuser.usrKind        = 2
                        objuser.usrDelete      = False
                        objuser.save()
                        strurl = reverse( 'manage_admin', kwargs = { 'intUsr' : intUsr } )
                        return redirect( strurl )
                    
                # 編集ボタン押下時
                elif 'btnEdit' in request.POST:

                    # 押下した顧客情報取得
                    objuser = UserMst.objects.get( id = intUsr )


                    return render( request, 'customer_m.html', params )
            
                # 保存ボタン押下時
                elif 'btnSave' in request.POST:
                    
                    return render( request, 'customer_m.html', params )
            
                # 削除ボタン押下時
                elif 'btnDelete' in request.POST:
                    with transaction.atomic():
                        objuser.usrDelete = True
                        objuser.save()

                    return render( request, 'Manage_Admin.html', params )
                    
                # 戻るボタン押下時
                if 'btnBack' in request.POST:
    
                    # ホーム画面に移行
                    strurl = reverse( 'home_admin', kwargs = { 'intUsr'  : intUsr } )
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

    return render(request, 'Manage_Admin.html', params)