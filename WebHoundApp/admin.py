from django.contrib import admin

from .models import Counter, Trace

# Register your models here.
admin.site.register(Counter)
admin.site.register(Trace)