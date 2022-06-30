from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Country)
admin.site.register(RaceResult)
admin.site.register(BetResult)
