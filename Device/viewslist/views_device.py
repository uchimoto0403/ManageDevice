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
                customer_id = request.POST.get('customer_id')

                # 顧客を選択していない場合
                if not customer_id:

                    blnerror = True  

                    # パラメータ更新
                    params['RequiredError'] = blnerror

                    return render( request, 'manage_device.html', params )
             
            # 顧客情報取得
                customer = UserMst.objects.filter(id=customer_id, usrKind=1, usrDelete=False).first()
                if not customer:
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'manage_device.html', params)

                # 機器情報取得
                devices = DeviceMst.objects.filter(dvcCustomer=customer, dvcDeleteFlag=False)
                for device in devices:
                    device.has_software = DeviceSoftMst.objects.filter(dvsDeviceID=device, dvsDeleteFlag=False).exists()                

                if not devices.exists():
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'manage_device.html', params)

                # 顧客と機器リストを返す
                params['Devices'] = devices
                params['SelectedCustomer'] = customer
                params['can_output'] = devices.exists()
                return render(request, 'manage_device.html', params)

            # ソフト確認ボタン押下時
            if 'btnCheckSoftware' in request.POST:
                device_id = request.POST.get('btnCheckSoftware')
                device = DeviceMst.objects.get(id=device_id)

                # ソフト一覧を取得
                softwares = DeviceSoftMst.objects.filter(dvsDeviceID=device, dvsDeleteFlag=False)

                customer = device.dvcCustomer

                devices = DeviceMst.objects.filter(dvcCustomer=customer, dvcDeleteFlag=False)
                for device in devices:
                    device.has_software = DeviceSoftMst.objects.filter(dvsDeviceID=device, dvsDeleteFlag=False).exists()

                params['Devices'] = devices
                params['softwares'] = softwares
                params['selected_device'] = device
                params['SelectedCustomer'] = customer 
                params['open_modal'] = True
                params['can_output'] = devices.exists()

                if not softwares.exists():
                    params['error_software'] = True
                else:
                    params['softwares'] = softwares

                return render(request, 'manage_device.html', params) 

            # 編集ボタン押下時
            if 'btnEdit' in request.POST:

                device_id = request.POST.get('btnEdit')

                # redirect関数を使用し機器編集画面表示
                strurl = reverse( 'edit_device', kwargs = { 'struserid' : objuser.id, 'intDvc' : device.id } )
                return redirect( strurl )

            # 削除ボタン押下時
            if 'btnDelete' in request.POST:
                device_id = request.POST.get('btnDelete')

                with transaction.atomic():
                    # 削除対象の機器を取得
                    device = DeviceMst.objects.get(id=device_id)

                    # 削除フラグを立てて保存
                    device.dvcDeleteFlag = True
                    device.save()

                # 再検索してリスト更新（削除後にリストから消すため）
                customer = device.dvcCustomer
                devices = DeviceMst.objects.filter(dvcCustomer=customer, dvcDeleteFlag=False)
                for d in devices:
                    d.has_software = DeviceSoftMst.objects.filter(dvsDeviceID=d, dvsDeleteFlag=False).exists()

                params['Devices'] = devices
                params['SelectedCustomer'] = customer
                params['can_output'] = devices.exists()

                return render(request, 'manage_device.html', params)
            
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

            # ソフト詳細ボタン押下時
            if 'btnCheck' in request.POST:
                return render( request, 'detail_device.html', params )

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

# 機器登録
# 引　数：リクエスト　ユーザーID
# 戻り値：なし

