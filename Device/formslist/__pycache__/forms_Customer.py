from django import forms

#------------------------------------------------------------------------------------------------#

#顧客登録ホーム

class CustomerForm( forms.Form ):

    #顧客名
    chrCustomer = forms.CharField(
        label = '顧客名',
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'placeholder': '顧客名を入力して下さい' } ),
        required = True )
    
    #ログインID
    chrLoginID = forms.CharField(
        label = 'ログインID',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'pattern' : '^[A-Za-z0-9_@.]+$',
                'placeholder': 'ログインIDを入力して下さい' } ),
        required = True )
    
    #パスワード
    chrPassWord = forms.CharField(
        label = 'パスワード',
        max_length = 15,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'pattern' : '^[A-Za-z0-9_@.]+$',
                'placeholder': 'パスワードを入力して下さい' } ),
        required = True )
    

    