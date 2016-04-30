from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from coding.models import *
import json
from django.core import serializers
import requests
from bs4 import BeautifulSoup
from time import strptime,strftime,mktime,gmtime,localtime
from urllib2 import urlopen,Request
from django.core.urlresolvers import reverse
import urllib
msg=""

posts= {"ongoing":[] , "upcoming":[]}
hackerrank_contests = {"urls":[]}
data = {}
def index(request):
	topFiveUsers = getTopFiveUsers()
	if(request.method=="GET"):
		print request.user.is_authenticated()
		message = request.GET.get('msg')
		if message is not None:
			return render(request, 'coding/index11.html',{'topFiveUsers' : topFiveUsers,"msg":message})
		else:
			return render(request, 'coding/index11.html',{'topFiveUsers' : topFiveUsers})

		# if msg=="Successfully Signed Up":
		# 	print "finally"
		# 	setString("")
		# 	return render(request, 'coding/index11.html',{'topFiveUsers' : topFiveUsers,"msg":"Successfully Signed Up"})
		# else:
		# 	print getString()
		# 	print "Gmara"
		# 	return render(request, 'coding/index11.html',{'topFiveUsers' : topFiveUsers})
	elif(request.method=="POST"):
		print request
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user is not None:
			login(request, user)
			print "user not none"
			print user.is_authenticated()
			return render(request,'coding/index11.html',{'msg':"Welcome "+user.first_name+" "+user.last_name,'topFiveUsers' : topFiveUsers})
		else:
			print "user none"
			return render(request,'coding/index11.html',{'msg':"Invalid Credentials",'topFiveUsers' : topFiveUsers})
					
def signup(request):
	if(request.method=="GET"):
		return render(request, 'coding/signup.html')	
	elif(request.method=="POST"):
		print request
		user_name = request.POST.get('username')
		first_name = request.POST.get('first')
		last_name = request.POST.get('last')
		email = request.POST.get('email')
		password = request.POST.get('password')
		cc = request.POST.get('CC')
		cf = request.POST.get('CF')
		sp = request.POST.get('SP')

		user = User.objects.filter(username=user_name).count()
		if user == 0:
			print 'yes'
			s = spojSpider(sp)
			c = codechefSpider(cc)
			usr = User.objects.create_user(email=email, username=user_name, password=password, first_name=first_name, last_name=last_name)
			
			myusr = myUser(user=usr, codechef_handle=cc, spoj_handle=sp, codeforces_handle=cf,spoj_count=s,codechef_count=c,problem_count=s+c)
			myusr.save()
			#topFiveUsers = getTopFiveUsers()
			setString("Successfully Signed Up")
			f = { 'msg' : 'Successfully Signed Up'}
			q = urllib.urlencode(f)
			return redirect('/?'+q)
			#return redirect('/',{'msg':"Successfully Signed Up",'topFiveUsers' : topFiveUsers})			
		else:
			print user
			print 'no'	
			return render(request,'coding/signup.html',{'msg':"Choose a different username"})
        
def compare(request):
    pieData = [10,20,30,40]
    return render(request,'coding/chart.html',{'pieData':pieData})      	
 
def upcomingContests(request):
	if(request.method=="GET"):
		upcoming_contests = UpcomingContest.objects.all()
		return render(request,'coding/future.html',{'upcoming_contests' : upcoming_contests})

def about(request):
    if(request.method=="GET"):
        return render(request,'coding/aboutUs.html')

def contactUs(request):
    if(request.method=="GET"):
        return render(request,'coding/contact.html') 

def tutorial(request):
    if(request.method=="GET"):
        return render(request,'coding/tuts.html')                

def leaderboard(request):
    if(request.method=="GET"):
        users = myUser.objects.all().order_by('-problem_count')        
        return render(request,'coding/leaderboard.html',{'users':users})

def log_out(request):
	logout(request)
	return redirect('/')        
