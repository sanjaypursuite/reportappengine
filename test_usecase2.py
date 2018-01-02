#!/usr/bin/python

import sys    


import google
print google.__path__
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')
query = '(SELECT *FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY po_id ORDER BY PO_Update_Date DESC) AS RowNo FROM (select * from (SELECT A.*, B.emai_id, B.phone_number FROM `indigo-lotus-154020.nodejs.xyz2` A left join `indigo-lotus-154020.nodejs.user_contact_dummy` B on A.user_id = B.user_id order by B.date_updated desc) AS C) ) x WHERE x.RowNo = 1)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('xyz2_user_contact_dummy_join')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"
