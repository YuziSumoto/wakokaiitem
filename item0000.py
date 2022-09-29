#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime

from MstBusyo   import *   # 部署マスタ
from DatHizuke  import *   # 発注日マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    LblMsg = ""
 
    Busyo = int(self.request.cookies.get('Busyo', '3'))

    template_values = { 'Busyo'    : Busyo,
                        'MstBusyo' : MstBusyo().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = ""

    Busyo = int(self.request.get('BusyoCD',"0"))

    if self.request.get('BtnSeikyu')  != '':
      Parm = "?BusyoCode=" + Busyo
      self.redirect("/item100/" + Parm)
      return

    template_values = { 'Busyo'    : Busyo,
                        'MstBusyo' : MstBusyo().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0000.html')

    self.response.headers.add_header('Set-Cookie', 'Busyo=%s;' % str(Busyo))
    self.response.out.write(template.render(path, template_values))

    return

app = webapp2.WSGIApplication([
    ('/item0000/', MainHandler)
], debug=True)
