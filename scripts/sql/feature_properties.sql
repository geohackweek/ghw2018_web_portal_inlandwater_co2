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
