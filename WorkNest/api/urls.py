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
    path('edit_skills/', EditSkills.as_view(), name='edit_skills'),
    path('get_skills/', GetSkills.as_view(), name='get_skills'),
    path('get_particular_skills/<int:id>/', GetParticularSkill.as_view(), name='get_skills_by_candidate'),
    path('delete_skills/', DeleteSkill.as_view(), name='delete_skills'),


    path('create_job_application/', CreateJobApplication.as_view(), name='create_job_application'),
    path('get_job_application/', GetJobApplication.as_view(), name='get_job_application'),
    path('get_particular_job_application/<int:id>/', GetParticularJobApplication.as_view(), name='get_particular_job_application'),
    path('change_job_application_status/', ChangeJobApplicationStatus.as_view(), name='change_job_application_status'),
    path('delete_job_application/', DeleteJobApplication.as_view(), name='delete_job_application'),
    path('get_all_candidates_for_job/<int:id>/',GetAllCandidatesForJob.as_view(),name='get_all_candidates_for_job'),


    path('get_job_application_by_job_post/<int:id>/',GetJobApplicationByRecruiter.as_view(),name='get_job_application_by_recruiter'),
    path('get_job_application_by_candidate/<int:id>/',GetJobApplicationByCandidate.as_view(),name='get_job_application_by_candidate'),


    path('search_jobs/',SearchJobs.as_view(),name='search_jobs'),
    path('job_recommendations/<int:id>/',JobRecommendationView.as_view(),name='job_recommendations'),

    path('save_job/', SaveJobView.as_view(), name='save_job'),
    path('save_candidate/', SaveCandidateView.as_view(), name='save_candidate'),
    path('saved_jobs/<int:candidate_id>/', ListSavedJobsView.as_view(), name='list_saved_jobs'),
    path('saved_candidates/<int:job_post_id>/', ListSavedCandidatesView.as_view(), name='list_saved_candidates'),


]
