import json
import logging
import os
import pickle
import urllib2
import webapp2

from google.appengine.ext.webapp import template


from eslib import basehandler
from contrib import oauth
from urlparse import urlparse, parse_qs

from config import config

class TwitterHandler( basehandler.BaseHandler ):

    def get( self ):


        application_key = config['twitter_application_key']
        application_secret = config['twitter_application_secret']

        twitter_user_info = None
        if ( 'twitter_user_info' in self.session ):
            twitter_user_info = self.session['twitter_user_info']
        twitter_secret = ''
        twitter_token = ''
        twitter_username = ''
        twitter_auth_token = ''
        twitter_auth_verifier = ''

        if twitter_user_info is not None:
            twitter_secret = twitter_user_info['secret']
            twitter_token = twitter_user_info['token']
            twitter_username = twitter_user_info['username']

        self.response.headers['Content-Type'] = 'application/json'


        api_url = self.request.get('api_url')

        urlparts = urlparse( api_url )
        endpoint = urlparts.scheme + '://' + urlparts.netloc + '/' + urlparts.path
        params = parse_qs( urlparts.query )
        for i in params:
            params[i] = params[i][0]


        callback_url = "%s/oauth/verify" % self.request.host_url
        client = oauth.TwitterClient(application_key, application_secret,
                callback_url)

        logging.info( 'token: ' + twitter_token + ' secret: ' + twitter_secret )

        result = client.make_request(url=endpoint, additional_params=params, token=twitter_token, secret=twitter_secret, protected=True)
        return self.response.out.write(result.content)


class PlusHandler( basehandler.BaseHandler ):

    def get( self ):
        googlePlusUrl = 'https://www.googleapis.com/plus/v1/activities?query=%23howardhack&key=AIzaSyB8rONLHXKSGpqB1yovS95JSyqTQqmPtuI'

        # Get the Google+ JSON.
        try:
          result = urllib2.urlopen(googlePlusUrl)
          # Parse the Google+ JSON.
          data = json.loads(result.read())
        except urllib2.URLError, e:
          handleError(e)



        output = []
        for val in data['items']:
          tmp = {}
          key = val['published']
          title = val['title']
          actor = val['actor']
          who = val['actor']['displayName']
          pic = val['actor']['image']['url'].split('sz=')[0] + 'sz=128'

          # Add to the temp key
          tmp['key'] = key
          tmp['title'] = title
          tmp['name'] = name
          tmp['picUrl'] = pic
          output.append(tmp)
        return json.dump({output})



app = webapp2.WSGIApplication(
        [
            ('/api/twitter/get', TwitterHandler),
            ('/api/plus/get', PlusHandler)
        ],
        debug=True,
        config=config['handlerconfig']
    )
