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
from MstBumon  import *   # 部門マスタ
from MstBusyo  import *   # 部署マスタ

class MainHandler(webapp2.RequestHandler):

  def get(self):  # 初期表示

    if self.request.get('Code',"") != "": # 選択ボタン押下時
      Rec = MstBusyo().GetRec(self.request.get('Code'))
    else:
      Rec = MstBusyo()
    if self.request.get('Del',"") != "": # 選択ボタン押下時
      Rec = MstBusyo().Delete(self.request.get('Del'))

    SnapBumon = MstBumon().GetAll()
    Snap = MstBusyo().GetAll()
    for Rec2 in Snap:
      Rec2.BumonName = "未指定"
      for RecBumon in SnapBumon:
        if RecBumon.Code == Rec2.Bumon:
          Rec2.BumonName = RecBumon.Name
          break

    template_values = { 'LblMsg': ""
                       ,'SnapBumon' :SnapBumon
                       ,'Snap'      :Snap
                       ,'Rec'       :Rec
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9020.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # 更新ボタン押下時

    LblMsg = ""
    Code   = self.request.get('Code',"0") # 入力値受取
    Bumon  = self.request.get('Bumon') # 入力値受取
    Name   = self.request.get('Name') # 入力値受取
    SortNo = self.request.get('SortNo',"0") # 入力値受取

    Rec = MstBusyo()
    Rec.Code   = int(Code)
    Rec.Bumon  = int(Bumon)
    Rec.Name   = Name
    if SortNo == "":
      SortNo = Rec.Code
    Rec.SortNo = int(SortNo)
    Rec.AddRec(Rec)

    self.redirect("/item9020/") #
    return

app = webapp2.WSGIApplication([
    ('/item9020/', MainHandler)
], debug=True)
