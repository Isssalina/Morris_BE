from django.contrib import admin
from .models import Caretaker, Healthcareprofessional, Requests, Roles, Securityquestions, Users

admin.site.register(Caretaker)
admin.site.register(Healthcareprofessional)
admin.site.register(Requests)
admin.site.register(Roles)
admin.site.register(Securityquestions)
admin.site.register(Users)
