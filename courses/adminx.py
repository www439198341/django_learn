import xadmin

from courses.models import Course, Lesson, Video, CourseResource

__author__ = 'Flynn'
__date__ = '2019/9/21 22:35'


class CourseAdmin:
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'fav_nums', 'click_nums', 'add_time']


class LessonAdmin:
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin:
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResourceAdmin:
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
