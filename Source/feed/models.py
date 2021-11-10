from django.db import models
from myprofile.models import Profile_details
import uuid

##
# @brief This class is used to create the Job_details table 
##
class Job_details(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_desc = models.TextField(blank=False, null=True)
    job_email = models.EmailField(null=True)
    phone_no = models.TextField(max_length=10,null=True)
    job_price = models.IntegerField(null=True)
    job_time = models.TimeField(auto_now=False)
    job_date=  models.DateField(auto_now=False)
    job_latitude=models.FloatField(null=True)
    job_address = models.TextField(blank=False, null=True)
    job_longitude=models.FloatField(null=True)
    job_skill= models.TextField(blank=False, null=True)
    job_distance=models.IntegerField(null=True)
    is_job_completed=models.BooleanField(default=False)
    image= models.TextField(blank=False, null=True)



##
# @brief This class is used to create the applied_jobs table 
##
class applied_jobs(models.Model):
    job_id=models.ForeignKey(Job_details,on_delete=models.CASCADE)
    user_id=models.ForeignKey(Profile_details,on_delete=models.CASCADE)
    is_job_approved=models.BooleanField(default=False)

    

   




