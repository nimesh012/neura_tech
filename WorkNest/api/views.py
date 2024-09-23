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
            if User.objects.filter(email=request.data['email']).exists() or User.objects.filter(username=request.data['username']).exists():
                return Response({"status": 500, "data": "Email or Username already been used"})
            user = User.objects.create(**userdict)
            if user:
                user.set_password(userdict['password'])
                user.save()
        
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
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg" : "Job post created successfully.","data" : serializer.data, "status" : 200})
        else:
            return Response({"Msg" : "Job post creation failed.","data" : serializer.errors, "status" : 400})
        

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