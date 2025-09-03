from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_customer import CustomerForm
from Device.models import UserMst
import logging
#------------------------------------------------------------------------------------------------#

# 顧客管理
# 引数：リクエスト　ユーザー種類
# 戻り値：なし

def manage_customer(request, intUsr ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=intUsr)    
        if objuser.count() <= 0 : 
            
            # ログイン画面に移行
            request.session.flush()
            return redirect( 'login' )
        
        blnname         = True
        blnloginid      = True
        blnpassword     = True
        intkind         = True
        blnerror        = False
        blnerror_d      = False
        objuser = UserMst.objects.filter(id=intUsr)

        insform = CustomerForm()



        # 共通パラメータ定義
        params = {
            'AccountName'               : blnname,              # アカウント名入力
            'LoginID'                   : blnloginid,           # ログインID入力
            'Password'                  : blnpassword,          # パスワード入力
            'AccountKind'               : intkind,              # アカウント種類
            'RequiredError'             : blnerror,             # 入力値エラー表示
            'DuplicateError'            : blnerror_d,           # 重複エラー表示
            'User'                      : objuser,              # ユーザー情報
            'Form'                      : insform,              # フォーム設定      
            }
         
        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'Manage_customer.html', params )    
        
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

                    return render( request, 'customer.html', params )

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

                    return render( request, 'customer.html', params )
                
                # 入力された顧客名が既に存在する場合
                if UserMst.objects.filter( usrName = request.POST['chrName'], usrDelete = False ).exists() :
                    blnerror    = True  

                    # パラメータ更新
                    params['DuplicateError'] = blnerror

                    return render( request, 'customer.html', params )
                
                # 入力されたログインIDが既に存在する場合
                if UserMst.objects.filter( usrLoginID = request.POST['chrLoginID'], usrDelete = False ).exists() :
                    blnerror    = True  

                    # パラメータ更新
                    params['DuplicateError'] = blnerror

                    return render( request, 'customer.html', params )
                
                # 入力に不備がない場合
                else :
                    # ユーザーマスタ登録
                    objuser = UserMst()
                    objuser.usrLoginID   = request.POST['chrLoginID']
                    objuser.usrPassWord  = request.POST['chrPassWord']
                    objuser.usrName      = request.POST['chrName']
                    objuser.usrKind      = 1
                    objuser.usrMail      = request.POST['chrMailAddress']
                    objuser.usrCustomer  = request.POST['chrName']
                    objuser.save()

                return render( request, 'customer.html', params )
            
            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:

                return render( request, 'customer_m.html', params )
            
            # 保存ボタン押下時
            elif 'btnSave' in request.POST:

                return render( request, 'customer_m.html', params )
            
            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:

                

                return render( request, 'customer_m.html', params )
            
            # 戻るボタン押下時

            elif 'btnBack' in request.POST:

                # ホーム画面に移行
                strurl = reverse( 'home_admin', kwargs = { 'intUsr' : intUsr } )
                return redirect( strurl )
            
            # ログアウトボタン押下時
            elif 'btnLogout' in request.POST:

                # ログイン画面に移行
                return redirect( 'login' )

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
    
    return render(request, 'Manage_Customer.html', params)