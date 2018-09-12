from django.contrib import admin
from apps.co2data.models import (SiteDescriptions,
								 SiteLocations,
								 Samples
								)
# Register your models here.

admin.site.register(SiteDescriptions)
admin.site.register(SiteLocations)
admin.site.register(Samples)
