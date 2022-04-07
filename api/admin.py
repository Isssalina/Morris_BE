from django.contrib import admin
from .models import Caretaker, Healthcareprofessional, Requests, Roles, Securityquestions, Users, WorkRecord


class CaretakerAdmin(admin.ModelAdmin):
    list_display = ['takerID', 'firstName', 'lastName', 'phoneNumber', 'postalAddress', 'email', 'enroll', 'userID']


class SecurityquestionsAdmin(admin.ModelAdmin):
    list_display = ['question']


class RolesAdmin(admin.ModelAdmin):
    list_display = ['roleName']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['userID', 'firstName', 'lastName', 'phoneNumber', 'postalAddress', 'email']


admin.site.register(Caretaker, CaretakerAdmin)
admin.site.register(Healthcareprofessional)
admin.site.register(Requests)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Securityquestions, SecurityquestionsAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(WorkRecord)
