from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator

from courses.models import Course, Lesson
from operation.models import UserFavourite, UserCourse, CourseComment


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 1, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
            'page_type': 'courses',
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        # 课程详情页面
        course = Course.objects.get(id=course_id)
        # 课程点击数增加1
        course.click_nums += 1
        course.save()
        # 相关课程推荐
        rel = Course.objects.filter(tag=course.tag)[:1]
        # 判断课程/机构是否已经收藏
        has_course_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_course_fav = True
            if UserFavourite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'course-detail.html', {
            'course': course,
            'rel': rel,
            'has_course_fav': has_course_fav,
            'has_org_fav': has_org_fav,
        })


class CourseVideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        if not UserCourse(user=request.user, course_id=course_id):
            UserCourse(user=request.user, course_id=course_id).save()
        similar = UserCourse.objects.filter(course_id=course_id).filter(~Q(user=request.user))[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'similar': similar,
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        comments = CourseComment.objects.order_by('-add_time').filter(user=request.user)
        return render(request, 'course-comment.html', {
            'course': course,
            'comments': comments,
        })


class AddCommentView(View):
    def post(self, request):
        if request.user.is_authenticated:
            course_id = request.POST.get('course_id', '')
            comments = request.POST.get('comments', '')
            CourseComment(user=request.user, course_id=course_id, comments=comments).save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})
