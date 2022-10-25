#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime

from MstBusyo   import *   # 部署マスタ
from MstHizuke  import *   # 発注日マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    LblMsg = ""
    
    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより

    Hizuke = datetime.datetime.now().strftime('%Y/%m/%d') # 今日

    NextDay = MstHizuke().GetNext(Hizuke,Busyo)

    if NextDay == False:
      LblMsg += u"次回発注日は未定です。"
    else:
      LblMsg += u"次回発注日は" + NextDay + u"です。"

    if NextDay != False:
      Hizuke = NextDay
    else:
      PrevDay = MstHizuke().GetPrev(Hizuke,Busyo)
      if PrevDay != False:
        Hizuke = PrevDay
      else:
        Huzuke = False

    template_values = { 'Busyo'    : int(Busyo),
                        'Hizuke'   : Hizuke,
                        'MstBusyo' : MstBusyo().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = ""

    Busyo = int(self.request.get('BusyoCD',"0"))

    self.redirect("/item0000/?Busyo=" + self.request.get('BusyoCD',"")) # 部署変更

    return

app = webapp2.WSGIApplication([
    ('/item0000/', MainHandler)
], debug=True)