def create_device(request, struserid):

    try:
        # 不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)
        if objuser.count() <= 0:
            # ログイン画面に移行
            request.session.flush()
            return redirect('login')

        blnerror = False
        blnerror_d = False

        # 引数で渡すものを指定
        objuser = UserMst.objects.get(id=struserid)
        customers = UserMst.objects.filter(usrKind=1, usrDelete=False)

        # 共通パラメータ定義
        params = {
            'User': objuser,                     # ユーザー情報
            'Form': DeviceForm(),                # フォーム設定
            'RequiredError': blnerror,           # 入力値エラー表示
            'DuplicateError': blnerror_d,        # 重複エラー表示 
            'struserid': struserid,              # ユーザーID  
            'customers': customers,              # 顧客情報   
        }

        # GET時処理
        if request.method == 'GET':
            return render(request, 'create_device.html', params)

        # POST時処理
        if request.method == 'POST':
            # 登録ボタン押下時
            if 'btnCreate' in request.POST:
                device_name = request.POST.get('chrDeviceName', '').strip()
                customer_id = request.POST.get('intCustomer')

                # --- 未入力チェック ---
                if not device_name or not customer_id:
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'create_device.html', params)

                # --- 顧客存在チェック ---
                customer = UserMst.objects.filter(
                    id=customer_id, usrKind=1, usrDelete=False
                ).first()
                if not customer:
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'create_device.html', params)

                # --- 重複チェック ---
                duplicate = DeviceMst.objects.filter(
                    dvcCustomer=customer,
                    dvcName=device_name,
                    dvcDeleteFlag=False
                ).exists()
                if duplicate:
                    blnerror_d = True
                    params['DuplicateError'] = blnerror_d
                    return render(request, 'create_device.html', params)

                # --- データ登録 ---
                device = DeviceMst()
                device.dvcName = device_name
                device.dvcCustomer = customer
                device.dvcKind = request.POST.get('chrDeviceKind', '')
                device.dvcMaker = request.POST.get('chrDeviceMaker', '')
                device.dvcPurchase = request.POST.get('dtDevicePurchase') or None
                device.dvcWarranty = request.POST.get('dtDeviceWarranty') or None
                device.dvcUser = request.POST.get('chrDeviceUser', '')
                device.dvcPlace = request.POST.get('chrDevicePlace', '')
                device.dvcAssetnumber = request.POST.get('chrDeviceAssetNumber', '')
                device.dvcStatus = request.POST.get('chrDeviceStatus', '')
                device.dvcSerialnumber = request.POST.get('chrDeviceSerialNumber', '')
                device.dvcOS = request.POST.get('chrDeviceOS', '')
                device.dvcCPU = request.POST.get('chrDeviceCPU', '')
                device.dvcRAM = request.POST.get('chrDeviceRAM', '')
                device.dvcGraphic = request.POST.get('chrDeviceGraphic', '')
                device.dvcStorage = request.POST.get('chrDeviceStorage', '')
                device.dvcIP = request.POST.get('chrDeviceIP', '')
                device.dvcNetWork = request.POST.get('chrDeviceNetwork', '')
                device.dvcNotes = request.POST.get('chrNotes', '')
                device.dvcDeleteFlag = False
                device.save()

                # 登録後に再度登録画面へ
                strurl = reverse('create_device', kwargs={'struserid': struserid})
                return redirect(strurl)

            # ソフト登録ボタン押下時
            if 'btnSoftCreate' in request.POST:
                return render(request, 'create_device.html', params)

            # 新規登録ボタン押下時   
            if 'btnCreateSoft' in request.POST:
                if request.POST.get('chrSoftName', '') == '':
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'create_device.html', params)
                else:
                    devicesoft = DeviceSoftMst()
                    devicesoft.dvsDeviceID = DeviceMst.objects.get(id=request.POST['intDvc'])
                    devicesoft.dvsSoftName = request.POST['chrSoftName']
                    devicesoft.dvsWarranty = request.POST['chrWarranty']
                    devicesoft.dvsDeleteFlag = False
                    devicesoft.save()
                    return render(request, 'create_device.html', params)

            # 編集ボタン押下時
            elif 'btnEdit' in request.POST:
                if request.POST.get('chrSoftName', '') == '':
                    blnerror = True
                    params['RequiredError'] = blnerror
                    return render(request, 'create_device.html', params)
                else:
                    devicesoft = DeviceSoftMst.objects.get(id=request.POST['intSoftID'])
                    devicesoft.dvsSoftName = request.POST['chrSoftName']
                    devicesoft.dvsWarranty = request.POST['chrWarranty']
                    devicesoft.save()
                    return render(request, 'create_device.html', params)

            # 削除ボタン押下時
            elif 'btnDelete' in request.POST:
                devicesoft = DeviceSoftMst.objects.get(id=request.POST['intSoftID'])
                devicesoft.dvsDeleteFlag = True
                devicesoft.save()
                return render(request, 'create_device.html', params)

            # 戻るボタン押下時
            elif 'btnBack' in request.POST:
                strurl = reverse('manage_device', kwargs={'struserid': struserid})
                return redirect(strurl)

            # ログアウトボタン押下時
            elif 'btnLogout' in request.POST:
                return redirect('login')

    except:
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(request)
        logger.error(traceback.format_exc())
        return redirect('login')

# 機器編集
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

def edit_device(request, struserid, strdevid ):

    try:
        # 不正アクセスが起きた場合
        objuser = UserMst.objects.filter(id=struserid)
        if objuser.count() <= 0:
            # ログイン画面に移行
            request.session.flush()
            return redirect('login')
        
    except:
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(request)
        logger.error(traceback.format_exc())
        return redirect('login')