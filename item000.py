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

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    RecHizuke = DatHizuke().GetNext(datetime.datetime.now()) # 今日以降の未閉め発注日
    if RecHizuke == {}:
      LblMsg = u"次回発注日は未定です。" 
    else:
      LblMsg = u"次回発注日は" + RecHizuke.Hizuke.strftime('%Y/%m/%d') + u"です。" 
 
    template_values = { "MstBusyo" : MstBusyo().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item000.html')
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
    path = os.path.join(os.path.dirname(__file__), 'item000.html')
    self.response.out.write(template.render(path, template_values))
    return

app = webapp2.WSGIApplication([
    ('/item000/', MainHandler),
    ('/', MainHandler)
], debug=True)
