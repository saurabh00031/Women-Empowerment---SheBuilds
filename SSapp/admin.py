from django.contrib import admin
from .models import *

admin.site.register([Usrinfo,Mentorinfo,Blog_Post,Comment])
admin.site.register(SchollershipList)
admin.site.register(WommenRights)
