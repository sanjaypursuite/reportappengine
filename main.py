import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Reporting!')
        
    def AsyncQuery(self, select_query, billing_projectId, dataset_projectId, datasetId, destination_tableId):
       query_request = self.bigquery_service.jobs()
       query_config = {
          'jobReference': {
      'projectId': 'indigo-lotus-154020',
      'jobId': str(uuid.uuid4())
       },
      'configuration': {
      'query':  {
        'query': 'SELECT *FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY tb1.user_id ORDER BY tb1.timestamp DESC) AS RowNo FROM [indigo-lotus-154020.nodejs.login] tb1) x WHERE x.RowNo = 1',
        'priority': 'BATCH',
        'useLegacySql': 'false',
        'writeDisposition': 'WRITE_TRUNCATE',
        'destinationTable': {
        'datasetId': 'indigo-lotus-154020.report',
        'projectId': 'indigo-lotus-154020',
        'tableId': 'login_digest'
                    }
              }
          }
   }

   query_response = query_request.insert(
       projectId='indigo-lotus-154020', 
       body=query_config).
       execute() 

   return query_response



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
