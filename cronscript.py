#!/usr/bin/python

import sys    
#sys.path.insert(1, '/google/google-cloud-sdk/platform/google_appengine')
#sys.path.insert(1, '/google/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
#sys.path.insert(1, 'lib')


import google
print google.__path__
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')
query = '(SELECT *FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY tb1.user_id ORDER BY tb1.timestamp DESC) AS RowNo FROM `indigo-lotus-154020.nodejs.login` tb1) x WHERE x.RowNo = 1)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('login_unique')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"
