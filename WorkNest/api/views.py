from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.forms.models import model_to_dict
from django.db.models import Q,F,FloatField,Case,When,Value,BooleanField,ExpressionWrapper, IntegerField, DecimalField
import requests as requests, base64
import datetime
import jwt
import re

class register(APIView):
    def post(self, request):
        userdict = {
            "password": request.data['password'],
            "username": request.data['username'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "email": request.data['email']
        }
        if User.objects.filter(email=request.data['email']).exists() or User.objects.filter(username=request.data['username']).exists():
            return Response({"status": 500, "data": "Email or Username already exists"})
        user = User.objects.create(**userdict)
        if user:
            user.set_password(request.data['password'])
            user.save()
            return Response({"data": "user registered successfully", "status": 200})
        else:
            return Response({"data": "something went wrong", "status": 500})


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, username)):
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
            else:
                return Response({'status': 'failed', 'data': "User not found"})
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=str(username))
            if not user.check_password(password):
                return Response({'status': 'failed', 'data': "Invalid Password."})
        else:
            return Response({'status': 'failed', 'data': "User not found"})
        token_request = requests.post(
            # url="https://artesiaapi.esarwa.com/auth/token/", data={'username': username, 'password': password})
            # url="http://127.0.0.1:8000/auth/token/", data={'username': username, 'password': password})
            url="http://127.0.0.1:8005/auth/token/", data={'username': username, 'password': password})
        print(token_request.json())
        userDict = [{"username": user.username, "email": user.email,
                     "f_name": user.first_name, "l_name": user.last_name, "mobile": int(user.username)}]
        if 'access' in token_request.json():
            user.last_login = datetime.datetime.now()
            user.save()
            return Response({'status': 'success', 'token': token_request.json()['access'], 'refresh': token_request.json()['refresh'], 'user': userDict})
        elif 'detail' in token_request.json():
            return Response({'status': 'failed', 'token': token_request.json()['detail'], 'refresh': token_request.json()['refresh'], 'user': userDict})
        else:
            return Response({'status': 'failed', 'data': {"data": "Invalid Credentials.", "status": 401}})
 


