import xadmin

from organization.models import CityDict, CourseOrg, Teacher

__author__ = 'Flynn'
__date__ = '2019/9/21 22:52'


class CityDictAdmin:
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums', 'add_time']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

