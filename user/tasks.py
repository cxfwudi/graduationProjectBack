from tools.sms import YunTongXin
from blog_back.celery import app
from django.conf import settings

@app.task
def send_sms_celery(phone,code):   #将此任务交给celery处理（生产者）
    config = {
        "accountSid": settings.ACCOUNTSID,
        "accountToken": settings.ACCOUNTTOKEN,
        "appId": settings.APPID,
        "templateId": settings.TEMPLATEID
    }
    yun = YunTongXin(**config)  # **变为关键字传参
    res = yun.run(phone,code)
    return res