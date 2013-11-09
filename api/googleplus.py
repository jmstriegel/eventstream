import os
import pickle
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import logging

from eslib import basehandler
from contrib import oauth
from urlparse import urlparse, parse_qs
from urllib import urlencode, quote

from config import config

class SearchHandler( basehandler.BaseHandler ):

    def get( self ):


        self.response.headers['Content-Type'] = 'application/json'



        api_key = config['google_api_key']
        search_term = self.request.get('q')
        logging.info( 'search term: ' + search_term )
        api_url = "https://www.googleapis.com/plus/v1/activities?maxResults=10&orderBy=recent&query=%s&key=%s" % (quote(search_term),quote(api_key))


        result = self.get_request( url=api_url ).get_result();
        logging.info( result )
        data = json.loads(result.read())
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

        return self.response.out.write(json.dump({output}))


    def get_request(self, url, method=urlfetch.GET, headers={}):

        rpc = urlfetch.create_rpc(deadline=10.0)
        urlfetch.make_fetch_call(rpc, url, method=method, headers=headers)
        return rpc


app = webapp2.WSGIApplication(
        [
            ('/api/googleplus/search', SearchHandler)
        ],
        debug=True,
        config=config['handlerconfig']
    )
