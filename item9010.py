#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
#from MstUser   import *   # 使用者マスタ
from MstBumon   import *   # 部門マスタ

class MainHandler(webapp2.RequestHandler):

  def get(self):  # 初期表示

    if self.request.get('Code',"") != "": # 選択ボタン押下時
      Rec = MstBumon().GetRec(self.request.get('Code'))
    else:
      Rec = MstBumon()
    if self.request.get('Del',"") != "": # 選択ボタン押下時
      Rec = MstBumon().Delete(self.request.get('Del'))

    template_values = { 'LblMsg': ""
                       ,'Snap'  :MstBumon().GetAll()
                       ,'Rec'   :Rec
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9010.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # 更新ボタン押下時

    LblMsg = ""
    Code   = self.request.get('Code') # 入力値受取
    Name   = self.request.get('Name') # 入力値受取
#    SortNo = self.request.get('SortNo') # 入力値受取

    Rec = MstBumon()
    Rec.Code   = int(Code)
    Rec.Name   = Name
#    Rec.SortNo = int(SortNo)
    Rec.AddRec(Rec)

    self.redirect("/item9010/") #
    return

app = webapp2.WSGIApplication([
    ('/item9010/', MainHandler)
], debug=True)
