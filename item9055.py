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
from MstSiyousya  import *   # 使用者マスタ
from MstTana      import *   # 棚マスタ
from MstSiiresaki import *   # 仕入先マスタ
from MstBuppin    import *   # 物品マスタ
from MstKamoku    import *   # 科目マスタ

class MainHandler(webapp2.RequestHandler):


  def get(self):  # 初期表示

    Code = self.request.get('Code',self.request.cookies.get('Code', '')) # Cookieより
    cookieStr = 'Code=' + str(Code) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Rec = MstBuppin().GetRec(Code)
    if Rec.KamokuCD == None:
      Rec.KamokuCD =  int(self.request.get('Kamoku',"10"))
                        
    template_values = { 'LblMsg'       : ""
                       ,'Rec'          : Rec
                       ,'SnapKamoku'   : MstKamoku().GetAll2()
                       ,'SnapSiiresaki': MstSiiresaki().GetAll()
                       ,'SnapTana'     : MstTana().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9055.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

    LblMsg = ""

    Rec = MstBuppin()
    Rec.Code      = int(self.request.get('Code'))
    Rec.Name      = self.request.get('Name')
    Rec.Kana      = self.request.get('Kana')
    Rec.Siiresaki = int(self.request.get('Siiresaki'))
    Rec.Tanni1    = self.request.get('Tanni1')
    Rec.Tanni2    = self.request.get('Tanni2')
    Rec.Tana      = int(self.request.get('Tana'))
    if self.request.get('Code2') != "":
      Rec.Code2     = int(self.request.get('Code2'))
    if self.request.get('Tanka') != "":
      Rec.Tanka     = float(self.request.get('Tanka'))
    Rec.KamokuCD  = int(self.request.get('KamokuCD'))
    Rec.YukoFlg   = True
    Rec.AddRec(Rec)
    self.redirect("/item9050/") #

app = webapp2.WSGIApplication([
    ('/item9055/', MainHandler)
], debug=True)
