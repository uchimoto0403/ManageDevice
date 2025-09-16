import re
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from Device.formslist.forms_customer import CustomerForm
from Device.models import UserMst

def manage_customer(request, struserid):
    try:
        objuser = UserMst.objects.filter(id=struserid)
        if objuser.count() <= 0:
            request.session.flush()
            return redirect('login')

        customers = UserMst.objects.filter(usrKind=1, usrDelete=False)
        insform = CustomerForm()

        params = {
            'User': objuser,
            'Form': insform,
            'struserid': struserid,
            'customers': customers,
            'RequiredError': False,
            'DuplicateError': False,
            'error_message': None,
            'editing_id': None,
        }

        if request.method == 'GET':
            return render(request, 'manage_customer.html', params)

        if request.method == 'POST':
            print("== POST内容 ==", request.POST)
            print("== FILES内容 ==", request.FILES)

            # 新規登録
            if 'btnCreate' in request.POST:
                if (request.POST['chrLoginID'] == '' or
                    request.POST['chrPassWord'] == '' or
                    request.POST['chrCustomer'] == ''):
                    params['RequiredError'] = True
                    return render(request, 'manage_customer.html', params)

                if UserMst.objects.filter(usrName=request.POST['chrCustomer'], usrDelete=False).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_customer.html', params)

                if UserMst.objects.filter(usrLoginID=request.POST['chrLoginID'], usrDelete=False).exists():
                    params['DuplicateError'] = True
                    return render(request, 'manage_customer.html', params)

                objuser = UserMst()
                objuser.usrLoginID = request.POST['chrLoginID']
                objuser.usrPassWord = request.POST['chrPassWord']
                objuser.usrName = request.POST['chrCustomer']
                objuser.usrKind = 1
                objuser.usrDelete = False
                if 'device_map' in request.FILES:
                    objuser.usrDeviceMap = request.FILES['device_map']
                objuser.save()
                return redirect('manage_customer', struserid=struserid)

            # 編集開始
            elif 'btnEdit' in request.POST:
                params['editing_id'] = int(request.POST.get('btnEdit'))
                return render(request, 'manage_customer.html', params)

            # 保存処理
            elif 'btnSave' in request.POST:
                customer_id = int(request.POST.get('btnSave'))
                customer = UserMst.objects.get(id=customer_id, usrKind=1, usrDelete=False)

                loginid = request.POST['chrLoginID']
                password = request.POST['chrPassWord']

                # 半角英数字チェック
                if not re.match(r'^[A-Za-z0-9]+$', loginid) or not re.match(r'^[A-Za-z0-9]+$', password):
                    params['RequiredError'] = True
                    params['error_message'] = "ログインIDとパスワードは半角英数字のみ使用できます"
                    params['editing_id'] = customer_id
                    return render(request, 'manage_customer.html', params)

                # 重複チェック
                if UserMst.objects.filter(usrName=request.POST['chrCustomer'], usrDelete=False).exclude(id=customer_id).exists():
                    params['DuplicateError'] = True
                    params['editing_id'] = customer_id
                    return render(request, 'manage_customer.html', params)

                if UserMst.objects.filter(usrLoginID=loginid, usrDelete=False).exclude(id=customer_id).exists():
                    params['DuplicateError'] = True
                    params['editing_id'] = customer_id
                    return render(request, 'manage_customer.html', params)

                # 更新
                customer.usrName = request.POST['chrCustomer']
                customer.usrLoginID = loginid
                customer.usrPassWord = password
                if f'device_map_{customer_id}' in request.FILES:
                    customer.usrDeviceMap = request.FILES[f'device_map_{customer_id}']
                customer.save()
                return redirect('manage_customer', struserid=struserid)

            # アップロード
            elif 'btnUpload' in request.POST:
                customer_id = request.POST.get('btnUpload')
                customer = UserMst.objects.get(id=customer_id, usrKind=1, usrDelete=False)
                file_key = f"device_map_{customer_id}"
                if file_key in request.FILES:
                    customer.usrDeviceMap = request.FILES[file_key]
                    customer.save()
                return redirect('manage_customer', struserid=struserid)

            # 確認
            elif 'btnCheck' in request.POST:
                customer_id = request.POST.get('btnCheck')
                customer = UserMst.objects.get(id=customer_id, usrKind=1, usrDelete=False)
                params['device_map'] = customer.usrDeviceMap.url if customer.usrDeviceMap else None
                params['open_modal'] = True
                return render(request, 'manage_customer.html', params)

            # 削除
            elif 'btnDelete' in request.POST:
                customer_id = request.POST.get('btnDelete')
                customer = UserMst.objects.get(id=customer_id, usrKind=1, usrDelete=False)
                customer.usrDelete = True
                customer.save()
                return redirect('manage_customer', struserid=struserid)

            # 戻る
            elif 'btnBack' in request.POST:
                strurl = reverse('home_admin', kwargs={'struserid': struserid})
                return redirect(strurl)

            # ログアウト
            elif 'btnLogout' in request.POST:
                return redirect('login')

    except Exception:
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(request)
        logger.error(traceback.format_exc())
        return redirect('login')

    return render(request, 'manage_customer.html', params)
