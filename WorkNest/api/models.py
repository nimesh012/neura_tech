from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    domain = models.CharField(max_length=500)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'skills'


class CompanySize(models.Model):
    size = models.CharField(max_length=50)
    class Meta:
        db_table = 'company_size'


class ContactMethod(models.Model):
    method = models.CharField(max_length=50) # Email, Phone, LinkedIn, Twitter, etc.

    class Meta:
        db_table = 'contact_method'
    

class EmploymentType(models.Model):
    name = models.CharField(max_length=50) # Full time, part time, contract, etc.

    class Meta:
        db_table = 'employees_type'

class JobStatus(models.Model):
    name = models.CharField(max_length=50) # Open, closed, hired, etc.

    class Meta:
        db_table = 'job_status'

class JobLocation(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'job_location'


class CandidateProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Professional Information
    headline = models.CharField(max_length=1000, null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    current_position = models.CharField(max_length=100, null=True, blank=True)
    current_company = models.CharField(max_length=100, null=True, blank=True)
    notice_period = models.CharField(max_length=50, null=True, blank=True) #choices=[('Immediate', 'Immediate'), ('1 month', '1 month'), ('2 months', '2 months')]
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True) # choices=[('Available', 'Available'), ('Looking for Opportunities', 'Looking for Opportunities'), ('Employed', 'Employed')]
    
    # Skills
    skills = models.ManyToManyField(Skill, blank=True)
    technical_skills = models.TextField(null=True, blank=True)  # Could be JSONField in some databases
    soft_skills = models.TextField(null=True, blank=True)
    
    # Education
    highest_degree = models.CharField(max_length=100, null=True, blank=True)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.DateField(null=True, blank=True)
    additional_certifications = models.TextField(null=True, blank=True)
    
    # Work Experience
    experience_details = models.JSONField(null=True, blank=True)
    
    # Resume and Documents
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    portfolio_link = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    
    # Other Information
    location = models.CharField(max_length=100, null=True, blank=True)
    preferred_location = models.CharField(max_length=100, null=True, blank=True)
    languages = models.TextField(null=True, blank=True)  # Could also be JSONField
    willing_to_relocate = models.BooleanField(default=False)
    visa_status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'candidate_profiles'

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(null=True, blank=True)
    # company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    designation = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    
    # Company Information
    industry = models.CharField(max_length=100, null=True, blank=True)
    company_size = models.ForeignKey(CompanySize, on_delete=models.SET_NULL, null=True, blank=True)
    company_location = models.CharField(max_length=100)
    about_company = models.TextField(null=True, blank=True)
    
    # hiring_for_roles = models.ManyToManyField('JobPost', blank=True, null = True)
    preferred_contact_method = models.ForeignKey(ContactMethod, on_delete=models.SET_NULL, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    recruitment_team_size = models.IntegerField(null=True, blank=True)
    
    # Social Links
    linkedin_company_page = models.URLField(null=True, blank=True)
    twitter_handle = models.URLField(null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    
    # Recruitment Experience
    years_of_experience = models.IntegerField(null=True, blank=True)
    specializations = models.TextField(null=True, blank=True)  # Can be JSONField in some databases
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    testimonials = models.TextField(null=True, blank=True)  # Could also be JSONField
    
    # Hiring Preferences
    employment_types = models.ManyToManyField('EmploymentType', blank=True, null = True)
    job_locations = models.ManyToManyField('JobLocation', blank=True,null = True)
    visa_sponsorship = models.BooleanField(default=False)

    class Meta:
        db_table = 'recruiter_profiles'


class JobPost(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to JobLocation model
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, blank=True)
    experience_required = models.CharField(max_length=50, null=True, blank=True)  # e.g., 2-4 years
    salary_range = models.CharField(max_length=100, null=True, blank=True)  # e.g., $60,000 - $80,000
    posted_on = models.DateTimeField(null = True, blank = True)
    application_deadline = models.DateField(null=True, blank=True)
    required_skills = models.ManyToManyField("Skill", blank=True)
    good_to_have_skills = models.ManyToManyField("Skill", blank=True,related_name='good_to_have_skills')

    status = models.ForeignKey(JobStatus, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-posted_on']
        db_table ='job_post'


class JobApplicationStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'job_application_status'

class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    status = models.ForeignKey(JobApplicationStatus, on_delete=models.SET_NULL, null=True, blank=True)
    applied_on = models.DateTimeField(null = True, blank = True)

    class Meta:
        ordering = ['-applied_on']
        db_table = 'job_application'


class SavedJob(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='saved_by_candidates')
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job_post')  # Prevent saving the same job more than once
        db_table = 'saved_jobs'


class SavedCandidate(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='saved_candidates')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,related_name='job_post')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_by_recruiters')
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recruiter', 'candidate')  # Prevent saving the same candidate more than once
        db_table = 'saved_candidates'

