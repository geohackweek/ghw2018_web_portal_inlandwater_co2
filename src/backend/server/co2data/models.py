from django.contrib.gis.db import models

class CO2(models.Model):
	sample_date = models.DateField()
	site = models.CharField(max_length=200)
	latitude = models.FloatField()
	longitude = models.FloatField()
	# GeoDjango-specific: a geometry field (PointField)
	point = models.PointField()

	def __str__(self):
		return (self.sample_date, self.point)
