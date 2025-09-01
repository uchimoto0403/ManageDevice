from django.shortcuts import render, redirect
from django.urls import reverse
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
            objuser = UserMst.objects.filter( id = intUsr )          
            if objuser is None  :
                
                # ログイン画面に移行
                request.session.flush()
                return redirect( 'login' )
            
            blnname         = True
            blnloginid      = True
            blnpassword     = True
            intkind         = True
            blnerror        = False
            blnerror_d      = False
            
            # 引数で渡すものを指定
            insuser = UserMst.objects.filter( id = intUsr )   # ユーザー情報
    
            # 共通パラメータ定義
            params = {
                'User'                      : insuser.first(),     # ユーザー情報
                'Form'                      : AdminForm(),         # フォーム設定
                'AccountName'               : blnname,              # アカウント名入力
                'LoginID'                   : blnloginid,           # ログインID入力
                'Password'                  : blnpassword,          # パスワード入力
                'AccountKind'               : intkind,              # アカウント種類
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
                        request.POST['chrPassWord'] == '' or
                        request.POST['chrName']     == ''
                    ):
                        
                        blnerror    = True
    
                        # パラメータ更新
                        params['RequiredError'] = blnerror
    
                        return render( request, 'Manage_Admin.html', params )    
    
                    objuser = None
                    objuser = UserMst.objects.filter( usrLoginID  = request.POST[ 'chrLoginID' ], 
                                                    usrPassWord = request.POST[ 'chrPassWord' ], 
                                                    usrDelete   = False                            
                                                ).first()
                    
                    # 入力に不備がある場合
                    if objuser is None :   
                        blnerror_d  = True  
    
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
    
                        return render( request, 'Manage_Admin.html', params )
                    # 入力に不備がない場合
                    else :
                        
                        # ホーム画面に移行
                        strurl = reverse( 'home_admin', kwargs = { 'intUsr' : intUsr } )
                        return redirect( strurl )
                    
                # 戻るボタン押下時
                if 'btnBack' in request.POST:
    
                    # ホーム画面に移行
                    strurl = reverse( 'home_admin', kwargs = { 'intUsr'  : intUsr } )
                    return redirect( strurl )
                
                # ログアウトボタン押下時
                if 'btnLogout' in request.POST:
    
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