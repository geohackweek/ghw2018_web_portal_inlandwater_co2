from django.shortcuts import render
import json
from django.http import HttpResponse
from django.db import connection

def return_all_samples():
	with connection.cursor() as cursor:
		query = """
select
	(select row_to_json(_) from (select site_location_id, bar.site_description, to_json(array_agg(samples_by_type)) as samples) as _) as properties,
	st_asGeoJson(sl.point) as feature
from (
	select
		site_location_id,
		sl.site_description,
		(select row_to_json(_) from (select sample_type, to_json(array_agg(observations)) as samples) as _) as samples_by_type
	from (
		select
			site_location_id,
			sample_type,
			(select row_to_json(_) from (select date, measurement) as _) as observations
		from
			co2data_sample
		group by
			site_location_id,
			sample_type,
			date,
			measurement
		order by
			site_location_id,
			sample_type
	) foo
	left join co2data_sitelocation sl on foo.site_location_id = sl.id
	group by
		site_location_id,
		site_description,
		sample_type
) bar
left join co2data_sitelocation sl on bar.site_location_id = sl.id
group by
	bar.site_location_id,
	bar.site_description,
	sl.point
 ;
"""
		cursor.execute(query, connection)
		row = cursor.fetchall()
	return row

# Create your views here.
def data(request):

	some_data_to_dump = {
		'some_var_1': 'foo',
		'some_var_2': 'bar',
	}


	results = return_all_samples()

	data = json.dumps(results, indent=4, separators=(',', ': '))
	return HttpResponse(data, content_type='application/json')
