from django import forms

#------------------------------------------------------------------------------------------------#

# 機器登録フォーム
class DeviceForm( forms.Form ):
    
# 機器名
    chrDeviceName = forms.CharField(
        label = '機器名',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'placeholder': '機器名は入力必須です' } ),
        required = True )
    
    DEVICE_KIND_CHOICES = [
        ('desktop', 'デスクトップPC'),
        ('laptop', 'ノートPC'),
        ('printer', 'プリンター'),
        ('server', 'サーバー'),
        ('network', 'ネットワーク機器'),
    ]
# 種類
    chrDeviceKind = forms.ChoiceField(
        label = '種類',
        choices=DEVICE_KIND_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'width:80%',
            }
        ))
    
# メーカー
    chrDeviceMaker = forms.CharField(  
        label = 'メーカー',
        max_length = 30)
    
# 型番
    chrDeviceModel = forms.CharField(
        label = '型番',
        max_length = 30)
    
# 購入日
    dtDevicePurchase = forms.DateField( 
        label = '購入日',
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:30% ',
                'type': 'date' } ),
        required = False )

# 保障期限
    dtDeviceWarranty = forms.DateField(
        label = '保障期限',
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:30% ',
                'type': 'date' } ),
        required = False )
    
# 使用者
    chrDeviceUser = forms.CharField(
        label = '使用者',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# 設置場所
    chrDevicePlace = forms.CharField(
        label = '設置場所',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# 資産番号
    chrDeviceAssetNumber = forms.CharField(
        label = '資産番号',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# 使用可否
    chrDeviceStatus = forms.CharField(
        label = '使用可否',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )
    
# シリアル番号
    chrDeviceSerialNumber = forms.CharField(
        label = 'シリアル番号',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# OS
    chrDeviceOS = forms.CharField(
        label = 'OS',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# CPU
    chrDeviceCPU = forms.CharField(
        label = 'CPU',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# RAM
    chrDeviceRAM = forms.CharField(
        label = 'RAM',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# グラフィックカード
    chrDeviceGraphicsCard = forms.CharField(
        label = 'グラフィックカード',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# ストレージ
    chrDeviceStorage = forms.CharField(
        label = 'ストレージ',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )
    
# IPアドレス
    chrDeviceIP = forms.CharField(
        label = 'IPアドレス',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )
    
# ネットワーク
    chrDeviceNetwork = forms.CharField(
        label = 'ネットワーク',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )

# 備考欄
    chrDevice = forms.CharField(
        label = '備考欄',
        max_length = 100,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                } ), )