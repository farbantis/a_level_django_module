from django.core.mail import send_mail
from django.core.management import BaseCommand
from shop.models import Return


class Command(BaseCommand):
    help = 'auto close all claims for return'

    def handle(self, *args, **options):
        returns = Return.objects.all()
        quantity = returns.count()
        returns.delete()
        # it's definitely possible to send email to every applicant for return
        send_mail(
            subject='auto closure of claims notification',
            from_email='wukelan.yalishanda@gmail.com',
            message=f'all {quantity} pending claims have been successfully closed',
            recipient_list=['wukelan.yalishanda@gmail.com', ]
        )



