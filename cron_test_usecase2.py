#!/usr/bin/python

import sys    


import google
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')
query = '(SELECT *FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY po_id ORDER BY po_updated_date DESC) AS RowNo FROM (select * from (SELECT A.po_id,A.buyer_company_name,A.delivery_state, A.po_amount, A.po_updated_date, B.seller_company_name, B.managed_type, B.operating_company, B.property_category FROM `indigo-lotus-154020.nodejs.po_updated_report_data` A left join `indigo-lotus-154020.nodejs.po_product_updated_report_data` B on A.po_id = B.po_id order by A.po_updated_date desc) AS C) ) x WHERE x.RowNo = 1)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('PO_Data_etl')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"
