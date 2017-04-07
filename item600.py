#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
from DatHizuke   import *   # 発注日データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = {
                        'Snap'  : DatHizuke().GetAll(),
                        'LblMsg': ""}
    path = os.path.join(os.path.dirname(__file__), 'item600.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = "aaa"
    for param in self.request.arguments(): 
      if "BtnSime" in param:  # 明細選択
        Hizuke = param.replace("BtnSime","")
        Rec = DatHizuke()
        Rec.Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
        Rec.SimeNitizi = datetime.datetime.now() + datetime.timedelta(hours=9) 
        DatHizuke().AddRec(Rec)
        LblMsg = "締め完了しました。"
    LblMsg = "印刷しました。"

    template_values = {
                        'Snap'  : DatHizuke().GetAll(),
                        'LblMsg': LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item600.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item600/', MainHandler)
], debug=True)
