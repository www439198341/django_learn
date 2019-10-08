from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator

from courses.models import Course
from operation.models import UserFavourite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UpdateUserInfoForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '账号已存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            # 想用户发送注册消息
            UserMessage(user=user_profile, message='欢迎注册').save()

            send_register_email(user_name)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            email = ''
            for record in records:
                email = record.email
            return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', '')
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'modify_form': modify_form})


class UserCenterView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'usercenter-info.html', {
            'page_type': request.GET.get('page_type')
        })


class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return JsonResponse({'status': 'fail', 'msg': '两次密码不一致'})
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return JsonResponse({'status': 'success', 'msg': '密码修改成功'})
        else:
            return JsonResponse(dict(modify_form.errors.items()), safe=False)


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email': '邮箱已经存在'})
        else:
            send_register_email(email, send_type='update_email')
            return JsonResponse({'status': 'success'})


class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证码错误'})


class UpdateUserInfoView(View):
    def post(self, request):
        update_form = UpdateUserInfoForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(dict(update_form.errors.items()))


class MyCourseView(View):
    def get(self, request):
        all_courses = Course.objects.filter(usercourse__user_id=request.user)

        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses,
            'page_type': request.GET.get('page_type'),
        })


class UserFavOrgView(View):
    def get(self, request):
        fav_ids = UserFavourite.objects.filter(user=request.user, fav_type=2)
        orgs = []
        for fav_id in fav_ids:
            org_id = fav_id.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgs.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
            'page_type': request.GET.get('page_type'),
        })


class UserFavTeacherView(View):
    def get(self, request):
        fav_ids = UserFavourite.objects.filter(user=request.user, fav_type=3)
        teachers = []
        for fav_id in fav_ids:
            teacher_id = fav_id.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
            'page_type': request.GET.get('page_type'),
        })


class UserFavCourseView(View):
    def get(self, request):
        fav_ids = UserFavourite.objects.filter(user=request.user, fav_type=1)
        courses = []
        for fav_id in fav_ids:
            course_id = fav_id.fav_id
            course = Course.objects.get(id=course_id)
            courses.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
            'page_type': request.GET.get('page_type'),
        })


class UserMessageView(View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user)

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 1, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
            'page_type': request.GET.get('page_type'),
        })

