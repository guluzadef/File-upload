from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from .models import File


@shared_task
def test():
    """
    5 gun qalmis notf gedriki odemlesen ataw reklamin pulunu
    :return:
    """
    # print(File.objects.all())
    print('++++++++++++++++')
    checking_datas = File.objects.all()
    time = timezone.now()
    for check in checking_datas:
        file_date = check.create_date
        time_check = time - file_date
        print(time_check)
        if time_check == 7:
            print('Deleted')
            ads = File.objects.filter(id=check.id).last()
            ads.delete()

            return 'deleted'
        else:
            pass
    #
    return 'okkkkk'