# Start of Scraping code			
# def get_duration(duration):
#     days = duration/(60*24)
#     duration %= 60*24
#     hours = duration/60
#     duration %= 60
#     minutes = duration
#     ans=""
#     if days==1: ans+=str(days)+" day "
#     elif days!=0: ans+=str(days)+" days "
#     if hours!=0:ans+=str(hours)+"h "
#     if minutes!=0:ans+=str(minutes)+"m"
#     return ans.strip()

# def fetch_codechef():
#     page = urlopen("http://www.codechef.com/contests")
#     soup = BeautifulSoup(page,"html.parser")

#     statusdiv = soup.findAll("div",attrs = {"class":"table-questions"})
#     upcoming_contests = statusdiv[1].findAll("tr")
#     if(len(upcoming_contests) <100):
#         for upcoming_contest in upcoming_contests[1:]:
#             details = upcoming_contest.findAll("td")
#             start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
#             end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
#             duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#             posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })

#         ongoing_contests = statusdiv[0].findAll("tr")
#         for ongoing_contest in ongoing_contests[1:]:
#             details = ongoing_contest.findAll("td")
#             end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
#             posts["ongoing"].append({ "Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time) ,"Platform":"CODECHEF"})
#     else:
#         upcoming_contests = statusdiv[0].findAll("tr")
#         for upcoming_contest in upcoming_contests[1:]:
#             details = upcoming_contest.findAll("td")
#             start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
#             end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
#             duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#             posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })

# def fetch_hackerearth():
#     cur_time = localtime()
#     ref_date =  strftime("%Y-%m-%d",  localtime(mktime(localtime())   - 432000))
#     duplicate_check=[]

#     page = urlopen("https://www.hackerearth.com/chrome-extension/events/")
#     data = json.load(page)["response"]
#     for item in data:
#         start_time = strptime(item["start_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
#         end_time = strptime(item["end_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
#         duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#         duplicate_check.append(item["title"].strip())
        
#         if item["challenge_type"]=='hiring':challenge_type = 'hiring'
#         else: challenge_type = 'contest'

#         if item["status"].strip()=="UPCOMING":
#             posts["upcoming"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration,"Platform":"HACKEREARTH"})
#         elif item["status"].strip()=="ONGOING":
#             posts["ongoing"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Platform":"HACKEREARTH"})
    

# def fetch_codeforces():
#     page = urlopen("http://codeforces.com/api/contest.list")
#     data = json.load(page)["result"]
#     for item in data:
        
#         if item["phase"]=="FINISHED": break
        
#         start_time = strftime("%a, %d %b %Y %H:%M",gmtime(item["startTimeSeconds"]+19800))
#         end_time   = strftime("%a, %d %b %Y %H:%M",gmtime(item["durationSeconds"]+item["startTimeSeconds"]+19800))
#         duration = get_duration( item["durationSeconds"]/60 )
        
#         if item["phase"].strip()=="BEFORE":  
#             posts["upcoming"].append({ "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"]) , "StartTime" :  start_time,"EndTime" : end_time,"Duration":duration,"Platform":"CODEFORCES"  })
#         else:
#             posts["ongoing"].append({  "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"])  , "EndTime"   : end_time  ,"Platform":"CODEFORCES"  })

# def fetch_topcoder():
#     try:
#         page = urlopen("https://clients6.google.com/calendar/v3/calendars/appirio.com_bhga3musitat85mhdrng9035jg@group.calendar.google.com/events?calendarId=appirio.com_bhga3musitat85mhdrng9035jg%40group.calendar.google.com&singleEvents=true&timeZone=Asia%2FCalcutta&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2015-04-26T00%3A00%3A00-04%3A00&timeMax=2016-06-07T00%3A00%3A00-04%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs",timeout=15)
#         data = json.load(page)["items"]
#         cur_time = localtime()
#         for item in data:
# 		if(item["start"].has_key("date")):continue
		        
#                 start_time = strptime(item["start"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
#                 start_time_indian = strftime("%a, %d %b %Y %H:%M",start_time)
#                 end_time = strptime(item["end"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
#                 end_time_indian = strftime("%a, %d %b %Y %H:%M",end_time)

