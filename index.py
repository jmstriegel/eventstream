import os
import pickle
import webapp2
from google.appengine.ext.webapp import template

from eslib import basehandler
from config import config

class MainHandler( basehandler.BaseHandler ):

    def get( self ):
        self.response.headers['Content-Type'] = 'text/html'
        
        tmpl = os.path.join( os.path.dirname(__file__), 'templates/index.html' )


        tmplvars = {
            'title': config['title'],
            'heading_text': config['heading_text'],
            'search_term': config['search_term'],

        }
        self.response.out.write( template.render( tmpl, tmplvars ) )


app = webapp2.WSGIApplication( 
        [
            ('/', MainHandler)
        ], 
        debug=True,
        config=config['handlerconfig']
    )
