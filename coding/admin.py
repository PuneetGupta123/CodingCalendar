from django.contrib import admin

# Register your models here.
from .models import myUser,PastContest,UpcomingContest,OngoingContest
admin.site.register(myUser)
admin.site.register(PastContest)
admin.site.register(UpcomingContest)
admin.site.register(OngoingContest)
