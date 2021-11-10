##
# @file
# File documentation
##

from django.shortcuts import render,redirect
from .models import Job_details
from .models import applied_jobs
from myprofile.models import Profile_details
from math import cos, asin, sqrt, pi
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
import operator


##
# @brief This function is used genrating new Job feed for the user
##

def feed(request):
	'''This function genrates feed for user.Tasks that this function accomplishes are 
	displaying user avatar,
	Ordering jobs based on Longitude and Latitude of the current User,
	and displaying the final job feeds.
	'''

	user_id=str(request.user)
	#user_details=Profile_details.objects.filter(user_id=user_id)
	email=user_id+"@gmail.com"
	# details= Job_details.objects.filter(~Q(job_email=email))
	details= Job_details.objects.exclude(job_email=email).exclude(is_job_completed=True)
	user_details=Profile_details.objects.filter(user_id=user_id)
	jobid1 = details.values('job_id')
	jobid2 = applied_jobs.objects.filter(user_id = user_id).values('job_id__job_id')
	jobid = jobid1.difference(jobid2)

	details = details.filter(job_id__in=jobid)
	# print(details.query)
	# print(details)
	profile_image=(user_details[0].image)
	if request.method == 'POST':
		lat=request.POST['latitude']
		lon=request.POST['longitude']
		request.session['lat']=lat
		request.session['lon']=lon
	request.session['profile_type']=user_details[0].profile_type
	#print(request.session['profile_type'])
	details=get_sorted_job_details(details,float(request.session['lat']),float(request.session['lon']))
	request.session['navbar']=1
	if(user_details[0].profile_type=='2'):
		request.session['navbar']=3
		return redirect('/posted_job_response/')

	# return render(request, 'feed.html',{'details':details,'profile_image':profile_image})

	return render(request, 'feed.html',{'details':details,'profile_image':profile_image})


##
# @brief This function is used updating and filtering new Job feed for the user
##
def feed_update(request):

	'''This function updates the feed for user.Tasks that this function accomplishes are 
	Filtering job feeds on basis of price,
	on basis of skill required for the job,
	also facilitates searching in job description  of jobs through search bar. 
	'''

	if request.method == 'POST':
		user_id=str(request.user)
		email=user_id+"@gmail.com"
		if 'price' in request.POST:
			price = request.POST['price']
			#print(float(request.session['lat']),float(request.session['lon']))
			#print(price)
			# details_new= Job_details.objects.filter(job_price__gte=price)
			details_new= Job_details.objects.exclude(job_email=email).exclude(is_job_completed=True).filter(job_price__gte=price)
			print(details_new.query)
			jobid1 = details_new.values('job_id')
			jobid2 = applied_jobs.objects.filter(user_id = user_id).values('job_id__job_id')
			jobid = jobid1.difference(jobid2)

			details_new = details_new.filter(job_id__in=jobid)
			details_new=get_sorted_job_details(details_new,float(request.session['lat']),float(request.session['lon']))
			#render(request, 'feed.html',{'details':details_new})
			return render(request, 'feed_update.html',{'details':details_new})

		if 'skill' in request.POST:
			skill = request.POST['skill']
			#print(skill)
			details_new= Job_details.objects.exclude(job_email=email).exclude(is_job_completed=True).filter(job_skill__icontains=skill)
			jobid1 = details_new.values('job_id')
			jobid2 = applied_jobs.objects.filter(user_id = user_id).values('job_id__job_id')
			jobid = jobid1.difference(jobid2)

			details_new = details_new.filter(job_id__in=jobid)
			details_new=get_sorted_job_details(details_new,float(request.session['lat']),float(request.session['lon']))
			#render(request, 'feed.html',{'details':details_new})
			return render(request, 'feed_update.html',{'details':details_new})

		if 'text' in request.POST:
			text = request.POST['text']
			#print(text)
			details_new= Job_details.objects.exclude(job_email=email).exclude(is_job_completed=True).filter(job_desc__icontains=text)
			jobid1 = details_new.values('job_id')
			jobid2 = applied_jobs.objects.filter(user_id = user_id).values('job_id__job_id')
			jobid = jobid1.difference(jobid2)

			details_new = details_new.filter(job_id__in=jobid)
			details_new=get_sorted_job_details(details_new,float(request.session['lat']),float(request.session['lon']))
			#render(request, 'feed.html',{'details':details_new})
			return render(request, 'feed_update.html',{'details':details_new})

		else:
			# details= Job_details.objects.all()
			details= Job_details.objects.exclude(job_email=email).exclude(is_job_completed=True)
			jobid1 = details.values('job_id')
			jobid2 = applied_jobs.objects.filter(user_id = user_id).values('job_id__job_id')
			jobid = jobid1.difference(jobid2)

			details = details.filter(job_id__in=jobid)
			details=get_sorted_job_details(details,float(request.session['lat']),float(request.session['lon']))
			return render(request, 'feed.html',{'details':details})


