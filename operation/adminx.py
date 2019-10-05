import xadmin

from operation.models import UserAsk, CourseComment, UserFavourite, UserMessage, UserCourse

__author__ = 'Flynn'
__date__ = '2019/9/21 22:57'


class UserAskAdmin:
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']


class CourseCommentAdmin:
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


class UserFavouriteAdmin:
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']


class UserMessageAdmin:
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']


class UserCourseAdmin:
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
