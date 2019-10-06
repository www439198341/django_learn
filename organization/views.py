from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator

from operation.models import UserFavourite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgView(View):
    def get(self, request):
        # 从数据库中取出全部机构
        all_orgs = CourseOrg.objects.all()
        # 热门机构为全部机构按照点击数排序的前三
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 从请求中获取到city，用来筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 从请求中获取到分类，用来筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':  # 按照学习人数排序
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':  # 按照课程数排序
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()
        all_cities = CityDict.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 1, request=request)
        orgs = p.page(page)

        context = {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        }
        return render(request, 'org-list.html', context=context)


class AddUserAskView(View):
    """用户店家咨询"""

    def post(self, request):
        ask_form = UserAskForm(request.POST)
        if ask_form.is_valid():
            ask_form.save()
            return JsonResponse({'status': 'success', 'msg': ''})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class OrgHomeView(View):
    """机构首页"""

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """机构课程列表"""

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    """机构介绍"""

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    """机构讲师"""

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page
        })


class AddFavView(View):
    """用户收藏及取消收藏"""

    def post(self, request):
        # 如果未登录，则返回错误
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})

        fav_id = int(request.POST.get('fav_id', '0'))
        fav_type = int(request.POST.get('fav_type', ''))

        record = UserFavourite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if record:
            # 取消收藏，删除记录
            record.delete()
            return JsonResponse({'status': 'success', 'msg': '收藏'})
        else:
            user_fav = UserFavourite()
            if fav_id > 0 and fav_type > 0:
                user_fav.user_id = request.user.id
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({'status': 'success', 'msg': '已收藏'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort == 'hot':  # 按人气排序
            all_teachers = all_teachers.order_by('-click_nums')

        sorted_teacher = all_teachers.order_by('-click_nums')[:3]

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'sorted_teacher': sorted_teacher,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        # 判断讲师/机构是否已经收藏
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True
            if UserFavourite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'sorted_teacher': sorted_teacher,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,
        })
