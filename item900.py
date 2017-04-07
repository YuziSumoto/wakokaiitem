#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

from DatHizuke import *   # 発注日マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = { 'LblMsg': ""
                       ,'Snap':DatHizuke().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item900.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    if self.request.get('BtnAdd')  != '': # 追加ボタン
      Hizuke = self.request.get('Hizuke').replace("-","/") # 入力値受取
      Rec = DatHizuke()
      Rec.Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      DatHizuke().AddRec(Rec)
      LblMsg = "追加完了"
    for param in self.request.arguments(): 
      if "BtnDel" in param:  # 明細削除
        Hizuke = param.replace("BtnDel","")  # 文字列取得
        Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d') # 日付型変換
        DatHizuke().Delete(Hizuke)
        Rec = {} 
        LblMsg = "削除完了"

    template_values = { 'LblMsg': LblMsg
                       ,'Snap':DatHizuke().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item900.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item900/', MainHandler)
], debug=True)
