from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_customer import CustomerForm
from Device.models import UserMst
import logging
#------------------------------------------------------------------------------------------------#

# 顧客管理
# 引数：リクエスト　ユーザー種類
# 戻り値：なし

def manage_customer(request, struserid ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)    
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
        objuser = UserMst.objects.filter(id=struserid)
        customers = UserMst.objects.filter(usrKind=1, usrDelete=False)
        insform = CustomerForm()

        # 共通パラメータ定義
        params = {
            'User'                      : objuser,              # ユーザー情報
            'AccountName'               : blnname,              # 顧客名入力
            'LoginID'                   : blnloginid,           # ログインID入力
            'Password'                  : blnpassword,          # パスワード入力
            'AccountKind'               : intkind,              # アカウント種類
            'RequiredError'             : blnerror,             # 入力値エラー表示
            'DuplicateError'            : blnerror_d,           # 重複エラー表示
            'Form'                      : insform,              # フォーム設定
            'struserid'                 : struserid,            # ユーザーID    
            'customers'                 : customers,            # 顧客情報
        }
         
        # GET時処理
        if request.method == 'GET':

            # 登録している顧客情報を取得
            objuser = UserMst.objects.get(id=struserid) 
            customers = UserMst.objects.filter(usrKind=1, usrDelete=False)

            # ホーム画面表示
            return render( request, 'manage_customer.html', params )    
        
        # POST時処理
        if request.method == 'POST':

            # 登録ボタン押下時
            if 'btnCreate' in request.POST:

                # 未入力がある場合
                if ( request.POST['chrLoginID']  == '' or 
                     request.POST['chrPassWord'] == '' or
                     request.POST['chrCustomer'] == ''
                ):
                    
                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage_customer.html', params )

                # 顧客名重複チェック
                if UserMst.objects.filter(usrName=request.POST['chrCustomer'], usrDelete=False).exists():
                    blnerror = True
                    params['DuplicateError'] = blnerror
                    return render(request, 'manage_customer.html', params)

                # ログインID重複チェック
                if UserMst.objects.filter(usrLoginID=request.POST['chrLoginID'], usrDelete=False).exists():
                    blnerror = True
                    params['DuplicateError'] = blnerror
                    return render(request, 'manage_customer.html', params)

                # 入力に不備がない場合
                objuser = UserMst()
                objuser.usrLoginID   = request.POST['chrLoginID']
                objuser.usrPassWord  = request.POST['chrPassWord']
                objuser.usrName      = request.POST['chrCustomer']
                objuser.usrKind      = 1
                objuser.usrDelete    = False
                objuser.save()
                return render(request, 'manage_customer.html', params)
            
            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:

                objuser = UserMst.objects.get( id = struserid )
                return render( request, 'manage_customer.html', params )
            
            # 保存ボタン押下時
            elif 'btnSave' in request.POST:
                
                # 未入力がある場合
                if ( request.POST['chrLoginID']  == '' or 
                     request.POST['chrPassWord'] == '' or
                     request.POST['chrCustomer']     == ''
                ):
                    
                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage_customer.html', params )
                
                # 顧客名重複チェック
                if UserMst.objects.filter(usrName=request.POST['chrCustomer'], usrDelete=False).exclude(id=struserid).exists():
                    blnerror = True
                    params['DuplicateError'] = blnerror
                    return render(request, 'manage_customer.html', params)

                # ログインID重複チェック
                if UserMst.objects.filter(usrLoginID=request.POST['chrLoginID'], usrDelete=False).exclude(id=struserid).exists():
                    blnerror = True
                    params['DuplicateError'] = blnerror
                    return render(request, 'manage_customer.html', params)

                # 入力に不備がない場合（保存処理は必要に応じて追加してください）
                return render(request, 'manage_customer.html', params)
            
            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:

                objuser = UserMst.objects.get( id = struserid )
                objuser.usrDelete = True
                objuser.save()
                return render( request, 'manage_customer.html', params )        
          
            # 戻るボタン押下時
            elif 'btnBack' in request.POST:

                # ホーム_管理者画面に移行
                strurl = reverse( 'home_admin', kwargs = { 'struserid' : struserid } )
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