from django.shortcuts import render, redirect
from django.urls import reverse
from Device.models import UserMst ,DeviceMst
from openpyxl import Workbook
import logging
#------------------------------------------------------------------------------------------------#

#ホーム_顧客
#引　数：リクエスト　ユーザー種類
#戻り値：なし

def home_customer(request, intUsr ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter( id = intUsr )          
        if objuser is None  :
            
            # ログイン画面に移行
            request.session.flush()
            return redirect( 'login' )
        
        # 引数で渡すものを指定
        insuser = UserMst.objects.get( id = intUsr )   # ユーザー情報

        # 共通パラメータ定義
        params = {
            'User'          : insuser,          
            }
         
        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'Home_Customer.html', params )    
        
        # POST時処理
        if request.method == 'POST':

            # 詳細ボタン押下時
            if 'btnDetail' in request.POST:

                # 詳細画面に移行
                strurl = reverse( 'detail_device', kwargs = { 'intUsr'  : intUsr , 'strDvcID' : request.POST['btnDetail'] } )
                return redirect( strurl )
            
            # 出力ボタン押下時
            elif 'btnOutput' in request.POST:
                # Excelファイル作成
                wb = Workbook()
                ws = wb.active
                ws.title = "機器一覧"

                # ユーザーの顧客に関連する機器を取得
                devices = DeviceMst.objects.filter(dvcCustomer=insuser.usrCustomer)

                # データ行の追加
                for device in devices:
                    row = [device.dvcName, device.dvcKind, device.dvcMaker, device.dvcPurchase,\
                            device.dvcWarranty, device.dvcUser, device.dvcPlace, device.dvcSoft]
                    ws.append(row)

                # HttpResponseを使用してExcelファイルを返す
                from django.http import HttpResponse       
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename=Device_List_{insuser.usrCustomer}.xlsx'
                wb.save(response)
                return response
            
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


#ホーム_管理者
#引　数：リクエスト　ユーザー種類
#戻り値：なし

def home_admin(request, intUsr):
    
    try:
        objuser = None
        
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter( id = intUsr )          
        if objuser is None  :
            
            # ログイン画面に移行
            request.session.flush()
            return redirect( 'login' )
        
        # 引数で渡すものを指定
        insuser = UserMst.objects.get( id = intUsr )   # ユーザー情報

        # 共通パラメータ定義
        params = {
            'User'          : insuser,          # ユーザー情報
            }

        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'Home_Admin.html', params )

        # POST時処理
        if request.method == 'POST':

            # 顧客管理ボタン押下時
            if 'btnCustomer' in request.POST:

                # 顧客管理画面に移行
                strurl = reverse( 'manage_customer', kwargs = { 'intUsr' : intUsr } )
                return redirect( strurl )  
            
            # 機器管理ボタン押下時
            elif 'btnDevice' in request.POST:

                # 機器管理画面に移行
                strurl = reverse( 'manage_device', kwargs = { 'intUsr' : intUsr } )
                return redirect( strurl )  
            
            # 管理者管理ボタン押下時
            elif 'btnAdmin' in request.POST:

                # 管理者管理画面に移行
                strurl = reverse( 'manage_admin', kwargs = { 'intUsr' : intUsr } )
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


    

        
