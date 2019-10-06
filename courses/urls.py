from courses.views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentView

__author__ = 'Flynn'
__date__ = '2019/9/27 21:01'

app_name = 'courses'
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^course/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^video/(?P<course_id>\d+)$', CourseVideoView.as_view(), name='course_video'),
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='course_comment'),
]
