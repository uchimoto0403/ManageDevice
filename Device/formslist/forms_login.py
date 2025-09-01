
from django import forms

# --------------------------------------------------------------------- #

# ログインフォーム
class LoginForm( forms.Form ):

    # ログインID
    chrLoginID = forms.CharField(
        label = 'ログインID',
        max_length = 15,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'pattern' : '^[A-Za-z0-9_@.]+$',
                'placeholder': 'ログインIDを入力して下さい' } ),
        required = True,
            error_messages={'required': 'ログインIDが未入力です',} )
    
    # パスワード
    chrPassWord = forms.CharField(
        label = 'パスワード',
        max_length = 15,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:80% ',
                'pattern' : '^[A-Za-z0-9_@.]+$',
                'placeholder': 'パスワードを入力して下さい' } ),
        required = True,
            error_messages={'required': 'パスワードが未入力です',} )
