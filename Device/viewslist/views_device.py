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

def manage_device(request, struserid):
    try:

        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)
        if objuser.count() <= 0:

            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        
        objuser     = UserMst.objects.get(id=struserid)
        customers   = UserMst.objects.filter(usrKind=1, usrDelete=False)
        blnerror    = False
        blnerror_c  = False


        # 共通パラメータ定義
        params = {
            'User'                  : objuser,
            'struserid'             : struserid,            # ユーザーID
            'customers'             : customers,            # 顧客情報
            'Required_error'        : blnerror,
           }

        # GET時処理
        if request.method == 'GET':

            customers = UserMst.objects.filter(usrKind=1, usrDelete=False)

            # 機器管理画面表示
            return render( request, 'manage_device.html', params ) 
        
        # POST時処理
        if request.method == 'POST':

            # 機器登録ボタン押下時
            if 'btnCreate' in request.POST:

                # 機器登録画面に移行
                strurl = reverse( 'create_device', kwargs = { 'struserid' : objuser.id } )
                return redirect( strurl ) 
             
            # 検索ボタン押下時
            if 'btnSearch' in request.POST:

                # 顧客を選択していない場合
                if not objuser.usrCustomer:

                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage.device.html', params )

                # 選択した顧客の機器が登録されていない場合
                elif not DeviceMst.objects.filter(dvcCustomer=objuser).exists():

                    blnerror    = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage.device.html', params )
                
                else :
                    # 選択した顧客の機器情報を取得
                    devices = DeviceMst.objects.filter(dvcCustomer=objuser)
                    # リストに表示
                    return render( request, 'manage.device.html', { 'User': objuser, 'Devices': devices } )

            # ソフト確認ボタン押下時
            if 'btnCheck' in request.POST:

                return render( request, 'manage.device.html', { 'User': objuser, 'Devices': devices } )

            # 編集ボタン押下時
            if 'btnEdit' in request.POST:

                # redirect関数を使用し機器編集画面表示
                strurl = reverse( 'edit_device', kwargs = { 'struserid' : objuser.id, 'intDvc' : device.id } )
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

                # HttpResponseを使用してExcelファイルを返す
                from django.http import HttpResponse       
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename=Device_List_{objuser.usrCustomer}.xlsx'
                wb.save(response)
                return response
            
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
    
    return render(request, 'Manage_Device.html', params)            

# 詳細
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

