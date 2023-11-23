from django.contrib import admin
from .models import Facility, Refinery, Mill, Agriplot, Tracetomill, Tracetoplantation, PlantedOutsideLandRegistration

# Register your models here.
admin.site.register(Facility)
admin.site.register(Refinery)
admin.site.register(Mill)
admin.site.register(Agriplot)
admin.site.register(Tracetomill)
admin.site.register(Tracetoplantation)
admin.site.register(PlantedOutsideLandRegistration)
