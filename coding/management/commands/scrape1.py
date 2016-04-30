
sys.path.append("C:\CodingCalendar")
os.environ["DJANGO_SETTINGS_MODULE"] = "CodingCalendar.settings"
django.setup()

import requests
from bs4 import BeautifulSoup
from time import strptime,strftime,mktime,gmtime,localtime
from urllib2 import urlopen,Request
import json


from django.core.management.base import BaseCommand, CommandError
from coding.models import UpcomingContest
from django.conf import settings

posts= {"ongoing":[] , "upcoming":[]}
hackerrank_contests = {"urls":[]}

class Command(BaseCommand):
    help = 'Scrape all the competition Data'
    args = 'Arguments is not needed'

    def handle(self, *args, **options):
        final()

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans+=str(days)+" day "
    elif days!=0: ans+=str(days)+" days "
    if hours!=0:ans+=str(hours)+"h "
    if minutes!=0:ans+=str(minutes)+"m"
    return ans.strip()

def fetch_codechef():
    page = urlopen("http://www.codechef.com/contests")
    soup = BeautifulSoup(page,"html.parser")

    statusdiv = soup.findAll("div",attrs = {"class":"table-questions"})
    upcoming_contests = statusdiv[1].findAll("tr")
    if(len(upcoming_contests) <100):
        for upcoming_contest in upcoming_contests[1:]:
            details = upcoming_contest.findAll("td")
            start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })

        ongoing_contests = statusdiv[0].findAll("tr")
        for ongoing_contest in ongoing_contests[1:]:
            details = ongoing_contest.findAll("td")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            posts["ongoing"].append({ "Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time) ,"Platform":"CODECHEF"})
    else:
        upcoming_contests = statusdiv[0].findAll("tr")
        for upcoming_contest in upcoming_contests[1:]:
            details = upcoming_contest.findAll("td")
            start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })

def fetch_hackerearth():
    cur_time = localtime()
    ref_date =  strftime("%Y-%m-%d",  localtime(mktime(localtime())   - 432000))
    duplicate_check=[]

    page = urlopen("https://www.hackerearth.com/chrome-extension/events/")
    data = json.load(page)["response"]
    for item in data:
        start_time = strptime(item["start_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        end_time = strptime(item["end_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
        duplicate_check.append(item["title"].strip())
        
        if item["challenge_type"]=='hiring':challenge_type = 'hiring'
        else: challenge_type = 'contest'

        if item["status"].strip()=="UPCOMING":
            posts["upcoming"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration,"Platform":"HACKEREARTH"})
        elif item["status"].strip()=="ONGOING":
            posts["ongoing"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Platform":"HACKEREARTH"})
    

def fetch_codeforces():
    page = urlopen("http://codeforces.com/api/contest.list")
    data = json.load(page)["result"]
    for item in data:
        
        if item["phase"]=="FINISHED": break
        
        start_time = strftime("%a, %d %b %Y %H:%M",gmtime(item["startTimeSeconds"]+19800))
        end_time   = strftime("%a, %d %b %Y %H:%M",gmtime(item["durationSeconds"]+item["startTimeSeconds"]+19800))
        duration = get_duration( item["durationSeconds"]/60 )
        
        if item["phase"].strip()=="BEFORE":  
            posts["upcoming"].append({ "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"]) , "StartTime" :  start_time,"EndTime" : end_time,"Duration":duration,"Platform":"CODEFORCES"  })
        else:
            posts["ongoing"].append({  "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"])  , "EndTime"   : end_time  ,"Platform":"CODEFORCES"  })

def fetch_topcoder():
    try:
        page = urlopen("https://clients6.google.com/calendar/v3/calendars/appirio.com_bhga3musitat85mhdrng9035jg@group.calendar.google.com/events?calendarId=appirio.com_bhga3musitat85mhdrng9035jg%40group.calendar.google.com&singleEvents=true&timeZone=Asia%2FCalcutta&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2015-04-26T00%3A00%3A00-04%3A00&timeMax=2016-06-07T00%3A00%3A00-04%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs",timeout=15)
        data = json.load(page)["items"]
        cur_time = localtime()
        for item in data:
            if(item["start"].has_key("date")):
                continue
                start_time = strptime(item["start"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
                start_time_indian = strftime("%a, %d %b %Y %H:%M",start_time)
                end_time = strptime(item["end"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
                end_time_indian = strftime("%a, %d %b %Y %H:%M",end_time)

                duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
                name = item["summary"]
                if "SRM" in name and "description" in item: 
                    url = "http://community.topcoder.com/tc?module=MatchDetails&rd="+ item["description"][110:115]
                else :            
                    url = "http://tco15.topcoder.com/algorithm/rules/"
                
                if cur_time<start_time:
                    posts["upcoming"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Duration":duration, "StartTime" :  start_time_indian,"Platform":"TOPCODER"  })
                elif cur_time>start_time and cur_time<end_time:
                    posts["ongoing"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Platform":"TOPCODER"  })
                    
    except Exception, e:
        pass
    
def fetch_hackerrank_general():
    cur_time = str(int(mktime(localtime())*1000))
    page = urlopen("https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=10&contest_slug=active&_="+cur_time)
    data = json.load(page)["models"]
    for item in data:
        if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
            start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            if not item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
            elif   item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })

def fetch_hackerrank_college():
    cur_time = str(int(mktime(localtime())*1000))
    page = urlopen("https://www.hackerrank.com/rest/contests/college?offset=0&limit=50&_="+cur_time)
    data = json.load(page)["models"]
    for item in data:
        if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
            start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            if not item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
            elif   item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })

def final():
    fetch_codechef()
    fetch_codeforces()
    fetch_hackerearth()
    fetch_topcoder()
    fetch_hackerrank_college()
    fetch_hackerrank_general()
    for key,value in posts.iteritems():
        if key=="ongoing":
            print "ongoing wale :\n\n" 
        else:
            print "upcoming wale :\n\n"
            for i in value:
                print "type"
                print type(i)
                platform = i['Platform']
                url = i['url']
                start_time = i['StartTime']
                end_time = i['EndTime']
                duration = i['Duration']
                name = i['Name']
                upcoming_contest = UpcomingContest(platform=platform,
                url=url, start_time=start_time, end_time=end_time,name = name,duration=duration)
                upcoming_contest.save()            