##
# @brief This function is used displaying a page that job provider uses to add job.
##
def post_job(request):
	'''This function enables the job provider for adding a new job. 
	'''
	user_id=str(request.user)
	email=user_id+"@gmail.com"
	user_email={'email':email}
	request.session['navbar']=4
	return render(request, 'submitJOB.html',user_email)




##
# @brief This function is used store the job data in databse, recieved from the job provider.
##
def submit_job(request):
	'''
	This function extracts the data from the post of the frontend and populate in databsae.
	'''

	user_id=str(request.user)
	if request.method == 'POST':
		data=dict(request.POST)
		print(data)
		keys_data=data.keys()
		skills_dict=["skill_Carpenter","skill_Plumbing","skill_Driver","skill_House Cleaner","skill_Dog Walker","skill_Washer"]
		skills_present=[]
		for i in skills_dict:
			if i in keys_data:
	 			skills_present.append(i)
		job_desc=data['description'][0]
		job_email=str(request.user)+"@gmail.com"
		#job_email=data['email'][0]
		job_phone=data['mobile'][0]
		job_price=data['money'][0]
		job_time =data['time'][0]
		job_date=data['date'][0]
		job_latitude=data['latitude'][0]
		job_longitude=data['longitude'][0]
		job_address=data['map_address'][0]
		job_skill=",".join(skills_present)
		#print(request.FILES)
		photos=[]
		#image=request.FILES['images']

		for i in request.FILES.getlist('images'):
			print(i)
			fs = FileSystemStorage()
			file_image = fs.save(i.name, i)
			photos.append(file_image)
		job_pics=",".join(photos)
		details=Job_details.objects.create(job_desc=job_desc,job_email=job_email,phone_no=job_phone,
			                                    job_price=job_price,job_time=job_time,job_date=job_date,
			                                    job_latitude=job_latitude,job_longitude=job_longitude,job_address=job_address,
			                                    job_skill=job_skill,image=job_pics)
		details.save()
	
	


		#print(data)
	return redirect('/current_location/')



##
# @brief This function is used to display the job posted by job provider.
##
def job_info(request):
	"""
	This function helps to create a template of Job details to display to job-seeker.
	We first extract data of job details from database and add it to a variable.
	Then we also query the profile table in database to get details about job poster.
	After all that we generate a template using this variable.
	"""

	if request.method == 'POST':
		if 'job_id' in request.POST:
			job_id = int(request.POST['job_id'])
			detail=Job_details.objects.filter(job_id=job_id)
			detail_value=dict(detail.values()[0])
			list_image=detail_value['image'].split(",")
			detail_value['first_image']=list_image[0]
			print(len(list_image))
			if(len(list_image)>1):
				detail_value['image_new']=list_image[1:]

			email=detail_value['job_email']
			user_details=Profile_details.objects.filter(email=email)
			#print(detail_value)
			profile_image=(user_details[0].image)
			name=(user_details[0].name)
			detail_value['profile_image']=profile_image
			detail_value['name']=name
	request.session['navbar']=1		
	return render(request, 'job_details.html',detail_value)


##
# @brief This function is used to save status of job applier to the job he has applied.
##

def save_applied(request):
	"""
	This function helps to create a entry in Job-Applied table indiacting the job-seeker is interested in a particular job.
	We create a instance of a matching profile table entry and a matching job table entry.
	Then we use this instances to save a foreign key entry of the instances.
	"""
	user_id=str(request.user)
	if request.method == 'POST':
		if 'job_id' in request.POST:
			#print(request.POST)
			job_id = int(request.POST['job_id'])
			jid=Job_details.objects.only('job_id').get(job_id=job_id)
			#User.objects.only('id').get(id=data['user_id'])
			uid=Profile_details.objects.only('user_id').get(user_id=user_id)
			id = applied_jobs.objects.filter(job_id=job_id).filter(user_id=user_id)
			if not id.exists():
				details=applied_jobs.objects.create(job_id=jid,user_id=uid)
				details.save()
	return redirect('/feed/')


