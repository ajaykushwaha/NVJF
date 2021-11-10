from django.db import models

##
# @brief This class is used to create the Profile_details table 
##
class Profile_details(models.Model):
    user_id = models.TextField(primary_key=True)
    name = models.TextField(blank=False, null=True) 
    email = models.EmailField()
    image= models.ImageField(upload_to='profile_pics/')
    phone_no = models.TextField(max_length=10)
    aadhar_no = models.TextField(max_length=12)
    choices = (
        ('1', 'Job-seeker only'),
        ('2', 'Job-provider only'),
        ('3','both')
    )
    profile_type = models.CharField(max_length=1, choices=choices)
    skills= models.TextField(blank=False, null=True)


