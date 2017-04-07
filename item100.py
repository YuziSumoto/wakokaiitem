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

from DatHizuke  import *   # 請求日付データ
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

    RecHizuke = DatHizuke().GetNext(datetime.datetime.now()) # 今日以降の未閉め発注日
    if RecHizuke == {}:
      Hizuke = datetime.datetime.now() # メニュー画面で弾いてるので発生しないが年のため
    else:
      Hizuke = RecHizuke.Hizuke 
      cookieStr = 'Hizuke=' + Hizuke.strftime('%Y/%m/%d') + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
      Rec["Hizuke"] = Hizuke.strftime('%Y/%m/%d') 

    DataRecs = MstBuppin().GetAll()
    WkSeikyu = DatSeikyu()
    for DataRec in DataRecs:
      RecSeikyu = WkSeikyu.GetRec(Hizuke,BusyoCD,DataRec.Code)
      if RecSeikyu == {}:
        setattr(DataRec,"Suryo","")
      else:
        setattr(DataRec,"Suryo",RecSeikyu.Suryo)
        setattr(DataRec,"Bikou",RecSeikyu.Bikou)

    template_values = { 'Rec'       :Rec,
                        'DataRecs'  :DataRecs,
                        'LblMsg'    : ""}

    path = os.path.join(os.path.dirname(__file__), 'item100.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    BusyoCD = self.request.cookies.get('BusyoCD', '') # Cookieより
    Hizuke  = self.request.cookies.get('Hizuke', '')  # Cookieより

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 更新ボタン？
        Parm = "?BusyoCode=" + BusyoCD # Cookieより
        Parm += "&Code=" + param.replace("BtnSel","") # 押下ボタン名
        Parm += "&Hizuke=" + Hizuke.replace("/","-")  # 日付
        self.redirect("/item110/" + Parm) #
        return

    Rec["BusyoName"] = MstBusyo().GetRec(BusyoCD).Name
    Rec["Hizuke"] = DatHizuke().GetNext(datetime.datetime.now()).strftime('%Y/%m/%d') # 今日の日付

    LblMsg = ""
    template_values = { 'Rec'       :Rec,
                        'MstBuppin' :MstBuppin().GetAll(),
                        'LblMsg'   : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item100.html')
    self.response.out.write(template.render(path, template_values))
    return

app = webapp2.WSGIApplication([
    ('/item100/', MainHandler)
], debug=True)
