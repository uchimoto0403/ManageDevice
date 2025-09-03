from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from Device.models import UserMst ,DeviceMst, DeviceSoftMst
from Device.formslist.forms_device import DeviceForm
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import logging
#------------------------------------------------------------------------------------------------#

  

# 機器管理
# 引　数：リクエスト　ユーザーID 機器ID
# 戻り値：なし

def manage_device(request, intUsr ):
    try:

        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=intUsr)      
        if objuser.count() <= 0 : 
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        # 引数で渡すものを指定
        objuser = UserMst.objects.get(id=intUsr)

        # 共通パラメータ定義
        params = {
            'User'          : objuser,                 
            }

        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'manage.device.html', params ) 
        
        # POST時処理
        if request.method == 'POST':

            # 機器登録ボタン押下時
            if 'btnCreate' in request.POST:

                # 機器登録画面に移行
                strurl = reverse( 'create_device', kwargs = { 'intUsr' : objuser.id } )
                return redirect( strurl ) 
            
            # 検索ボタン押下時
            if 'btnSearch' in request.POST:

                # 顧客を選択していない場合
                if not objuser.usrCustomer:
                    strurl = reverse( 'create_device', kwargs = { 'intUsr' : objuser.id } )
                    return redirect( strurl )

                # 選択した顧客の機器が登録されていない場合
                if not DeviceMst.objects.filter(dvcCustomer=objuser).exists():
                    strurl = reverse( 'create_device', kwargs = { 'intUsr' : objuser.id } )
                    return redirect( strurl )
                
                else :
                    # 選択した顧客の機器情報を取得
                    devices = DeviceMst.objects.filter(dvcCustomer=objuser)
                    render( request, 'manage.device.html', { 'User': objuser, 'Devices': devices } )

            # ソフト確認ボタン押下時
            if 'btnCheck' in request.POST:

                return render( request, 'manage.device.html', { 'User': objuser, 'Devices': devices } )

            # 編集ボタン押下時
            if 'btnEdit' in request.POST:

                # redirect関数を使用し機器編集画面表示
                strurl = reverse( 'edit_device', kwargs = { 'intUsr' : objuser.id, 'intDvc' : device.id } )
                return redirect( strurl )

            # 削除ボタン押下時
            if 'btnDelete' in request.POST:
                    # トランザクション設定
                    with transaction.atomic():

                        # 削除フラグをTrueにして保存
                        objuser.usrDelete = True
                        objuser.save()

                    return render( request, 'Manage_Device.html', params )
            
            # 出力ボタン押下時
            if 'btnOutput' in request.POST:
                # Excelファイル作成
                wb = load_workbook(r"C:\Users\PC1-30_uchimoto\Desktop\Python 危機管理システム\05.コーディング\機器一覧出力_管理者用.xlsx")
                ws = wb["Sheet1"]

                ws["G3"] = objuser.usrCustomer
                
                # 登録されている機器情報取得
                devices = DeviceMst.objects.filter(dvcCustomer=objuser)

            # 開始位置を D7 に設定
                start_row = 7
                start_col = 4  

                for idx, device in enumerate(devices):
                    row_num = start_row + idx

                    softwares = device.dvs_dvc_id.all()
                    sw_names = ", ".join([sw.dvsSoftName for sw in softwares]) if softwares else ""
                    sw_warranties = ", ".join([sw.dvsWarranty.strftime("%Y-%m-%d") for sw in softwares]) if softwares else ""

                    # 機器情報とソフト情報を1行にまとめる
                    values = [
                        device.dvcName,
                        device.dvcKind,
                        device.dvcMaker,
                        device.dvcPurchase,
                        device.dvcWarranty,
                        device.dvcUser,
                        device.dvcPlace,
                        device.dvcAssetnumber,
                        device.dvcStatus,
                        device.dvcSerialnumber,
                        device.dvcOS,
                        device.dvcCPU,
                        device.dvcRAM,
                        device.dvcGraphic,
                        device.dvcStorage,
                        device.dvcIP,
                        device.dvcNetWork,
                        sw_names,
                        sw_warranties,
                        device.dvcNotes,  
                    ]

                    for col_offset, value in enumerate(values):
                        ws.cell(row=row_num, column=start_col + col_offset, value=value)

                # ===== 自動列幅調整 =====
                for col in ws.columns:
                    max_length = 0
                    col_letter = get_column_letter(col[0].column)
                    for cell in col:
                        try:
                            if cell.value:
                                max_length = max(max_length, len(str(cell.value)))
                        except:
                            pass
                    adjusted_width = max_length + 2  # 余白を持たせる
                    ws.column_dimensions[col_letter].width = adjusted_width


                # HttpResponseを使用してExcelファイルを返す
                from django.http import HttpResponse       
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename=Device_List_{objuser.usrCustomer}.xlsx'
                wb.save(response)
                return response
            
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
    
    return render(request, 'Manage_Device.html', params)            

