from django.shortcuts import render, redirect
from django.urls import reverse
from Device.models import UserMst ,DeviceMst, DeviceSoftMst
import logging
#------------------------------------------------------------------------------------------------#

# 詳細
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし  

def detail_device(request, intUsr, intDevice ):
    try:
         
        #不正アクセスが起きた場合
        objuser = UserMst.objects.filter( id = intUsr ).first()          
        if objuser is None  :
            
            # ログイン画面に移行
            request.session.flush()
            strurl = reverse( 'login' )
            return redirect( strurl )
        
        # 引数で渡すものを指定
        insuser = UserMst.objects.filter( id = intUsr ).first()  

        device = DeviceMst.objects.filter( id = intDevice ).first()  

        devicesofts = DeviceSoftMst.objects.filter( dsvDevice = device )  

        # 共通パラメータ定義
        params = {
            'User'          : insuser,
            'device'        : device,  
            'devicesofts'  : devicesofts,                  
            }
         
        # GET時処理
        if request.method == 'GET':

            # ホーム画面表示
            return render( request, 'Detail_Device.html', params )    
        
        # POST時処理
        if request.method == 'POST':

            # 戻るボタン押下時
            if 'btnBack' in request.POST:

                # ホーム画面に移行
                strurl = reverse( 'home_customer', kwargs = { 'intUsr'  : intUsr } )
                return redirect( strurl )
            
    except:
        # トレース設定
        import traceback

        # ログ出力
        logger = logging.getLogger(__name__)
        logger.error( request )
        logger.error( traceback.format_exc() )

    return render( request, 'Detail_Device.html', params )


# 機器登録
# 引　数：リクエスト　ユーザーID
# 戻り値：なし

# def create_device(request, intUsr ):

# 機器編集
# 引　数：リクエスト　ユーザーID　機器ID
# 戻り値：なし

# def create_device(request, intUsr, intDevice ):