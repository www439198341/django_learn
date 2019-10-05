import xadmin
from xadmin import views

from users.models import UserProfile, EmailVerifyRecord, Banner

__author__ = 'Flynn'
__date__ = '2019/9/21 22:05'


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class UserProfileAdmin:
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    search_fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']


class EmailVerifyRecordAdmin:
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
