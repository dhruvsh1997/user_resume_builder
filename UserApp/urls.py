from django.urls import path
from .views import user_form, get_resume_status

urlpatterns = [
    path('', user_form, name='user_form'),
    path('check_resume_status/<str:task_id>/', get_resume_status, name='check_resume_status'),
]

