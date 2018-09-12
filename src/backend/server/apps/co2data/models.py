from django.contrib.gis.db import models

class SiteDescriptions(models.Model):
	"""describes the site_types of a location"""
	id = models.IntegerField(primary_key=True)
	site = models.CharField(max_length=200)

	def __str__(self):
		return self.site


class SiteLocations(models.Model):
	"""the locations of samples represented as a point geometry"""
	id = models.IntegerField(primary_key=True)
	site_description = models.ForeignKey(
		SiteDescriptions,
		on_delete=models.PROTECT
	)
	latitude = models.FloatField(default=0.00)
	longitude = models.FloatField(default=0.00)
	altitude = models.IntegerField(null=False)

	# GeoDjango-specific: a geometry field (PointField)
	point = models.PointField()
	def __str__(self):
		return '-'.join((self.site_description, f'{self.point.x}, {self.point.y}'))

#eventual implementation of the sampletypes and units of measure
# class SampleType(object):
# 	"""Greenhouse Gas Concentration"""
#
# 	greenhouse_gas = model.CharField(max_length=25)
#
# class Unit(object):
# 	"""Unit of measure for a Sample Type"""
#
# 	unit = model.CharField(max_length=25)

class Samples(models.Model):
	"""Date and Location of Sample."""
	id = models.IntegerField(primary_key=True)
	date = models.DateTimeField()
	site_location = models.ForeignKey(
		SiteLocations,
		on_delete=models.PROTECT
	)
	#eventual implementation of the sampletypes and units of measure
	# sample_type = models.ForeignKey(
	# 	'SampleType',
	# on_delete=models.PROTECT
	# )
	# unit = models.ForeignKey(
	# 	'Unit',
	# on_delete=models.PROTECT
	# )
	sample_type = models.CharField(max_length=25)
	unit = models.CharField(max_length=25)
	measurement = models.FloatField()
