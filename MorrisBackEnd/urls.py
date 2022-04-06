from django.contrib import admin
from django.urls import path, re_path
from api import views

urlpatterns = [
    path('api/auth/', views.AuthView.as_view()),
    path('api/users/', views.UserListView.as_view()),
    path('api/caretakers/', views.CareTakersView.as_view()),
    re_path('^api/caretaker/(.*?)/$', views.CareTakerView.as_view()),
    re_path('^api/caretaker_enroll/(.*?)/$', views.CareTakerEnRollView.as_view()),
    path('api/questions/', views.QuestionListView.as_view()),
    path('api/applicants/', views.HealthCareProfessionalsView.as_view()),
    re_path('^api/applicants/(.*?)/$', views.HealthCareProfessionalsView.as_view()),
    re_path('^api/applicant/(.*?)/$', views.HealthCareProfessionalView.as_view()),
    path('api/applications/', views.ApplicationsView.as_view()),
    re_path('^api/application/(.*?)/$', views.ApplicationView.as_view()),
    re_path('^api/approve/(.*?)/$', views.HcpApproveView.as_view()),
    re_path('^api/deny/(.*?)/$', views.HcpDenyView.as_view()),
    re_path('^api/question/(.*?)/$', views.QuestionView.as_view()),
    re_path('^api/user/(.*?)/$', views.UserView.as_view()),
    path('api/requests/', views.RequestsView.as_view()),
    re_path('^api/request/(.*?)/$', views.RequestView.as_view()),
    re_path('^api/available_hcp/(.*?)/$', views.AvailableHcpView.as_view()),
    path('api/assign/', views.AssignRequestView.as_view()),
    path('api/unassign/', views.AssignRequestView.as_view()),
    path('admin/', admin.site.urls),
]
