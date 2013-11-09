import os
import pickle
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from webapp2_extras import sessions
from contrib import oauth 

from eslib import basehandler
from config import config


class MainHandler( basehandler.BaseHandler ):

    def get( self, mode ):


        application_key = config['twitter_application_key']
        application_secret = config['twitter_application_secret']


        callback_url = "%s/oauth/verify" % self.request.host_url
        client = oauth.TwitterClient(application_key, application_secret, 
                callback_url)
        if mode == "login":
              return self.redirect(client.get_authorization_url())
        if mode == "verify":
              auth_token = self.request.get("oauth_token")
              auth_verifier = self.request.get("oauth_verifier")
              user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
              self.session['twitter_user_info'] = user_info
              self.session['twitter_auth_token'] = auth_token
              self.session['twitter_auth_verifier'] = auth_verifier
              return self.redirect( '%s/oauth/' % self.request.host_url )
        if mode == "logout":
              return self.redirect(client.get_logout_url())

        self.response.headers['Content-Type'] = 'text/html'
        
        twitter_user_info = None
        if ( 'twitter_user_info' in self.session ):
            twitter_user_info = self.session['twitter_user_info']
        twitter_secret = ''
        twitter_token = ''
        twitter_username = ''

        if twitter_user_info is not None:
            twitter_secret = twitter_user_info['secret']
            twitter_token = twitter_user_info['token']
            twitter_username = twitter_user_info['username']

        tmpl = os.path.join( os.path.dirname(__file__), 'templates/auth.html' )
        self.response.out.write( twitter_user_info )
        tmplvars = {
            'twitter_username': twitter_username,
            'twitter_user_info': str(twitter_user_info),
            'twitter_secret': twitter_secret,
            'twitter_token': twitter_token
        }

        self.response.out.write( template.render( tmpl, tmplvars ) )



app = webapp2.WSGIApplication( 
        [
            ('/oauth/(.*)', MainHandler)
        ], 
        debug=True,
        config=config['handlerconfig']
    )
