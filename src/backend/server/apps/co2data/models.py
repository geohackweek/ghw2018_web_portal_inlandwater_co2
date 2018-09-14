from django.contrib.gis.db import models

# class SiteDescription(models.Model):
# 	"""describes the site_types of a location"""
# 	id = models.AutoField(primary_key=True)
# 	site = models.CharField(max_length=200)
#
# 	def __str__(self):
# 		return self.site


class SiteLocation(models.Model):
	"""the locations of samples represented as a point geometry"""
	id = models.AutoField(primary_key=True)
	# to be implemented later
	# site_description = models.ForeignKey(
	# 	SiteDescription,
	# 	on_delete=models.PROTECT
	# )
	site_description = models.CharField(max_length=150, null=True)
	latitude = models.FloatField(default=0.00, null=True)
	longitude = models.FloatField(default=0.00, null=True)
	altitude = models.FloatField(null=True)

	# GeoDjango-specific: a geometry field (PointField)
	point = models.PointField()
	def __str__(self):
		return '-'.join((f'{self.point.x}, {self.point.y}'))

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

class Sample(models.Model):
	"""Date and Location of Sample."""
	id = models.AutoField(primary_key=True)
	date = models.CharField(max_length=25, null=True)
	site_location = models.ForeignKey(
		SiteLocation,
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
	sample_type = models.CharField(max_length=25, null=True)
	unit = models.CharField(max_length=25, null=True)
	measurement = models.FloatField(null=True)
