from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from Device.models import DeviceMst, DeviceSoftMst, UserMst
from datetime import timedelta

class Command(BaseCommand):
    help = "Check warranty expiry and send email alerts to admins"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        warning_date = today + timedelta(days=30)  # 30日以内に期限切れ

        # 管理者を取得（usrKind=2）
        admins = UserMst.objects.filter(usrKind=2, usrDelete=False).exclude(usrMail__isnull=True).exclude(usrMail="")

        if not admins.exists():
            self.stdout.write("送信先の管理者がいません")
            return

        recipients = [admin.usrMail for admin in admins]

        # 対象データを取得
        devices = DeviceMst.objects.filter(dvcWarranty__lte=warning_date, dvcDeleteFlag=False)
        softwares = DeviceSoftMst.objects.filter(dvsWarranty__lte=warning_date, dvsDeleteFlag=False)

        if not devices.exists() and not softwares.exists():
            self.stdout.write("期限間近の機器・ソフトはありません")
            return

        # メール本文作成
        message_lines = ["保証期限が近いものがあります:\n"]

        for d in devices:
            message_lines.append(f"機器: {d.dvcName} (期限: {d.dvcWarranty})")
        for s in softwares:
            message_lines.append(f"ソフト: {s.dvsSoftName} (期限: {s.dvsWarranty})")

        send_mail(
            subject="【警告】保証期限が近づいています",
            message="\n".join(message_lines),
            from_email="noreply@example.com",  # 送信元（SMTP設定必要）
            recipient_list=recipients,
        )

        self.stdout.write(self.style.SUCCESS("保証期限メールを送信しました"))
