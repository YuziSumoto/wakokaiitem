#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

from MstBuppin import *
import datetime

class MainHandler(webapp2.RequestHandler):

  def get(self):

    template_values = {'Msg': ""
                      }
    path = os.path.join(os.path.dirname(__file__), "item9051.html")
    self.response.out.write(template.render(path, template_values))

  def post(self):

    Msg = MstBuppin().CSVGet(self.request.get('file'))

    self.redirect("/item9050/") #
    return
  
app = webapp2.WSGIApplication([
    ('/item9051/', MainHandler)
], debug=True)
