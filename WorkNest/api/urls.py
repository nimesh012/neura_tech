from django.contrib import admin
from django.urls import path,re_path,include
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('register/', register.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),

    path('create_recruiter_profile/', CreateRecruiterProfile.as_view(), name='create_recruiter'),
    path('edit_recruiter_profile/', EditRecruiterProfile.as_view(), name='edit_recruiter'),
    path('get_recruiter_profile/', GetRecruiterProfile.as_view(), name='get_recruiter'),
    path('delete_recruiter_profile/', DeleteRecruiterProfile.as_view(), name='delete_recruiter'),
    path('get_particular_recruiter_profile/<int:id>/', GetParticularRecruiterProfile.as_view(), name='get_particular_recruiter'),

    
    path('create_candidate/', CreateCandidateProfile.as_view(), name='create_candidate'),
    path('edit_candidate/', EditCandidateProfile.as_view(), name='edit_candidate'),
    path('get_candidate/', GetCandidateProfile.as_view(), name='get_candidate'),
    path('delete_candidate/', DeleteCandidateProfile.as_view(), name='delete_candidate'),
    path('get_particular_candidate_profile/<int:id>/', GetParticularCandidateProfile.as_view(), name='get_particular_candidate'),


    path('create_jobpost/', CreateJobPost.as_view(), name='create_jobpost'),
    path('edit_jobpost/', EditJobPost.as_view(), name='edit_jobpost'),
    path('get_jobpost/', GetJobPost.as_view(), name='get_jobpost'),
    path('delete_jobpost/', DeleteJobPost.as_view(), name='delete_jobpost'),
    path('get_particular_jobpost/<int:id>/', GetParticularJobPost.as_view(), name='get_particular_jobpost'),

    path('add_skills/', AddSkills.as_view(), name='add_skills'),
]
