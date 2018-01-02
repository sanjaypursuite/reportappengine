#!/usr/bin/python

import sys    
#sys.path.insert(1, '/google/google-cloud-sdk/platform/google_appengine')
#sys.path.insert(1, '/google/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
#sys.path.insert(1, 'lib')


import google
print google.__path__
from google.cloud import bigquery
client = bigquery.Client('indigo-lotus-154020')

query = '(SELECT *FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY part_id ORDER BY PO_Update_Date DESC) AS RowNo FROM (select * from (SELECT A.*, B.PO_ID as part_id, B.PO_Update_Date ,B.Purchase_Type purchasetype, B.Purchase_Model purchasemodel, B.Commission_Amount, B.Commission_Amount_Pending, B.Commission_Amount_Received, B.PO_Status, B.PO_Dispatch_Status, B.Quotation_Date, B.Property_Name B_propertyname, B.Property_Type B_propertytype, B.PO_Amount, B.PO_Amount_Received, B.PO_Amount_Pending, B.Shipping_Name, B.Delivery_Pincode   FROM `indigo-lotus-154020.nodejs.company_wise_report_data` A left join `indigo-lotus-154020.nodejs.mtd_test` B on A.po_id = B.po_id ) AS C) ) x WHERE x.RowNo = 1)'
job_config = bigquery.QueryJobConfig()
job_config.allow_large_results = True
dest_dataset_ref = client.dataset('cron')
dest_table_ref = dest_dataset_ref.table('join_company_wise_report_data_and_mtd_test')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
query_job = client.query(query, job_config=job_config)
res = query_job.result()
print "Done"