from django.contrib import admin
from map.models import UserProfileInfo , Parameters , SIR


admin.site.register(UserProfileInfo)
# Register your models here.
admin.site.register(Parameters)

admin.site.register(SIR)