# 詳細
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

def detail_device(request, intUsr, intDevice ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=intUsr)      
        if objuser.count() <= 0 : 
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        # 引数で渡すものを指定
        objuser = UserMst.objects.get(id=intUsr)
        device  = DeviceMst.objects.filter( id = intDevice ).first() 
        devicesofts = DeviceSoftMst.objects.filter(dvsDeviceID = device, dvsDeleteFlag=False )

        # 共通パラメータ定義
        params = {
            'User'          : objuser,
            'device'        : device,  
            'devicesofts'  : devicesofts,                  
            }
         
        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'detail_device.html', params )    
        
        # POST時処理
        if request.method == 'POST':

            # 戻るボタン押下時
            if 'btnBack' in request.POST:

                # ホーム画面に移行
                strurl = reverse( 'home_customer', kwargs = { 'intUsr'  : intUsr } )
                return redirect( strurl )
            
            # 戻るボタン(モーダル)押下時
            if 'btnBack' in request.POST:

                # ホーム画面に移行
                strurl = reverse( 'home_customer', kwargs = { 'intUsr'  : intUsr } )
                return redirect( strurl )
            
            # ログアウトボタン押下時
            elif 'btnLogout' in request.POST:

                # ログイン画面に移行
                strurl = reverse( 'login' )
                return redirect( strurl )
            
        return render(request, 'detail_device.html', params)
        
    except:
        # トレース設定
        import traceback

        # ログ出力
        logger = logging.getLogger(__name__)
        logger.error( request )
        logger.error( traceback.format_exc() )

    return render( request, 'detail_device.html', params )


# 機器登録
# 引　数：リクエスト　ユーザーID
# 戻り値：なし

def create_device(request, intUsr ):

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
            
            # 引数で渡すものを指定
            objuser = UserMst.objects.filter( id = intUsr )   
    
            # 共通パラメータ定義
            params = {
                'User'                      : objuser,               # ユーザー情報
                'Form'                      : DeviceForm(),          # フォーム設定
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
                                                      usrDelete   = False                            
                                                ).first()
                    
                    # 入力に不備がある場合
                    if objuser is None :   
                        blnerror_d  = True  
    
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
    
                        return render( request, 'Manage_Admin.html', params )
                    
                    # 入力された名前が既に存在する場合

                    objuser = UserMst.objects.filter( usrName    = request.POST[ 'chrName' ],
                                                      usrDelete  = False                            
                                                    ).first()   
                    if objuser is not None :
                        blnerror_d  = True
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
                        return render( request, 'Manage_Admin.html', params )
                    
                    # 入力されたログインIDが既に存在する場合
                    objuser = UserMst.objects.filter( usrLoginID = request.POST[ 'chrLoginID' ],
                                                      usrDelete  = False                            
                                                    ).first()
                    if objuser is not None :
                        blnerror_d  = True
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
                        return render( request, 'Manage_Admin.html', params )                       

                    # 入力に不備がない場合
                    else :
                        
                        # 入力されたデータ登録
                        objuser = UserMst()
                        objuser.usrName        = request.POST['chrName']
                        objuser.usrLoginID     = request.POST['chrLoginID']
                        objuser.usrPassWord    = request.POST['chrPassWord']
                        objuser.usrKind        = 2
                        objuser.usrDelete      = False
                        objuser.save()
                        strurl = reverse( 'home_admin', kwargs = { 'intUsr' : intUsr } )

                    return redirect( strurl )
                
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
                    


# 機器編集
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

def edit_device(request, intUsr, intDevice ):

        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=intUsr)      
        if objuser.count() <= 0 : 
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        