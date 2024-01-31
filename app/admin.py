from django.contrib import admin
from .models import Facility, Refinery, Agriplot,  Mill, Tracetomill, Tracetoplantation, TestAgriplot

# Register your models here.
admin.site.register(Facility)
admin.site.register(Refinery)
admin.site.register(Mill)
admin.site.register(Agriplot)
admin.site.register(TestAgriplot)
admin.site.register(Tracetomill)
admin.site.register(Tracetoplantation)
