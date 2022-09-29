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
 
    template_values = { 'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item9000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = ""

    if self.request.get('BtnItem100')  != '':
      RecHizuke = DatHizuke().GetNext(datetime.datetime.now()) # 今日以降の未閉め発注日
      if RecHizuke == {}:
        LblMsg = u"次回発注日は未定です。" 
      else:
        Parm = "?BusyoCode=" + self.request.get('BusyoCD')
        self.redirect("/item100/" + Parm) #
        return

    template_values = { "MstBusyo" : MstBusyo().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0000.html')
    self.response.out.write(template.render(path, template_values))
    return

app = webapp2.WSGIApplication([
    ('/item9000/', MainHandler)
], debug=True)
