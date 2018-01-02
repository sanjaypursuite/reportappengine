#!/usr/bin/python

#Dispatch REPORT order_dispatch cron
import google
print google.__path__
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')
query = '(SELECT *FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY tb1.DO_ID ORDER BY tb1.date_updated DESC) AS RowNo FROM `indigo-lotus-154020.nodejs.order_dispatch` tb1) x WHERE x.RowNo = 1)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('order_dispatch_source')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"
