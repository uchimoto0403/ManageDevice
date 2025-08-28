from django.contrib import admin

# Register your models here.
from .models import UserMst
from .models import DeviceMst
from .models import DeviceSoftMst


admin.site.register( UserMst )      #ユーザーマスタ

admin.site.register( DeviceMst )    #機器マスタ

admin.site.register( DeviceSoftMst ) #機器ソフトマスタ