#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
from MstBusyo   import *   # 部署マスタ
from MstBuppin  import *   # 物品マスタ
from MstTeisu   import *   # 定数マスタ
from DatSeikyu  import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Rec = {} # 画面受け渡し用領域

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '')) # パラメタ無しならCookieより
    cookieStr = 'Busyo=' + Busyo + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Rec["BusyoName"] = MstBusyo().GetRec(Busyo).Name

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', '')) # パラメタ無しならCookieより
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    dHizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')

    Code = self.request.get('Code',self.request.cookies.get('Code', '')) 
    cookieStr = 'Code=' + Code + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = { 'Busyo'     : Busyo,
                        'Hizuke'    : Hizuke,
                        'RecMst'    : MstBuppin().GetRec(Code),
                        'Rec'       : DatSeikyu().GetRec(dHizuke,Busyo,Code),
                        'RecTeisu'  : MstTeisu().GetRec(Busyo,Code),
                        'LblMsg'    : ""}
    path = os.path.join(os.path.dirname(__file__), 'item0110.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    Rec = DatSeikyu()
    Hizuke = self.request.cookies.get('Hizuke', '')
    Rec.Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')

    Rec.BusyoCode  = int(self.request.cookies.get('Busyo', '')) # Cookieより
    Rec.BuppinCode = int(self.request.cookies.get('Code', '')) # Cookieより
 
    if self.request.get('Suryo1') == "" and self.request.get('Suryo2') == "":
      Rec.Delete(Rec.Hizuke,Rec.BusyoCode,Rec.BuppinCode)
    else:
      if self.request.get('Suryo1','') == "":
        Rec.Suryo1      = 0
      else:
        Rec.Suryo1      = int(self.request.get('Suryo1'))
      if self.request.get('Suryo2','') == "":
        Rec.Suryo2      = 0
      else:
        Rec.Suryo2      = int(self.request.get('Suryo2'))
      Rec.Bikou       = self.request.get('Bikou')
      Rec.AddRec(Rec)

    MstRec = MstBuppin().GetRec(Rec.BuppinCode)
    self.redirect("/item0100/?Kamoku=" + str(MstRec.KamokuCD)  ) #
    return

app = webapp2.WSGIApplication([
    ('/item0110/', MainHandler),
], debug=True)
