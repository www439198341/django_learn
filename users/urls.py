from users.views import UserCenterView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, \
    UpdateUserInfoView, MyCourseView

__author__ = 'Flynn'
__date__ = '2019/10/6 22:45'

from django.conf.urls import url


app_name = 'users'

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserCenterView.as_view(), name='user_center_info'),
    # 用户上传头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='upload_image'),
    # 用户修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^update_info/$', UpdateUserInfoView.as_view(), name='update_info'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

]