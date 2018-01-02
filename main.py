import json
import os

import googleapiclient.discovery
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import webapp2


# The project id whose datasets you'd like to list
PROJECTID = 'indigo-lotus-154020'

# Create the method decorator for oauth.
decorator = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    scope='https://www.googleapis.com/auth/bigquery')

# Create the bigquery api client
service = googleapiclient.discovery.build('bigquery', 'v2')


class MainPage(webapp2.RequestHandler):

    # oauth_required ensures that the user goes through the OAuth2
    # authorization flow before reaching this handler.
    @decorator.oauth_required
    def get(self):
        # This is an httplib2.Http instance that is signed with the user's
        # credentials. This allows you to access the BigQuery API on behalf
        # of the user.
        http = decorator.http()

        response = service.datasets().list(projectId=PROJECTID).execute(http)

        self.response.out.write('<h3>Datasets.list raw response:</h3>')
        self.response.out.write('<pre>%s</pre>' %
                                json.dumps(response, sort_keys=True, indent=4,
                                           separators=(',', ': ')))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    # Create the endpoint to receive oauth flow callbacks
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
