from courses.views import CourseListView

__author__ = 'Flynn'
__date__ = '2019/9/27 21:01'

app_name = 'courses'
from django.conf.urls import url

urlpatterns = [
    url('list/', CourseListView.as_view(), name='course_list'),
]