##
# @brief This function is used to show job seeker all the jobs he has applied to.
##
def applied_job(request):
	"""
	This function helps user to see all the jobs he has applied to.
	We query both job-applied table and job-details table and perform a natural join to get the details of jobs job seeker has applied.
	"""

	user_id = str(request.user)
	# print('applied_job request.user : ',user_id)
	jobs = applied_jobs.objects.filter(user_id=user_id,is_job_approved=True).select_related('job_id', 'user_id').filter(job_id__is_job_completed=False)
	request.session['navbar']=2	
	return render(request, 'applied_jobs.html',{'jobs':jobs})


##
# @brief This function is used apply various filter to view the jobs posted.
##
def applied_job_update(request):
	"""
	This function helps user to query/view jobs and apply four filters.
	1)current_approval_awaiting_jobs
	2)past_approved_jobs
	3)past_not_responded_jobs
	4)Current_approved_jobs
	"""
	# print('applied_job_update request.user : ',request.user)
	
	if request.method == 'POST':
		user_id = str(request.user)
		# print(user_id)
		jobs={}
		# print('id : ',type(request.POST['id']),request.POST['id'])
	
		if 'current_approval_awaiting_jobs' == request.POST['id']:
			jobs = applied_jobs.objects.filter(user_id=user_id,is_job_approved=False).select_related('job_id', 'user_id').filter(job_id__is_job_completed=False)
	

		elif 'past_approved_jobs' == request.POST['id']:

			jobs = applied_jobs.objects.filter(user_id=user_id,is_job_approved=True).select_related('job_id', 'user_id').filter(job_id__is_job_completed=True)

		elif 'past_not_responded_jobs' == request.POST['id']:

			jobs = applied_jobs.objects.filter(user_id=user_id,is_job_approved=False).select_related('job_id', 'user_id').filter(job_id__is_job_completed=True)

		else :
			jobs = applied_jobs.objects.filter(user_id=user_id,is_job_approved=True).select_related('job_id', 'user_id').filter(job_id__is_job_completed=False)

 			
		# for i in jobs:
		
		request.session['navbar']=2	# print( i.user_id , i.job_id.is_job_completed , i.is_job_approved )
		return render(request, 'applied_job_update.html',{'jobs':jobs})

	return HttpResponse('<h1>undefined page reference</h1>')


##
# @brief This function lets users to delete the job he has previously applied.
##
def delete_applied_job(request):
	"""
	This function helps user to delete his previously applied jobs.
	We query applied_jobs table and delete the entry containg the current profile and job the user has selected.
	"""
	print("delete applied job !!")
	if request.method =="POST":
		print("delete applied job !!")
		user_id = str(request.user)
		job_id = request.POST['job_id']
		print('user_id : ',user_id)
		print('job_id : ',job_id)
		job_id=int(job_id)
		delt = applied_jobs.objects.filter(user_id=user_id,job_id=job_id).delete()
		jobs = applied_jobs.objects.filter(user_id = user_id)
		print('done deleted')
		request.session['navbar']=2
		return render(request, 'applied_job_update.html',{'jobs':jobs})

	return HttpResponse('<h1>undefined page reference</h1>')

##
# @brief This function lets job provider to see responses from job seekers.
##
def posted_job_response(request):
	"""
	This function helps job provider to see responses from job seeker on his posted job.
	We query the job details and Applied jobs and inner join them.
	Then we filter jobs using job id of current user.
	"""
	print('posted job resp!!!')
	user_email = str(request.user)+'@gmail.com'
	jobs = Job_details.objects.filter(job_email=user_email,is_job_completed=False)
	request.session['navbar']=3
	return render(request, 'resp_job.html',{'jobs':jobs})


##
# @brief This function lets job provider to query his posted jobs and apply filters to them.
##
def posted_job_response_update(request):
	"""
	This function helps job provider to filter and view his posted jobs:
	This filter works using a variable is_job_completed to see if the job is completed.
	"""
	print('posted_job_response_update!!!')
	if request.method == "POST":
		jobs={}
		user_email = str(request.user)+'@gmail.com'
		
		if request.POST['type'] == 'past_jobs':
			print('past_jobs!!!')
			jobs = Job_details.objects.filter(job_email=user_email,is_job_completed=True)
		else:
			print('upcomming jobs')
			jobs = Job_details.objects.filter(job_email=user_email,is_job_completed=False)
		request.session['navbar']=3
		return render(request, 'resp_job_update.html',{'jobs':jobs})

	return HttpResponse('<h1>undefined page reference</h1>')


