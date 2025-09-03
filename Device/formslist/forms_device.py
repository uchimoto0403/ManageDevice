from django import forms

#------------------------------------------------------------------------------------------------#

#機器登録フォーム
class DeviceForm( forms.Form ):
    
#機器名
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
#種類
    chrDeviceKind = forms.ChoiceField(
        label = '種類',
        choices=DEVICE_KIND_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'width:80%',
            }
        ))
    
#メーカー
    chrDeviceMaker = forms.CharField(  
        label = 'メーカー',
        max_length = 30)
    
#型番
    chrDeviceModel = forms.CharField(
        label = '型番',
        max_length = 30)
    
#購入日
    dtDevicePurchase = forms.DateField( 
        label = '購入日',
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:30% ',
                'type': 'date' } ),
        required = False )