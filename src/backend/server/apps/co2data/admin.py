from django.contrib import admin
from apps.co2data.models import (SiteDescription,
								 SiteLocation,
								 Sample
								)
# Register your models here.

admin.site.register(SiteDescription)
admin.site.register(SiteLocation)
admin.site.register(Sample)
