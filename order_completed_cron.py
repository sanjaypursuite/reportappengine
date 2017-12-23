#!/usr/bin/python
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')
query = '(SELECT u.company company, u.phone phone,u.email email, u.name name, u.firstname firstname, o.po_id PO_ID, o.user_id user_id, o.buyer_name buyer_name,o.original_timestamp orignal_timestamp, o.po_date po_date ,o.amount_left po_amount_left, o.amount_paid po_amount_paid, (o.amount_left + o.amount_paid) as total_po_amount,o.order_id order_id FROM `indigo-lotus-154020.nodejs.users` u inner join `indigo-lotus-154020.nodejs.order_completed` o on u.id = o.user_id)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('order_completed')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"
