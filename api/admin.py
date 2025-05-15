from multiprocessing.resource_tracker import register

from django.contrib import admin

from api.models import Course, User, TeacherSelection

admin.site.register(Course)
admin.site.register(User)
admin.site.register(TeacherSelection)

