from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_login import LoginForm
from Device.models import UserMst
import logging
# --------------------------------------------------------------------- #

# ログイン
# 引　数：リクエスト
# 戻り値：なし

def login( request ):

    try:

        blnerror    = False         
        insform     = LoginForm()   

        # 共通パラメータ定義
        params = {
            'Form'          : insform,          # フォーム設定
            'RequiredError' : blnerror,         # ログインエラー表示
            }

        # GET時処理
        if request.method == 'GET':

            # ログイン画面表示
            return render( request, 'login.html', params )

        # POST時処理
        if request.method == 'POST':

            # ログインボタン押下時
            if 'btnLogin' in request.POST:

                # 未入力がある場合
                if ( request.POST['chrLoginID']  == '' or 
                     request.POST['chrPassWord'] == '' 
                ):
                    
                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'login.html', params )

                objuser = None
                objuser = UserMst.objects.filter( usrLoginID  = request.POST[ 'chrLoginID' ], 
                                                  usrPassWord = request.POST[ 'chrPassWord' ], 
                                                  usrDelete   = False                            
                                                ).first()                    

                # 入力に不備がある場合
                if objuser is None :
                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'login.html', params )
                
                # 入力に不備がない場合
                else :

                    # 顧客でログインする場合
                    if objuser.usrKind == 1:  
                   
                        # 顧客のホーム画面に移行
                        strurl = reverse( 'home_customer', kwargs = { 'intUsr'  : objuser.id } )
                        return redirect( strurl )  
                                      
                    # 管理者でログインする場合
                    elif objuser.usrKind == 2:
                       
                        # 管理者のホーム画面に移行
                        strurl = reverse( 'home_admin', kwargs = { 'intUsr'  : objuser.id } )
                        return redirect( strurl )
                    
                return render(request, 'login.html', params)
            
            return render(request, 'login.html', params)
                    
    except:
        # トレース設定
        import traceback

        # ログ出力
        logger = logging.getLogger(__name__)
        logger.error( request )
        logger.error( traceback.format_exc() )

        # ログイン画面に移行
        strurl = reverse( 'login' )
        return redirect( strurl )

# --------------------------------------------------------------------- #

