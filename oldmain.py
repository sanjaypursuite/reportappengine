import json
import os

import googleapiclient.discovery
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import webapp2
PROJECTID = 'indigo-lotus-154020'
client = googleapiclient.discovery.build('bigquery', 'v2')
class MainPage(webapp2.RequestHandler):
	def get(self):
	#	client = bigquery.Client('indigo-lotus-154020')
		query = '(SELECT *FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY tb1.user_id ORDER BY tb1.timestamp DESC) AS RowNo FROM `indigo-lotus-154020.nodejs.login` tb1) x WHERE x.RowNo = 1)'
		job_config = bigquery.QueryJobConfig()
		job_config.allow_large_results = True
		dest_dataset_ref = client.dataset('report')
		dest_table_ref = dest_dataset_ref.table('login_temp')
		job_config.destination = dest_table_ref
		# Allow the results table to be overwritten.
		job_config.write_disposition = 'WRITE_TRUNCATE'
		query_job = client.query(query, job_config=job_config)
		res = query_job.result()

		self.response.headers['Content-Type'] = 'text/plain'
	        self.response.write('Hello, Bro!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

