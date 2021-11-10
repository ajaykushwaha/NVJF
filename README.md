----------------CS699 Project------------------
Phantom Troupe

Nearest Vocational Job Finder(NVJF)

Ajay Sarup Jain -  203050036
Mahendra Patel  -  203050078
Ajay Shyamsunder - 203059009
Polu Varshith -    203050099
Avijit Darshal -   203051001


Motivation

In the wake of the global pandemic, there has been a huge disturbance in the service market, both organized and unorganized. The organized sector from some time now has had many platforms (like Monster India, Indeed .etc) to publish and find stable full-time work. But such platforms are not appropriate to post nearby vocational jobs like Plumbing, Electrician, Nurs- ing aides, Carpenters etc. These jobs arise at the need of the hour and current location of the service provider as well as job location is of utmost importance. Our idea is to develop a web application which can act as a middleman for service exchange in these sectors.




Install python3 on your system
• sudo apt-get install python3.6

To install Django on ubuntu, run the following command in your terminal.
• pip3 install django

Install postgresql :
	to download the postgresql click on the below link :
	https://www.postgresql.org/download/
	after installation:
	1. create database with name NVJF with default user postgre and password="1234"(without quotes)
	2. check your port no in settings.py

• pip3 install social-auth-app-django

• pip3 install psycopg2

One needs to git clone the project. 
git clone https://(USERNAME)@git.cse.iitb.ac.in/PhantomTroupe/project_cs699.git			.......repository is private

After that open terminal in main
directory and run following commands.
• python3 manage.py makemigrations
• python3 manage.py migrate
• python3 manage.py runserver 

To access the application open the web browser and go to "localhost:8000"

All right the project is now running .Enjoy the project.

# Screenshots
## Sign in Page
![alt text](/Documentation/Screenshots/1.png)

## Make you Profile (For first time user)
![alt text](/Documentation/Screenshots/2.png)

## New Job Feed (For job seeker)
![alt text](/Documentation/Screenshots/3.png)

## New Job Feed (For both profile type)
![alt text](/Documentation/Screenshots/4.png)

## Job Details (on clicking view more button)
![alt text](/Documentation/Screenshots/5.png)

## Post a Job (Job Provider can post a job)
![alt text](/Documentation/Screenshots/6.png)

## Posted Job Response (For Job provider)
![alt text](/Documentation/Screenshots/7.png)



