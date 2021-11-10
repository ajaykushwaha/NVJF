from django.contrib import admin
from .models import Job_details
from .models import applied_jobs


# Register your models here.

admin.site.register(Job_details)
admin.site.register(applied_jobs)