#                 duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#                 name = item["summary"]
#                 if "SRM" in name and "description" in item: url = "http://community.topcoder.com/tc?module=MatchDetails&rd="+ item["description"][110:115]
#                 else :            url = "http://tco15.topcoder.com/algorithm/rules/"
                
#                 if cur_time<start_time:
#                     posts["upcoming"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Duration":duration, "StartTime" :  start_time_indian,"Platform":"TOPCODER"  })
#                 elif cur_time>start_time and cur_time<end_time:
#                     posts["ongoing"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Platform":"TOPCODER"  })
                    
#     except Exception, e:
#         pass
    
# def fetch_hackerrank_general():
#     cur_time = str(int(mktime(localtime())*1000))
#     page = urlopen("https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=10&contest_slug=active&_="+cur_time)
#     data = json.load(page)["models"]
#     for item in data:
#         if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
#             start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
#             end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
#             duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#             if not item["started"]:
#                 hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
#                 posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
#             elif   item["started"]:
#                 hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
#                 posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })

# def fetch_hackerrank_college():
#     cur_time = str(int(mktime(localtime())*1000))
#     page = urlopen("https://www.hackerrank.com/rest/contests/college?offset=0&limit=50&_="+cur_time)
#     data = json.load(page)["models"]
#     for item in data:
#         if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
#             start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
#             end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
#             duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
#             if not item["started"]:
#                 hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
#                 posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
#             elif   item["started"]:
#                 hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
#                 posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })

# def final():
# 	fetch_codechef()
# 	fetch_codeforces()
# 	fetch_hackerearth()
# 	fetch_topcoder()
# 	fetch_hackerrank_college()
# 	fetch_hackerrank_general()
# 	for key,value in posts.iteritems():
# 		if key=="ongoing":
# 			print "ongoing wale :\n\n" 
# 		else:
# 			print "upcoming wale :\n\n"
# 			for i in value:
# 				print "type"
# 				print type(i)
# 				platform = i['Platform']
# 				url = i['url']
# 				start_time = i['StartTime']
# 				end_time = i['EndTime']
# 				duration = i['Duration']
# 				name = i['Name']
# 				upcoming_contest = UpcomingContest(platform=platform,
# 				url=url, start_time=start_time, end_time=end_time,name = name,duration=duration)
# 				upcoming_contest.save()
# 		# for i in value:
# 		# 	for k,v in i.iteritems():
# 		# 		print k,v

def codechefSpider(username):
	print 'codechefSpider'
	url = 'https://www.codechef.com/users/'+username
	source_code = requests.get(url)
	#print source_code
	plain_text = source_code.text
	#print plain_text
	soup = BeautifulSoup(plain_text,"html.parser")
	for divider in soup.findAll('table',{'id': 'problem_stats'}):
		#href = divider.get('data-evar48')
		#m = re.search('foo','foobar')
		#m.group()
		s = divider.findAll("tr")
		q = s[1].findAll('td')
		#print q
		score = q[0].string
		data['cc'] = score
        return int(score)
		#print score

def spojSpider(username):
	print 'spojSpider'
	url = 'http://www.spoj.com/users/'+username
	source_code = requests.get(url)
	#print source_code
	plain_text = source_code.text
	#print plain_text
	soup = BeautifulSoup(plain_text,"html.parser")
	for divider in soup.findAll('dl',{'class': 'dl-horizontal profile-info-data profile-info-data-stats'}):
		#print divider
		s = divider.findAll("dd")
		#print s
		score = s[0].string
		data['sp'] = score
        return int(score)    

def getTopFiveUsers():
	topFiveUsers = []
	numOfUsers = myUser.objects.all().count()
	if numOfUsers>=5:
		topFiveUsers = myUser.objects.all().order_by('-problem_count')[:5]
	else:
		topFiveUsers = myUser.objects.all().order_by('-problem_count')
	return topFiveUsers	

def setString(s):
	msg = s
def getString():
	return msg		




#End of Scraping code