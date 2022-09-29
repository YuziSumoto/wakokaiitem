#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
from MstBusyo   import *   # 部署マスタ
from MstKamoku  import *   # 科目マスタ
from MstBuppin  import *   # 物品マスタ

from DatHizuke  import *   # 請求日付データ
from DatSeikyu  import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Rec = {} # 画面受け渡し用領域

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより
    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kamoku = self.request.get('Kamoku',self.request.cookies.get('Kamoku', '10')) # Cookieより
    cookieStr = 'Kamoku=' + str(Kamoku) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = self.request.get('Hizuke',datetime.datetime.now().strftime('%Y/%m/%d'))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    DataRecs = MstBuppin().GetKamoku(Kamoku)
    WkSeikyu = DatSeikyu()
    for DataRec in DataRecs:
      RecSeikyu = WkSeikyu.GetRec(datetime.datetime.strptime(Hizuke, '%Y/%m/%d'),Busyo,DataRec.Code)
      if RecSeikyu == {}:
        setattr(DataRec,"Suryo","")
      else:
        setattr(DataRec,"Suryo",RecSeikyu.Suryo)
        setattr(DataRec,"Bikou",RecSeikyu.Bikou)

    Rec["BusyoName"] = MstBusyo().GetRec(Busyo).Name
    Rec["Hizuke"] = Hizuke

    template_values = { 'Rec'       :Rec,
                        'MstKamoku' :MstKamoku().GetAll2(),
                        'Kamoku'    :int(Kamoku),
                        'DataRecs'  :DataRecs,
                        'LblMsg'    : ""}

    path = os.path.join(os.path.dirname(__file__), 'item0100.html')
    self.response.out.write(template.render(path, template_values))
    return

  def post(self): # 基本来ない

    Kamoku  = int(self.request.get('Kamoku',"0"))    # 画面より
#    Busyo   = self.request.cookies.get('Busyo', '')  # Cookieより
#    Hizuke  = self.request.cookies.get('Hizuke', '') # Cookieより

#    for param in self.request.arguments(): 
#      if "BtnSel" in param:  # 更新ボタン？
#        Parm = "?BusyoCode=" + BusyoCD # Cookieより
#        Parm += "&Code=" + param.replace("BtnSel","") # 押下ボタン名
#        Parm += "&Hizuke=" + Hizuke.replace("/","-")  # 日付
#        self.redirect("/item110/" + Parm) #
#        return

    self.redirect("/item0100/" + "?Kamoku=" + str(Kamoku)) # 科目変更

    return

app = webapp2.WSGIApplication([
    ('/item0100/', MainHandler)
], debug=True)
