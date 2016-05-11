from django.contrib import admin

# Register your models here.
from .models import myUser,PastContest,UpcomingContest,OngoingContest,Skill
admin.site.register(myUser)
admin.site.register(PastContest)
admin.site.register(UpcomingContest)
admin.site.register(OngoingContest)
admin.site.register(Skill)
