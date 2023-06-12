from django.contrib import admin
from .models import OnOff,BreakEvent
# Register your models here.
admin.site.register(OnOff)
admin.site.register(BreakEvent)