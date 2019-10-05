from datetime import datetime

from django.db import models

# Create your models here.
from organization.models import CourseOrg


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100)
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
