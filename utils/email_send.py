from random import Random

from django.core.mail import send_mail

from imooc.settings import EMAIL_FROM
from users.models import EmailVerifyRecord

__author__ = 'Flynn'
__date__ = '2019/9/22 22:35'


def send_register_email(email, send_type='register'):
    record = EmailVerifyRecord()
    code = generate_random_str(16)
    record.code = code
    record.email = email
    record.send_type = send_type
    record.save()

    if send_type == 'register':
        email_title = '慕学在线注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '慕学在线密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def generate_random_str(random_length=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str
