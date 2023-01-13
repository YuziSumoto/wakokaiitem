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
from MstHizuke  import *   # 請求日マスタ

from DatSime    import *   # 請求日付データ
from DatSeikyu  import *   # 請求データ

import urllib
# from urllib.parse import unquote

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Rec = {} # 画面受け渡し用領域

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより
    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kensaku = self.request.get('Kensaku','')

    sHizuke = self.request.get('sHizuke','') # ,self.request.cookies.get('sHizuke', ''))
    if sHizuke == '':
      dHizuke = datetime.datetime.now() - datetime.timedelta(days=28)
      sHizuke = dHizuke.strftime("%Y/%m/%d")#今日の日付から4週間(28日)前

    eHizuke = self.request.get('eHizuke','') # self.request.cookies.get('eHizuke', ''))
    if eHizuke == '':
      dHizuke = datetime.datetime.now()
      eHizuke = dHizuke.strftime("%Y/%m/%d") #今日の日付

    Snap = DatSeikyu().GetKikan2(Busyo,sHizuke,eHizuke) # 期間内データ取得
    for DataRec in Snap:
      rBuppin = MstBuppin().GetRec(DataRec.BuppinCode)
      if Kensaku != "": #検索キー指定
        if Kensaku not in rBuppin.Name:
          continue
      setattr(DataRec,"Code",str(DataRec.BuppinCode).zfill(5))
      setattr(DataRec,"Name",rBuppin.Name)
      setattr(DataRec,"Tanni1",rBuppin.Tanni1)
      setattr(DataRec,"Tanni2",rBuppin.Tanni2)

    Rec["Busyo"]     = Busyo
    Rec["BusyoName"] = MstBusyo().GetRec(Busyo).Name

    template_values = { 'Rec'       :Rec,
                        'sHizuke'   :sHizuke.replace("/","-"),
                        'eHizuke'   :eHizuke.replace("/","-"),
                        'Kensaku'   :Kensaku,
                        'DataRecs'  :Snap,
                        'LblMsg'    : ""}

    path = os.path.join(os.path.dirname(__file__), 'item0150.html')
    self.response.out.write(template.render(path, template_values))
    return

  def post(self):

    LblMsg = ""
    Rec = {} # 画面受け渡し用領域

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより
    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    sHizuke = self.request.get('sHizuke',"")
    eHizuke = self.request.get('eHizuke',"")
    Kensaku = self.request.get('Kensaku',"")

#    Parm = "?sHizuke=" + sHizuke + "&eHizuke=" + eHizuke + "&Kensaku=" + Kensaku

    Snap = DatSeikyu().GetKikan2(Busyo,sHizuke,eHizuke) # 期間内データ取得
    for DataRec in Snap:
      rBuppin = MstBuppin().GetRec(DataRec.BuppinCode)
      if Kensaku != "": #検索キー指定
        if Kensaku not in rBuppin.Name:
          continue
      setattr(DataRec,"Code",str(DataRec.BuppinCode).zfill(5))
      setattr(DataRec,"Name",rBuppin.Name)
      setattr(DataRec,"Tanni1",rBuppin.Tanni1)
      setattr(DataRec,"Tanni2",rBuppin.Tanni2)

    Rec["Busyo"]     = Busyo
    Rec["BusyoName"] = MstBusyo().GetRec(Busyo).Name

    template_values = { 'Rec'       :Rec,
                        'sHizuke'   :sHizuke.replace("/","-"),
                        'eHizuke'   :eHizuke.replace("/","-"),
                        'Kensaku'   :Kensaku,
                        'DataRecs'  :Snap,
                        'LblMsg'    : ""}

    path = os.path.join(os.path.dirname(__file__), 'item0150.html')
    self.response.out.write(template.render(path, template_values))
    return


app = webapp2.WSGIApplication([
    ('/item0150/', MainHandler)
], debug=True)
