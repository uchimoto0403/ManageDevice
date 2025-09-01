from django import forms 

#------------------------------------------------------------------------------------------------#

#管理者登録フォーム

    #管理者登録フォーム
class AdminForm( forms.Form ):

    #管理者名
    chrName = forms.CharField(
        label = '管理者名',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'placeholder': '名前を入力して下さい' } ),
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
    
    #メールアドレス
    chrMail = forms.CharField(
        label = 'メールアドレス',
        max_length = 30,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'pattern' : '^[A-Za-z0-9_@.]+$', } ),
        required = False )