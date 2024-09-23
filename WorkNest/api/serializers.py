from rest_framework import serializers
from .models import *

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = '__all__'

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocation
        fields = '__all__'