class CreateCandidateProfile(APIView):
    def post(self, request):

        data = request.data
        if CandidateProfile.objects.filter(email=data['email']).exists():
            return Response({"Msg" : "Email already exists.", "status" : 403})
        if CandidateProfile.objects.filter(phone_number=data['phone_number']).exists():
            return Response({"Msg" : "Phone number already exists.", "status" : 403})
        if User.objects.filter(username=data['phone_number']).exists():
            data['user'] = User.objects.get(username=data['phone_number']).id
        else:
            userdict = {
                "password": (data['first_name']+data['phone_number']),
                "username": data['phone_number'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email']
            }
            if User.objects.filter(email=request.data['email']).exists() or User.objects.filter(username=request.data['phone_number']).exists():
                return Response({"status": 500, "data": "Email or Username already been used"})
            user = User.objects.create(**userdict)
            if user:
                user.set_password(userdict['password'])
                user.save()
                data['user'] = user.id

        
        data['user'] = User.objects.get(username=data['phone_number']).id
        serializer = CandidateProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Candidate profile created successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Candidate profile creation failed.","data" : serializer.errors, "status" : 400})
        

class EditCandidateProfile(APIView):
    def post(self, request):
        data = request.data
        if CandidateProfile.objects.filter(email=data['email']).exclude(id=data['id']).exists():
            return Response({"Msg" : "Email already exists.", "status" : 403})
        if CandidateProfile.objects.filter(phone_number=data['phone_number']).exclude(id=data['id']).exists():
            return Response({"Msg" : "Phone number already exists.", "status" : 403})
        candidate = CandidateProfile.objects.get(id=data['id'])
        serializer = CandidateProfileSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Candidate profile updated successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Candidate profile update failed.","data" : serializer.errors, "status" : 400})
        

class GetCandidateProfile(APIView):
    def get(self, request):
        data = CandidateProfile.objects.all()
        serializer = CandidateProfileSerializer(data, many=True)
        return Response({"data" : serializer.data, "status" : 200})
    

class DeleteCandidateProfile(APIView):
    def post(self, request):
        data = request.data
        candidate = CandidateProfile.objects.get(id=data['id'])
        candidate.delete()
        return Response({"Msg" : "Candidate profile deleted successfully.", "status" : 200})
    

class GetParticularCandidateProfile(APIView):
    def get(self, request,id):
        candidate = CandidateProfile.objects.get(id=id)
        serializer = CandidateProfileSerializer(candidate)
        return Response({"data" : serializer.data, "status" : 200})
    

class CreateRecruiterProfile(APIView):
    def post(self, request):
        data = request.data 
        if RecruiterProfile.objects.filter(company_name=data['company_name']).exists():
            return Response({"Msg" : "A Company with this name already exists.", "status" : 403})
        if RecruiterProfile.objects.filter(contact_email=data['contact_email']).exists():
            return Response({"Msg" : "Email already exists.", "status" : 403})
        if RecruiterProfile.objects.filter(phone_number=data['phone_number']).exists():
            return Response({"Msg" : "Phone number already exists.", "status" : 403})
        if User.objects.filter(username=data['phone_number']).exists():
            data['user'] = User.objects.get(username=data['phone_number']).id
        else:
            userdict = {
                "password": (data['first_name']+data['phone_number']),
                "username": data['phone_number'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email']
            }
            if User.objects.filter(email=request.data['email']).exists() or User.objects.filter(username=request.data['username']).exists():
                return Response({"status": 500, "data": "Email or Username already been used"})
            user = User.objects.create(**userdict)
            if user:
                user.set_password(userdict['password'])
                user.save()
                data['user'] = user.id
            

        serializer = RecruiterProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Recruiter profile created successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Recruiter profile creation failed.","data" : serializer.errors, "status" : 400})
        

class EditRecruiterProfile(APIView):
    def post(self, request):
        data = request.data
        if RecruiterProfile.objects.filter(company_name=data['company_name']).exclude(id=data['id']).exists():
            return Response({"Msg" : "A Company with this name already exists.", "status" : 403})
        if RecruiterProfile.objects.filter(contact_email=data['contact_email']).exclude(id=data['id']).exists():
            return Response({"Msg" : "Email already exists.", "status" : 403})
        if RecruiterProfile.objects.filter(phone_number=data['phone_number']).exclude(id=data['id']).exists():
            return Response({"Msg" : "Phone number already exists.", "status" : 403})
        recruiter = RecruiterProfile.objects.get(id=data['id'])
        serializer = RecruiterProfileSerializer(recruiter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Recruiter profile updated successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Recruiter profile update failed.","data" : serializer.errors, "status" : 400})
        

class GetRecruiterProfile(APIView):
    def get(self, request):
        data = RecruiterProfile.objects.all()
        serializer = RecruiterProfileSerializer(data, many=True)
        return Response({"data" : serializer.data, "status" : 200})
    

class GetParticularRecruiterProfile(APIView):
    def get(self, request,id):
        recruiter = RecruiterProfile.objects.get(id=id)
        serializer = RecruiterProfileSerializer(recruiter)
        return Response({"data" : serializer.data, "status" : 200})
    

class DeleteRecruiterProfile(APIView):
    def post(self, request):
        data = request.data
        recruiter = RecruiterProfile.objects.get(id=data['id'])
        recruiter.delete()
        return Response({"Msg" : "Recruiter profile deleted successfully.", "status" : 200})
    

class CreateJobPost(APIView):
    def post(self, request):
        data = request.data
        b = []
        for i in data:
            serializer = JobPostSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
            else:
                b.append(serializer.errors)
        return Response({"Msg" : "Job post created successfully.","data" : serializer.data,'error':b ,"status" : 200})
        # else:
        #     return Response({"Msg" : "Job post creation failed.","data" : serializer.errors, "status" : 400})
        

class EditJobPost(APIView):
    def post(self, request):
        data = request.data
        job = JobPost.objects.get(id=data['id'])
        serializer = JobPostSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Job post updated successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Job post update failed.","data" : serializer.errors, "status" : 400})
        

class GetJobPost(APIView):
    def get(self, request):
        data = request.data
        post = JobPost.objects.filter(recruiter = data['recruiter'])
        serializer = JobPostSerializer(post, many=True)
        return Response({"data" : serializer.data, "status" : 200})
    

class GetParticularJobPost(APIView):
    def get(self, request,id):
        job = JobPost.objects.get(id=id)
        serializer = JobPostSerializer(job)
        return Response({"data" : serializer.data, "status" : 200})
    

class DeleteJobPost(APIView):
    def post(self, request):
        data = request.data
        job = JobPost.objects.get(id=data['id'])
        job.delete()
        return Response({"Msg" : "Job post deleted successfully.", "status" : 200})
    

class AddSkills(APIView):
    def post(self, request):
        data = request.data
        a = []
        b = []
        for i in data['skills']:
            serializer = SkillSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
                a.append(serializer.data)
            else:
                b.append(i)

        return Response({"Msg" : "Skills added successfully.","data" : a, "failed_skills" : b, "status" : 200})
    

class EditSkills(APIView):
    def post(self, request):
        data = request.data
        skill = Skill.objects.get(id=data['id'])
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Skill updated successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Skill update failed.","data" : serializer.errors, "status" : 400})


class GetSkills(APIView):
    def get(self, request):
        data = Skill.objects.all()
        serializer = SkillSerializer(data, many=True)
        return Response({"data" : serializer.data, "status" : 200})
    

class GetParticularSkill(APIView):
    def get(self, request,id):
        skill = Skill.objects.get(id=id)
        serializer = SkillSerializer(skill)
        return Response({"data" : serializer.data, "status" : 200}) 
    

class DeleteSkill(APIView):
    def post(self, request):
        data = request.data
        skill = Skill.objects.get(id=data['id'])
        skill.delete()
        return Response({"Msg" : "Skill deleted successfully.", "status" : 200})
    

class CreateJobApplication(APIView):
    def post(self, request):
        data = request.data
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Job application submitted successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Job application submission failed.","data" : serializer.errors, "status" : 400})
        

class EditJobApplication(APIView):
    def post(self, request):
        data = request.data 
        application = JobApplication.objects.get(id=data['id'])
        serializer = JobApplicationSerializer(application, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Job application updated successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Job application update failed.","data" : serializer.errors, "status" : 400})

class GetJobApplication(APIView):
    def get(self, request):
        data = JobApplication.objects.all()
        serializer = JobApplicationSerializer(data, many=True)
        return Response({"data" : serializer.data, "status" : 200})
    

class GetParticularJobApplication(APIView):
    def get(self, request,id):
        application = JobApplication.objects.get(id=id)
        serializer = JobApplicationSerializer(application)
        candidate = CandidateProfile.objects.get(id=application.candidate.id)
        recruiter = RecruiterProfile.objects.get(id=application.job.recruiter.id)
        candidate_serializer = CandidateProfileSerializer(candidate)
        recruiter_serializer = RecruiterProfileSerializer(recruiter)
        serializer.data['candidate'] = candidate_serializer.data
        serializer.data['recruiter'] = recruiter_serializer.data
        
        return Response({"data" : serializer.data, "status" : 200})


class ChangeJobApplicationStatus(APIView):
    def post(self, request):
        data = request.data
        application = JobApplication.objects.get(id=data['id'])
        application.status = data['status']
        application.save()
        return Response({"Msg" : "Job application status changed successfully.", "status" : 200})
    

class DeleteJobApplication(APIView):
    def post(self, request):
        data = request.data
        application = JobApplication.objects.get(id=data['id'])
        application.delete()
        return Response({"Msg" : "Job application deleted successfully.", "status" : 200})
    

class GetJobApplicationByRecruiter(APIView):
    def get(self, request, id):
        application = JobApplication.objects.filter(job = id)
        serializer = JobApplicationSerializer(application, many=True)
        for applications in serializer.data:
            candidate = CandidateProfile.objects.get(id=applications['candidate'])
            # recruiter = RecruiterProfile.objects.get(id=applications['recruiter'])
            candidate_serializer = CandidateProfileSerializer(candidate)
            # recruiter_serializer = RecruiterProfileSerializer(recruiter)
            applications['candidate'] = candidate_serializer.data
            # applications['recruiter'] = recruiter_serializer.data
        return Response({"data" : serializer.data, "status" : 200})
    

class GetJobApplicationByCandidate(APIView):
    def get(self, request, id):
        application = JobApplication.objects.filter(candidate = id)
        serializer = JobApplicationSerializer(application, many=True)
        candidate = CandidateProfile.objects.get(id=application.candidate.id)
        recruiter = RecruiterProfile.objects.get(id=application.recruiter.id)
        candidate_serializer = CandidateProfileSerializer(candidate)
        recruiter_serializer = RecruiterProfileSerializer(recruiter)
        serializer.data['candidate'] = candidate_serializer.data
        serializer.data['recruiter'] = recruiter_serializer.data
        return Response({"data" : serializer.data, "status" : 200})
    

class GetAllCandidatesForJob(APIView):
    def get(self, request, id):
        application = JobApplication.objects.filter(job = id)
        serializer = JobApplicationSerializer(application, many=True)
        application_data = serializer.data.copy()
        candidate_data = []
        for i in application_data:
            candidate = CandidateProfile.objects.get(id=i['candidate'])
            candidate_serializer = CandidateProfileSerializer(candidate)
            candidate_data.append(candidate_serializer.data.copy())
        return Response({"data" : application_data, "status" : 200})
    
from collections import defaultdict
from django.db.models import Q, Case, When, IntegerField, Count
from django.db.models.functions import Lower
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# class SearchJobs(APIView):
#     def get(self, request):
#         data = request.data
#         # Get filters from query parameters
#         title = data['title']
#         location = data['location']
#         employment_type = data['employment_type']
#         experience_required = data['experience_required']
#         skill_ids = data['skills']

#         # skill_ids = [int(skill_id) for skill_id in skill_ids]

#         # Fetch skill names based on skill IDs
#         skills = Skill.objects.filter(id__in=skill_ids).values_list('name', flat=True)
#         print(skills)
        
#           # Fetch all jobs initially
#         all_jobs = JobPost.objects.all()
#         job_scores = []

#         # Define weights for each filter
#         weights = {
#             'title': 3,               # Higher weight for title match
#             'location': 2,            # Medium weight for location match
#             'employment_type': 2,     # Medium weight for employment type match
#             'experience_required': 1, # Lower weight for experience match
#             'required_skills': 4,     # Highest weight for required skills match
#             'good_to_have_skills': 2  # Medium weight for good-to-have skills match
#         }

#         for job in all_jobs:
#             score = 0

#             # Title matching
#             if title and title.lower() in job.title.lower():
#                 score += weights['title']

#             # Location matching
#             if location and job.location and location.lower() in job.location.city.lower():
#                 score += weights['location']

#             # Employment type matching
#             if employment_type and job.employment_type and employment_type.lower() in job.employment_type.name.lower():
#                 score += weights['employment_type']

#             # Experience required matching
#             if experience_required and experience_required.lower() in job.experience_required.lower():
#                 score += weights['experience_required']

#             # Required skills matching
#             if skills:
#                 job_required_skills = set(skill.name.lower() for skill in job.required_skills.all())
#                 matched_required_skills = set(skill.lower() for skill in skills).intersection(job_required_skills)
#                 if matched_required_skills:
#                     score += weights['required_skills'] * len(matched_required_skills)

#             # Good-to-have skills matching
#             if skills:
#                 job_good_to_have_skills = set(skill.name.lower() for skill in job.good_to_have_skills.all())
#                 matched_good_to_have_skills = set(skill.lower() for skill in skills).intersection(job_good_to_have_skills)
#                 if matched_good_to_have_skills:
#                     score += weights['good_to_have_skills'] * len(matched_good_to_have_skills)

#             # Append job with its calculated score
#             job_scores.append((job, score))

#         # Sort jobs by score in descending order
#         sorted_jobs = sorted(job_scores, key=lambda x: x[1], reverse=True)

#         # Flatten sorted_jobs to just jobs (we don't need the scores for the response)
#         sorted_jobs = [job for job, _ in sorted_jobs]
#         # Serialize the jobs
#         serializer = JobPostSerializer(sorted_jobs, many=True)
#         return Response({"data" : serializer.data, "status" : 200})
    
class SearchJobs(APIView):
    def post(self, request):
        data = request.data
        # Get filters from query parameters
        title = data['title']
        location = data['location']
        employment_type = data['employment_type']
        experience_required = data['experience_required']
        skill_ids = data['skills']
        
        skill_ids = [int(skill_id) for skill_id in skill_ids]


        # Base query with no filtering, so we can score all jobs
        job_query = JobPost.objects.prefetch_related('required_skills', 'good_to_have_skills', 'location', 'employment_type')

        # Scoring conditions using Case and When
        job_query = job_query.annotate(
            title_match=Case(
                When(title__icontains=title, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if title else Value(0, output_field=IntegerField()),
            location_match=Case(
                When(location__city__icontains=location, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if location else Value(0, output_field=IntegerField()),
            employment_type_match=Case(
                When(employment_type__name__icontains=employment_type, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if employment_type else Value(0, output_field=IntegerField()),
            experience_required_match=Case(
                When(experience_required__icontains=experience_required, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if experience_required else Value(0, output_field=IntegerField()),
            # Required and Good to Have Skills Matches
            required_skills_match=Case(
                When(required_skills__id__in=skill_ids, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if skill_ids else Value(0, output_field=IntegerField()),
            good_to_have_skills_match=Case(
                When(good_to_have_skills__id__in=skill_ids, then=1),
                default=Value(0),
                output_field=IntegerField()
            ) if skill_ids else Value(0, output_field=IntegerField()),
        )

        # Total score for each job based on matching criteria
        job_query = job_query.annotate(
            total_score=(
                F('title_match') * 3 +
                F('location_match') * 2 +
                F('employment_type_match') * 2 +
                F('experience_required_match') +
                F('required_skills_match') * 4 +
                F('good_to_have_skills_match') * 2
            )
        ).order_by('-total_score')

        # Retrieve the top-matching jobs
        serializer = JobPostSerializer(job_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobRecommendationView(APIView):
    
    def get(self, request, id):
        try:
            # Retrieve candidate profile
            candidate = CandidateProfile.objects.get(id=id)
            
            # Extract skills and preferred location from the candidate profile
            skill_ids = candidate.skills.values_list('id', flat=True)
            preferred_location = candidate.preferred_location
            experience_years = candidate.experience_years
            employment_type_preference = candidate.availability  # Assuming availability indicates type preference
            
            # Start with a base query of all JobPosts
            job_query = JobPost.objects.all()

            # Annotate for skill match count
            job_query = job_query.annotate(
                skill_match_count=Count('required_skills', filter=Q(required_skills__in=skill_ids)) + 
                                  Count('good_to_have_skills', filter=Q(good_to_have_skills__in=skill_ids)),
                location_match=Case(
                    When(location__city__icontains=preferred_location, then=1),
                    default=0,
                    output_field=IntegerField()
                ),
                experience_match=Case(
                    When(experience_required__icontains=str(experience_years), then=1),
                    default=0,
                    output_field=IntegerField()
                ),
                employment_type_match=Case(
                    When(employment_type__name__icontains=employment_type_preference, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )

            # Add a total match score by summing up all the matching fields
            job_query = job_query.annotate(
                total_match_score=F('skill_match_count') + F('location_match') + F('experience_match') + F('employment_type_match')
            ).order_by('-total_match_score', '-skill_match_count')

            # Serialize the job results
            serialized_jobs = JobPostSerializer(job_query, many=True)
            return Response({'recommended_jobs': serialized_jobs.data})
        
        except CandidateProfile.DoesNotExist:
            return Response({"error": "Candidate profile not found."}, status=404)


class SaveJobView(APIView):
    def post(self, request):
        candidate_id = request.data.get('candidate_id')
        job_post_id = request.data.get('job_post_id')

        # Ensure candidate and job post exist
        try:
            candidate = CandidateProfile.objects.get(id=candidate_id)
            job_post = JobPost.objects.get(id=job_post_id)
        except (CandidateProfile.DoesNotExist, JobPost.DoesNotExist):
            return Response({'error': 'Invalid candidate or job post ID'}, status=status.HTTP_404_NOT_FOUND)

        # Create a saved job entry
        saved_job, created = SavedJob.objects.get_or_create(candidate=candidate, job_post=job_post)
        if created:
            return Response(SavedJobSerializer(saved_job).data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Job already saved'}, status=status.HTTP_200_OK)


class SaveCandidateView(APIView):
    def post(self, request):
        recruiter_id = request.data.get('recruiter_id')
        candidate_id = request.data.get('candidate_id')
        job_post_id = request.data.get('job_post_id')

        # Ensure recruiter and candidate exist
        try:
            recruiter = RecruiterProfile.objects.get(id=recruiter_id)
            candidate = CandidateProfile.objects.get(id=candidate_id)
            job_post = JobPost.objects.get(id=job_post_id)
        except (RecruiterProfile.DoesNotExist, CandidateProfile.DoesNotExist, JobPost.DoesNotExist):
            return Response({'error': 'Invalid recruiter, candidate or job post doesn`t exist'}, status=status.HTTP_404_NOT_FOUND)

        # Create a saved candidate entry
        saved_candidate, created = SavedCandidate.objects.get_or_create(recruiter=recruiter, candidate=candidate,job_post = job_post)
        if created:
            return Response(SavedCandidateSerializer(saved_candidate).data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Candidate already saved'}, status=status.HTTP_200_OK)


class ListSavedJobsView(APIView):
    def get(self, request, candidate_id):
        try:
            candidate = CandidateProfile.objects.get(id=candidate_id)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

        saved_jobs = SavedJob.objects.filter(candidate=candidate)
        return Response(SavedJobSerializer(saved_jobs, many=True).data)


class ListSavedCandidatesView(APIView):
    def get(self, request, job_post_id):
        try:
            job_post = JobPost.objects.get(id=job_post_id)
        except RecruiterProfile.DoesNotExist:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)

        saved_candidates = SavedCandidate.objects.filter(job_post=job_post)
        return Response(SavedCandidateSerializer(saved_candidates, many=True).data)
