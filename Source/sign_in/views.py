##
# @file
# File documentation
##

from django.shortcuts import render,redirect
from myprofile.models import Profile_details


##
# @brief This function directs user to log-in ,if user isn't logged in.Otherwise directs user to main page.
##
def index(request):
	"""
	We check if a user session is created and depending on it direct user to appropriate page.
	"""
	email=str(request.user)+"@gmail.com"
	user=Profile_details.objects.filter(email=email)
	if user.exists():
		return redirect('/current_location/')
		
	else:
		return render(request, 'signin.html')

##
# @brief This function dircts user to create a profile ,if user doesn't exist in our database.
##
def new_view(request):
	"""
	We are checking on basis of google signed-in email, if the user email exists in our database.
	If user exists in our database we direct him to mainpage.
	Else we redirect him to create a new profile.
	"""
	email=str(request.user)+"@gmail.com"
	print(email)
	user=Profile_details.objects.filter(email=email)
	if user.exists():
		return redirect('/current_location/')
		
	else:
		return redirect('/profile/')



	

