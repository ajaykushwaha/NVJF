"""NVJF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from sign_in import views as views_main
from feed import views as feed_main
from myprofile import views as profile_main
from django.conf.urls.static import static








urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
   path('logout/',
        LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),
        name='logout'
        ),
   path('', views_main.index, name='index'),
   path('feed/', feed_main.feed, name='feed'),
   path('feed/feed_update/', feed_main.feed_update, name='feed_update'),
   path('sign_in/redirect', views_main.new_view, name='new_view'),
   path('profile/', profile_main.profile, name='profile'),
   path('save_profile/', profile_main.save_profile, name='save_profile'),
   path('fetch_profile/', profile_main.fetch_profile, name='fetch_profile'),
   path('post_job/', feed_main.post_job, name='post_job'),
   path('applied_job/', feed_main.applied_job, name='applied_job'),
   path('save_applied/', feed_main.save_applied, name='save_applied'),
   path('current_location/', feed_main.current_location, name='current_location'),
   path('job_info/', feed_main.job_info, name='job_info'),
   path('applied_job_update/', feed_main.applied_job_update, name='applied_job_update'),
   
   path('delete_applied_job/', feed_main.delete_applied_job, name='delete_applied_job'),
   path('posted_job_response/', feed_main.posted_job_response, name='posted_job_response'),
   path('posted_job_response_update/', feed_main.posted_job_response_update ,name='posted_job_response_update'),



   path('show_job_responses/', feed_main.show_job_responses, name='show_job_responses'),
   path('save_job_response/', feed_main.save_job_response, name='save_job_response'),

   path('mark_complete/', feed_main.mark_complete, name='mark_complete'),


















   path('submit_job/', feed_main.submit_job, name='submit_job'),




   



]

urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
