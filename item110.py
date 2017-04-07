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

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Rec = {} # 画面受け渡し用領域

    if self.request.get('BusyoCode') != "": # パラメタあり？
      BusyoCD = self.request.get('BusyoCode')   # パラメタ取得
      cookieStr = 'BusyoCD=' + BusyoCD + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
      BusyoCD = self.request.cookies.get('BusyoCD', '') # Cookieより

    Rec["BusyoName"] = MstBusyo().GetRec(BusyoCD).Name

    if self.request.get('Hizuke') != "": # パラメタあり？
      Hizuke = self.request.get('Hizuke').replace("-","/")   # パラメタ取得
      cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
      Rec["Hizuke"] = Hizuke
      Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')

    if self.request.get('Code') != "": # パラメタあり？
      Code = self.request.get('Code')   # パラメタ取得
      cookieStr = 'Code=' + Code + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
      Code = self.request.cookies.get('Code', '') # Cookieより

    RecMst = MstBuppin().GetRec(Code)
    Rec["Name"] = RecMst.Name
    Rec["Tanni1"] = RecMst.Tanni1
    SnapSeikyu =DatSeikyu().GetRec(Hizuke,BusyoCD,Code)
    if SnapSeikyu == {}:
      Rec["Suryo"] = ""
    else:
      Rec["Suryo"] = SnapSeikyu.Suryo
      Rec["Bikou"] = SnapSeikyu.Bikou

    RecTeisu = MstTeisu().GetRec(BusyoCD,Code) # 定数セット
    if RecTeisu != {}:
      Rec["Teisu"] = RecTeisu.Suryo

    template_values = { 'Rec'       :Rec,
                        'LblMsg'    : ""}
    path = os.path.join(os.path.dirname(__file__), 'item110.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    RecSeikyu = DatSeikyu()
    Hizuke = self.request.cookies.get('Hizuke', '')
    RecSeikyu.Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')

    RecSeikyu.BusyoCode  = int(self.request.cookies.get('BusyoCD', '')) # Cookieより
    RecSeikyu.BuppinCode = int(self.request.cookies.get('Code', '')) # Cookieより
 
    if self.request.get('Suryo') == "":
      RecSeikyu.Delete(RecSeikyu.Hizuke,RecSeikyu.BusyoCode,RecSeikyu.BuppinCode)
    elif self.request.get('Suryo') == "":
      RecSeikyu.Delete(RecSeikyu.Hizuke,RecSeikyu.BusyoCode,RecSeikyu.BuppinCode)
    else:
      RecSeikyu.Suryo      = int(self.request.get('Suryo'))
      RecSeikyu.Bikou      = self.request.get('Bikou')
      RecSeikyu.AddRec(RecSeikyu)
    
    Parm = "?BusyoCode=" + str(RecSeikyu.BusyoCode) # Cookieより
    self.redirect("/item100/" + Parm) #
    return

app = webapp2.WSGIApplication([
    ('/item110/', MainHandler),
    ('/', MainHandler)
], debug=True)
