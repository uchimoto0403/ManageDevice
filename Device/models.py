from django.db import models

#------------------------------------------------------------------------------------------------#

#ユーザーマスタ

class UserMst(models.Model):

    
    usrLoginID          = models.CharField( max_length = 15 )                               #ログインID

    usrName             = models.CharField( max_length = 15 )                               #ユーザー名

    usrPassWord         = models.CharField( max_length = 15 )                               #パスワード
    
    usrKind             = models.IntegerField( choices = [( 1, '顧客' ),
                                                          ( 2, '管理者'),
                                                        ] 
                                        )                                                   #ユーザー種別
    
    usrDelete           = models.BooleanField( default = False )                            #削除フラグ
    
    usrMail             = models.CharField( max_length = 30, null = True, blank = True )    #メールアドレス
    
    usrCustomer         = models.CharField( max_length = 30, null = True, blank = True )    #顧客名

    def __str__(self):
        return str( self.id ) + '[' + str( self.usrDelete ) +']' + (self.usrName if self.usrName else self.usrCustomer)
    
class DeviceMst(models.Model):

    dvcName                 = models.CharField( max_length = 30 )                       #機器名

    dvcKind                 = models.CharField( max_length = 15, null = True, blank = True )          #種類

    dvcMaker                = models.CharField( max_length = 30, null = True, blank = True )          #メーカー

    dvcModel                = models.CharField( max_length = 30, null = True, blank = True )          #型番

    dvcPurchase             = models.DateField( null = True, blank = True )                           #購入日

    dvcWarranty             = models.DateField( null = True, blank = True )                           #保証期限

    dvcUser                 = models.CharField( max_length = 15, null = True, blank = True )          #使用者

    dvcPlace                = models.CharField( max_length = 30, null = True, blank = True )          #設置場所

    dvcAssetnumber          = models.CharField( max_length = 30, null = True, blank = True )          #資産番号

    dvcStatus               = models.CharField( max_length = 15, null = True, blank = True )          #使用可否

    dvcSerialnumber         = models.CharField( max_length = 30, null = True, blank = True )          #シリアル番号

    dvcOS                   = models.CharField( max_length = 15, null = True, blank = True )          #OS

    dvcCPU                  = models.CharField( max_length = 15, null = True, blank = True )          #CPU

    dvcRAM                  = models.CharField( max_length = 15, null = True, blank = True )          #RAM

    dvcGraphic              = models.CharField( max_length = 15, null = True, blank = True )          #グラフィックカード

    dvcStorage              = models.CharField( max_length = 15, null = True, blank = True )          #ストレージ

    dvcIP                   = models.CharField( max_length = 30, null = True, blank = True )          #IPアドレス

    dvcNetWork              = models.CharField( max_length = 30, null = True, blank = True )          #ネットワーク

    dvcNotes                = models.CharField( max_length = 200, null = True, blank = True )         #備考欄

    dvcDeleteFlag           = models.BooleanField( default = False )                    #削除フラグ

    #----------------------外部キー----------------------#

    #顧客名
    dvcCustomer             = models.ForeignKey( 'UserMst', 
                                                on_delete = models.CASCADE,
                                                related_name = 'dvc_usr_id',
                                                null = True,
                                                blank = True
                                                ) 

    def __str__(self):
        return str( self.id ) + '[' + str( self.dvcDeleteFlag ) +']' + ( self.dvcName )
    
class DeviceSoftMst(models.Model):

    dvsSoftName         = models.CharField( max_length = 30 )                       #ソフト名

    dvsWarranty         = models.DateField()                                        #保証期限

    dvsDeleteFlag       = models.BooleanField( default = False )                    #削除フラグ

    #----------------------外部キー----------------------#

    #機器ID
    dvsDeviceID         = models.ForeignKey( 'DeviceMst', 
                                                on_delete = models.CASCADE,
                                                related_name = 'dvs_dvc_id'
                                                )   
           

    def __str__(self):
        return str( self.id ) + '[' + str( self.dvsDeleteFlag ) +']' + ( self.dvsSoftName )








#------------------------------------------------------------------------------------------------#

