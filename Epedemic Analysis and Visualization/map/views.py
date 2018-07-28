from django.shortcuts import render
from map.forms import UserForm, UserProfileInfoForm , ParameterForm
from django.core .urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate , login , logout
from map.models import Parameters , SIR
import json
import random
import numpy as np
from bisect import bisect_left
from bisect import bisect_right
import math
from collections import deque
import os




def index(request):
	return render(request,'map/index.html')




def register(request):

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileInfoForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid() :

			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user 

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']


			profile.save()

			registered = True

		else:
			print(user_form.errors , profile_form.errors)
	else:

		user_form = UserForm()
		profile_form = UserProfileInfoForm()


	return render(request,'map/registeration.html', {'user_form':user_form,'profile_form':profile_form,'registered' : registered})




@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("map:index"))			



@login_required
def special(request):
	return HttpResponse("Hey Bro special !")



def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username , password = password)

		if user :
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse("map:eav"))			
			else:
				return HttpResponse("User is not Active")
		else:
			return HttpResponse("User Login Failed !")
	else:
		return render(request,'map/login.html')



def eav(request):
	context = {"SIR" : SIR.objects.all() , "range" : range(10)}

	return render(request,'map/eav.html',context)


# =============== parameter_view ====================


def para_view(request):

	if request.method == 'POST':

		para_form = ParameterForm(request.POST , request.FILES)

		if para_form.is_valid():

			para_form.save()
			printfun()
			return HttpResponseRedirect(reverse("map:eav"))				

	else:

		para_form = ParameterForm()

	return render(request,'map/parameter.html', {'para_form':para_form})




def remove(arr1,arr2):
    for i in range(len(arr1)):
        arr2=np.delete(arr2,arr1[i]-i)
    return arr2


# In[9]:

def include(susceptable_pop_lat,susceptable_pop_lng ,inf,rinf):
    for values in rinf:
        inf.append([susceptable_pop_lat[values][0],susceptable_pop_lng[values][0]])
    return inf


# In[10]:

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


# In[11]:

def increment_date(dd,mm,yy):
    dd+=1
    if dd>30:
        mm+=1
        dd=1
    if mm>12:
        mm=1
        yy+=1
    return dd,mm,yy
    



def printfun():

	p = Parameters.objects.all()

	json_file = json.loads(p[0].upload_file.read())

	mainlist=[]
	for lines in json_file:   
	    mainlist.append([lines["lat"],lines["lng"]])
	
	mainlist.sort(key=lambda x:x[0])


	#=============================== Redundent data removal =================================
	i=0
	deleted=0
	while i<len(mainlist):
	    if mainlist[i-1]==mainlist[i]:
	        mainlist.remove(mainlist[i])
	        deleted+=1
	    else:
	        i+=1

	#print(len(mainlist))

	longitude=[]
	latitude=[]
	for i in range(len(mainlist)):
	    latitude.append(mainlist[i][0])
	    longitude.append(mainlist[i][1])

	#print(len(longitude))


	# # initialising the data

	# In[3]:


	susceptable_pop_lat=np.array(latitude)   #np.random.randint(1,100,(10000))
	susceptable_pop_lng=np.array(longitude)    #np.random.randint(1,100,(10000))

	threshold=0.1
	initiallyinfected=np.random.randint(0,len(json_file)-1,size=(2,1))
	infected=deque()
	recovered=[]
	counter=deque()

	mpd=0


	# In[4]:

	# # initialising the date

	# In[5]:


	dd=1
	mm=1
	yy=2015


	# In[6]:


	recover=5


	# In[7]:


	initiallyinfected=np.sort(initiallyinfected,axis=0)

	infected=include(susceptable_pop_lat,susceptable_pop_lng,infected,initiallyinfected)
	susceptable_pop_lat=np.delete(susceptable_pop_lat,initiallyinfected)
	susceptable_pop_lng=np.delete(susceptable_pop_lng,initiallyinfected)
	counter+=[0]*len(infected)



	# In[13]:



	for i in range(len(infected)):
	    valued='{\ncounter: 0 ,\n'
	    date='date : '+str([yy,mm,dd])+',\n'
	    coords='coords : '+str([infected[i][0],infected[i][1]])+'\n}\n'
	    data=valued+date+coords
	    s = SIR()
	    s.lat = infected[i][0]
	    s.lng = infected[i][1]
	    s.counter = 0
	    s.date = str(yy)+"-"+str(mm)+"-"+str(dd)
	    s.save()

	while len(infected)>0:
	    
	    dd,mm,yy=increment_date(dd,mm,yy)
	    
	    recent_infection=[]
	    for i in range(len(infected)):
	        
	        for j in range(len(susceptable_pop_lat)):
	            
	            dist=distance(infected[i],[susceptable_pop_lat[j],susceptable_pop_lng[j]])
	            
	            if dist<=threshold:
	                
	                probablity=np.random.random()
	                
	                if probablity>0.5:
	                    recent_infection.append(j)
	                    
	    recent_infection=list(set(recent_infection))
	    counter=deque([val+1 for val in counter])
	    counter=counter+deque([0]*len(recent_infection))
	    
	    
	    for k in range(len(recent_infection)):
	        infected.append([susceptable_pop_lat[recent_infection[k]],susceptable_pop_lng[recent_infection[k]]])
	        #entering the data of recently infected population in the file
	        valued='{\ncounter: 0 ,\n'
	        date='date : '+str([yy,mm,dd])+',\n'
	        coords='coords : '+str([susceptable_pop_lat[recent_infection[k]],susceptable_pop_lng[recent_infection[k]]])+'\n}\n'
	        data=valued+date+coords
	        s = SIR()
	        s.lat = infected[k][0]
	        s.lng = infected[k][1]
	        s.counter = 0
	        s.date = str(yy)+"-"+str(mm)+"-"+str(dd)
	        s.save()
	    
	    susceptable_pop_lat=np.delete(susceptable_pop_lat,recent_infection)
	    susceptable_pop_lng=np.delete(susceptable_pop_lng,recent_infection)
	    recovering=0
	    for l in range(len(counter)):
	        if counter[l]>=recover:
	            recovering+=1
	        else:
	            break
	    for l in range(recovering):
	        coordinates=infected.popleft()
	        valued='{\ncounter: 1 ,\n'
	        date='date : '+str([yy,mm,dd])+',\n'
	        coords='coords : '+str(coordinates)+'\n}\n'
	        data=valued+date+coords
	        s = SIR()
	        s.lat = coordinates[0]
	        s.lng = coordinates[1]        
	        s.counter = 1
	        s.date = str(yy)+"-"+str(mm)+"-"+str(dd)
	        s.save()
	        recovered.append(coordinates)
	        counter.popleft()

	    print("Total Susceptable Recent Infection  Total Infected     Total Recovered Date")
	    print(len(susceptable_pop_lat) ,len(recent_infection),len(infected),len(recovered),str([yy,mm,dd]))
	            