def detail_device(request, struserid, strdevid ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)      
        if objuser.count() <= 0 : 
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        params = {} 
        
        # 引数で渡すものを指定
        objuser = UserMst.objects.get(id=struserid)
        device  = DeviceMst.objects.get( id = strdevid )
        devicesofts = DeviceSoftMst.objects.filter(dvsDeviceID = device, dvsDeleteFlag=False )

        # 共通パラメータ定義
        params = {
            'User'                      : objuser,
            'device'                    : device,  
            'devicesofts'               : devicesofts, 
            'struserid'                 : struserid,           # ユーザーID
            "strdevid"                  : strdevid,            # 機器ID
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
                strurl = reverse('home_customer', kwargs={'struserid': struserid})
                return redirect(strurl)
            
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

def create_device(request, struserid ):

    try:
            
            #不正アクセスが起きた場合
            objuser = UserMst.objects.filter(id=struserid)        
            if objuser.count() <= 0 :
                
                # ログイン画面に移行
                request.session.flush()
                return redirect( 'login' )
            
            blnname         = True
            blnerror        = False
            blnerror_d      = False
            
            # 引数で渡すものを指定
            objuser = UserMst.objects.get( id = struserid ) 
            devices = DeviceMst.objects.filter( dvcCustomer = objuser, dvcDeleteFlag = False )

            # 共通パラメータ定義
            params = {
                'User'                      : objuser,               # ユーザー情報
                'Form'                      : DeviceForm(),          # フォーム設定
                'AccountName'               : blnname,              # アカウント名入力
                'RequiredError'             : blnerror,             # 入力値エラー表示
                'DuplicateError'            : blnerror_d,           # 重複エラー表示 
                'struserid'                 : struserid,            # ユーザーID     
                }
            
            # GET時処理
            if request.method == 'GET':
    
                # ホーム画面表示
                return render( request, 'create_device.html', params )    
            
            # POST時処理
            if request.method == 'POST':
    
                # 登録ボタン押下時
                if 'btnCreate' in request.POST:
    
                    # 未入力がある場合
                    if ( request.POST['chrDevice']  == ''):
                        
                        blnerror    = True
    
                        # パラメータ更新
                        params['RequiredError'] = blnerror
    
                        return render( request, 'create_device.html', params )    
    
                    devices = None
                    devices = UserMst.objects.filter( dvcName = request.POST['chrDevice'], dvcDelete = False ).first()
                    
                    # 入力に不備がある場合
                    if objuser is None :   
                        blnerror_d  = True  
    
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
    
                        return render( request, 'create_device.html', params )
                    
                    # 入力された機器名が既に存在する場合

                    devices = DeviceMst.objects.filter( devName    = request.POST[ 'chrDevice' ],
                                                        devDelete  = False                            
                                                    ).first()   
                    if devices is not None :
                        blnerror_d  = True
                        # パラメータ更新
                        params['DuplicateError'] = blnerror_d
                        return render( request, 'create_device.html', params )                   

                    # 入力に不備がない場合
                    else :
                        
                        # 入力されたデータ登録
                        devices                 = DeviceMst()
                        devices.dvcKind         = request.POST['chrKind']
                        devices.dvcMaker        = request.POST['chrMaker']
                        devices.dvcPurchase     = request.POST['chrPurchase']
                        devices.dvcWarranty     = request.POST['chrWarranty']
                        devices.dvcUser         = request.POST['chrUser']
                        devices.dvcPlace        = request.POST['chrPlace']
                        devices.dvcAssetnumber  = request.POST['chrAssetnumber']
                        devices.dvcStatus       = request.POST['chrStatus']
                        devices.dvcSerialnumber = request.POST['chrSerialnumber']
                        devices.dvcOS           = request.POST['chrOS']
                        devices.dvcCPU          = request.POST['chrCPU']
                        devices.dvcRAM          = request.POST['chrRAM']
                        devices.dvcGraphic      = request.POST['chrGraphic']
                        devices.dvcStorage      = request.POST['chrStorage']
                        devices.dvcIP           = request.POST['chrIP']
                        devices.dvcNetWork      = request.POST['chrNetWork']
                        devices.dvcNotes        = request.POST['chrNotes']
                        devices.dvcDeleteFlag   = False
                        devices.save()
                        strurl = reverse( 'create_device', kwargs = { 'struserid' : struserid } )

                    return redirect( strurl )
                
                # ソフト登録ボタン押下時
                if 'btnSoftCreate' in request.POST:

                 # モーダル画面に移行
                    return render( request, 'create_device.html', params )

                # 新規登録ボタン押下時   
                if 'btnCreateSoft' in request.POST:

                    # 入力内容に未入力があった場合
                    if ( request.POST['chrSoftName']  == '' ):
                        
                        blnerror    = True

                        # パラメータ更新
                        params['RequiredError'] = blnerror

                        return render( request, 'create_device.html', params )
                    
                    else:
                        # 入力されたデータ登録
                        devicesoft = DeviceSoftMst()
                        devicesoft.dvsDeviceID    = DeviceMst.objects.get( id = request.POST['intDvc'] )
                        devicesoft.dvsSoftName    = request.POST['chrSoftName']
                        devicesoft.dvsWarranty    = request.POST['chrWarranty']
                        devicesoft.dvsDeleteFlag  = False
                        devicesoft.save()
                        
                        return render( request, 'create_device.html', params )

                # 編集ボタン押下時
                elif 'btnEdit' in request.POST:
                    # ソフト名が未入力の場合
                    if ( request.POST['chrSoftName']  == '' ):
                        
                        blnerror    = True

                        # パラメータ更新
                        params['RequiredError'] = blnerror

                        return render( request, 'create_device.html', params )
                    
                    else :
                        # 入力されたデータに更新
                        devicesoft = DeviceSoftMst.objects.get( id = request.POST['intSoftID'] )
                        devicesoft.dvsSoftName     = request.POST['chrSoftName']    
                        devicesoft.dvsWarranty     = request.POST['chrWarranty']
                        devicesoft.save()
                        return render( request, 'create_device.html', params )

                # 削除ボタン押下時
                elif 'btnDelete' in request.POST:

                    devicesoft = DeviceSoftMst.objects.get( id = request.POST['intSoftID'] )
                    devicesoft.dvsDeleteFlag = True
                    devicesoft.save()
                    return render( request, 'create_device.html', params )

                # 戻るボタン押下時
                elif 'btnBack' in request.POST:

                    # ホーム_管理者画面に移行
                    strurl = reverse( 'manage_device', kwargs = { 'struserid' : struserid } )
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

# 機器編集
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

def edit_device(request, struserid, strdevid ):

    try:
            
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)        
        if objuser.count() <= 0 :
            
            # ログイン画面に移行
            request.session.flush()
            return redirect( 'login' )
        
        blnname         = True
        blnerror        = False
        blnerror_d      = False
        
        # 引数で渡すものを指定
        objuser = UserMst.objects.filter( id = struserid ) 
        devices = DeviceMst.objects.filter( usrID = objuser, dvcDeleteFlag = False )

        # 共通パラメータ定義
        params = {
            'User'                      : objuser,               # ユーザー情報
            'Form'                      : DeviceForm(),          # フォーム設定
            'AccountName'               : blnname,              # アカウント名入力
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
                
                # 入力された機器名が既に存在する場合

                objuser = DeviceMst.objects.filter( devName    = request.POST[ 'chrName' ],
                                                    devDelete  = False                            
                                                ).first()   
                if objuser is not None :
                    blnerror_d  = True
                    # パラメータ更新
                    params['DuplicateError'] = blnerror_d
                    return render( request, 'Manage_Admin.html', params )                   

                # 入力に不備がない場合
                else :
                    
                    # 入力されたデータ登録
                    devices = DeviceMst()
                    devices.dvcKind         = request.POST['chrKind']
                    devices.dvcMaker        = request.POST['chrMaker']
                    devices.dvcPurchase     = request.POST['chrPurchase']
                    devices.dvcWarranty     = request.POST['chrWarranty']
                    devices.dvcUser         = request.POST['chrUser']
                    devices.dvcPlace        = request.POST['chrPlace']
                    devices.dvcAssetnumber  = request.POST['chrAssetnumber']
                    devices.dvcStatus       = request.POST['chrStatus']
                    devices.dvcSerialnumber = request.POST['chrSerialnumber']
                    devices.dvcOS           = request.POST['chrOS']
                    devices.dvcCPU          = request.POST['chrCPU']
                    devices.dvcRAM          = request.POST['chrRAM']
                    devices.dvcGraphic      = request.POST['chrGraphic']
                    devices.dvcStorage      = request.POST['chrStorage']
                    devices.dvcIP           = request.POST['chrIP']
                    devices.dvcNetWork      = request.POST['chrNetWork']
                    devices.dvcNotes        = request.POST['chrNotes']
                    devices.save()
                    strurl = reverse( 'create_device', kwargs = { 'struserid' : struserid } )

                return redirect( strurl )
            
            # ソフト登録ボタン押下時
            if 'btnEdit' in request.POST:
                
                # モーダル画面表示
                return render( request, 'Manage_Admin.html', params )
            
            # 新規登録ボタン押下時   
            if 'btnCreateSoft' in request.POST:

                # 入力内容に未入力があった場合
                if ( request.POST['chrSoftName']  == '' ):
                    
                    blnerror    = True

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'create_device.html', params )
                
                else:
                    # 入力されたデータ登録
                    devicesoft = DeviceSoftMst()
                    devicesoft.dvsDeviceID    = DeviceMst.objects.get( id = request.POST['intDvc'] )
                    devicesoft.dvsSoftName    = request.POST['chrSoftName']
                    devicesoft.dvsWarranty    = request.POST['chrWarranty']
                    devicesoft.dvsDeleteFlag  = False
                    devicesoft.save()
                    
                    return render( request, 'create_device.html', params )

            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:
                # ソフト名が未入力の場合
                if ( request.POST['chrSoftName']  == '' ):
                    
                    blnerror    = True

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'create_device.html', params )
                
                else :
                    # 入力されたデータに更新
                    devicesoft = DeviceSoftMst.objects.get( id = request.POST['intSoftID'] )
                    devicesoft.dvsSoftName     = request.POST['chrSoftName']    
                    devicesoft.dvsWarranty     = request.POST['chrWarranty']
                    devicesoft.save()
                    return render( request, 'create_device.html', params )

            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:

                devicesoft = DeviceSoftMst.objects.get( id = request.POST['intSoftID'] )
                devicesoft.dvsDeleteFlag = True
                devicesoft.save()
                return render( request, 'create_device.html', params )

            # 戻るボタン押下時
            elif 'btnBack' in request.POST:

                # ホーム_管理者画面に移行
                strurl = reverse( 'manage_device', kwargs = { 'struserid' : struserid } )
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
        
