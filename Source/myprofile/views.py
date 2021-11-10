##
# @file
# File documentation
##

from django.shortcuts import render,redirect
from .models import Profile_details
from django.core.files.storage import FileSystemStorage

def profile(request):
	email=str(request.user)+"@gmail.com"
	user_email={'email':email}
	return render(request, 'profile.html',user_email)


##
# @brief This function is used to store information of user in database.
##
def save_profile(request):
	"""
	We save the details provide by user in Profile_details Table.
	There are three types of profile user can choose Job-seeker only,Job-provider only and both.
	"""
	if request.method == 'POST':
		user_id=str(request.user)
		cur_user_email=str(request.user) + "@gmail.com"
		user=Profile_details.objects.filter(email=cur_user_email)
		if user.exists():
			Profile_details.objects.filter(user_id=user_id).delete()


		data=dict(request.POST)
		keys_data=data.keys()
		skills_dict=["skill_Carpenter","skill_Plumbing","skill_Driver","skill_House Cleaner","skill_Dog Walker","skill_Washer"]
		skills_present=[]
		for i in skills_dict:
			if i in keys_data:
				skills_present.append(i)
		user_id=str(request.user)
		name="".join(data['name'])
		email_id=str(request.user)+"@gmail.com"
		#photo="".join(data['photo'])
		mobile="".join(data['mobile'])
		aadhar="".join(data['aadhar'])
		opt="".join(data['opt'])
		#print(data)
		#print(request.POST)
		#print(request.FILES)

		image=request.FILES['photo']
		fs = FileSystemStorage()
		file_image = fs.save(image.name, image)



		str_skills=",".join(skills_present)
		#print(request.user,name,email_id,photo,mobile,aadhar,opt,str_skills)
		details=Profile_details.objects.create(user_id=user_id,
			                                   name=name,
			                                   email=email_id,
			                                   image=file_image,
			                                   phone_no=mobile,
			                                   aadhar_no=aadhar,
			                                   profile_type=opt,
			                                   skills=str_skills)
		details.save()

	return redirect('/current_location/')



##
# @brief This function is used to fetch user information from database.
##
def fetch_profile(request):
	"""
	We load profile details in our profile_details form for the user to update profile .
	"""
	user_id=str(request.user)
	print(user_id)
	user_details=Profile_details.objects.filter(user_id=user_id)
	user= user_details.values()[0]
	user=dict(user)
	print(user)
	request.session['navbar']=5
	return render(request,'fetch_profile.html',user)

	



	