##
# @brief This function lets job provider to see detailed info of the job seekers who have applied for the job.
##
def show_job_responses(request):
	"""
	This functions helps job provider to see detailed job seekers info.
	From Applied jobs table on the basis of job_id we get all users who has applied that particular job.
	Then using Profile table we get detailed information about each job seeker. 
	"""
	if request.method == 'POST':
		if 'job_id' in request.POST:
			job_id = int(request.POST['job_id'])

	users_apply=applied_jobs.objects.filter(job_id=job_id).select_related('job_id', 'user_id').filter()
	details_job=Job_details.objects.filter(job_id=job_id)
	detail_value=dict(details_job.values()[0])
	list_image=detail_value['image'].split(",")
	detail_value['first_image']=list_image[0]
	if(len(list_image)>1):
		detail_value['image']=list_image[1:]
	#print(detail_value)
	request.session['navbar']=3
	return render(request, 'job_resp_details.html',{'users_apply':users_apply,'detail':detail_value})


##
# @brief This function helps job provider to select one or more job seeker for his posted job.
##
def save_job_response(request):
	"""
	In this function we query apllied jobs table using user id and job_id and set is_job_approved column to be TRUE.
	"""
	if request.method == 'POST':
		job_id = int(request.POST['job_id'])
		user_id= str(request.POST['user_id'])
		print(job_id,user_id)
		details=applied_jobs.objects.get(job_id=job_id,user_id=user_id)
		details.is_job_approved=not details.is_job_approved
		
		details.save()
	return HttpResponse(status=204)


##
# @brief This function helps job provider to mark his posted job as complete.
##
def mark_complete(request):
	"""
	In this function we query Job details table using job_id and set is_job_completed column to be TRUE.
	"""

	if request.method == 'POST':
		job_id = int(request.POST['job_id'])
		details=Job_details.objects.get(job_id=job_id)
		details.is_job_completed=not details.is_job_completed
		details.save()
	return HttpResponse(status=204)

##
# @brief This function helps to calculate distance between job seeker and job location.
##
def distance(lat1, lon1, lat2, lon2):
	""""
	This function will calculate the distance between two points job seeker(lat1,lon1) & job location(lat2,lon2)
	"""
	##
	# @param lat1  Job-seeker Latitude
	# @param lon1  Job-seeker Longitude
	# @param lat2  Job-location Latitude
	# @param lon2  Job-location Longitude
	##

	p = pi/180
	a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
	return 12742 * asin(sqrt(a))


##
# @brief This function helps to sort job details table on basis distance between job seeker and job location.
##
def get_sorted_job_details(details,lat,lon):
	"""
		Returns the job details queryset in sorted order by distance
	"""
	##
	# @param lat  Job-seeker Latitude
	# @param lon  Job-seeker Longitude
	##

	for i in details:
		i.job_distance = distance( i.job_latitude, i.job_longitude,lat,lon)
		# print("dist : ",i.job_distance)

	return sorted(details, key=operator.attrgetter('job_distance'))

##
# @brief This function helps to fetch current location of job seeker.
##
def current_location(request):
	"""
	We  are reuesting job seeker's location, if the location isn't already available in request.session
	"""
	if 'lat' in request.session:
		return redirect('/feed/')
		
	else:
		return render(request, 'current_location.html')




	# 	keys_data=data.keys()
	# 	skills_dict=["skill_Carpenter","skill_Plumbing","skill_Driver","skill_House Cleaner","skill_Dog Walker","skill_Washer"]
	# 	skills_present=[]
	# 	for i in skills_dict:
	# 		if i in keys_data:
	# 			skills_present.append(i)
	# 	job_desc=data['description']
	# 	user_id=str(request.user)
	# 	name="".join(data['name'])
	# 	email_id=str(request.user)+"@gmail.com"
	# 	photo="".join(data['photo'])
	# 	mobile="".join(data['mobile'])
	# 	aadhar="".join(data['aadhar'])
	# 	opt="".join(data['opt'])

	# 	str_skills=",".join(skills_present)
	# 	details=Profile_details.objects.create(user_id=user_id,
	# 		                                   name=name,
	# 		                                   email=email_id,
	# 		                                   image=photo,
	# 		                                   phone_no=mobile,
	# 		                                   aadhar_no=aadhar,
	# 		                                   profile_type=opt,
	# 		                                   skills=str_skills)
	# 	details.save()
	# return redirect('/feed/')


	# job_desc = models.TextField(blank=False, null=True)
 #    job_email = models.EmailField(null=True)
 #    phone_no = models.TextField(max_length=10,null=True)
 #    job_price = models.IntegerField(null=True)
 #    job_time = models.TimeField(auto_now=True)
 #    job_date=  models.DateField(auto_now=True)
 #    job_latitude=models.FloatField(null=True)
 #    job_address = models.TextField(blank=False, null=True)
 #    job_longitude=models.FloatField(null=True)
 #    job_skill= models.TextField(blank=False, null=True)





	
	
