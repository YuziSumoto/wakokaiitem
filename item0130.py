#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
from MstBusyo    import *   # 部署マスタ
from MstKamoku   import *   # 科目マスタ
from MstBuppin   import *   # 部署マスタ
from MstHizuke   import *   # 日付マスタ
from DatSime     import *   # 締めデータ
from DatSeikyu   import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより
    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', ''))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('Kanrisya','') == "None": # Postからの戻り?
      LblMsg = u"所属長未入力では発注できません"
    else:
      LblMsg = u""

    RecBusyo = MstBusyo().GetRec(Busyo) # １部署指定
    RecHizuke = MstHizuke().GetRec(Hizuke,Busyo)

    Snap = []
    wMstBuppin = MstBuppin()
    wMstKamoku = MstKamoku()

    SnapSeikyu = DatSeikyu().GetSnap(Hizuke,RecBusyo.Code)
    for Rec in SnapSeikyu:
      RecBuppin = wMstBuppin.GetRec(Rec.BuppinCode)
      RecKamoku = wMstKamoku.GetRec(RecBuppin.KamokuCD)
      setattr(Rec,"KamokuCD",RecKamoku.Code)
      setattr(Rec,"KamokuName",RecKamoku.Name)
      setattr(Rec,"BuppinName",RecBuppin.Name)
      setattr(Rec,"Tanni1",RecBuppin.Tanni1)
      setattr(Rec,"Tanni2",RecBuppin.Tanni2)
      Snap.append(Rec)

    Snap.sort(key=lambda x:(x.KamokuCD)) # 部署CD,科目コードでソート
      
    KamokuCD = 0
    for Rec in Snap:
      if Rec.KamokuCD != KamokuCD:
        KamokuCD = Rec.KamokuCD
        setattr(Rec,"KamokuCD2",RecKamoku.Code)
      else:
        setattr(Rec,"KamokuCD2",0)

    template_values = {
                        'BusyoName' : RecBusyo.Name,
                        'Hizuke'    : Hizuke,
                        'RecHizuke' : RecHizuke,
                        'Snap'      : Snap,
                        'LblMsg'    : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0130.html')
    self.response.out.write(template.render(path, template_values))

  def post(self): # 発注ボタン押下時

    Hizuke      = self.request.cookies.get('Hizuke', '')
    Busyo       = self.request.cookies.get('Busyo', '')
    Kanrisya    = self.request.get('Kanrisya','')    # 画面より
    if Kanrisya == '':
      self.redirect("/item0130/?Kanrisya=None") # 再表示
    else:
      MstHizuke().ModKanrisya(Hizuke,Busyo,Kanrisya)
      self.redirect("/item0000/?MODE=KANRYO" ) # 元の画面へ

    return

app = webapp2.WSGIApplication([
    ('/item0130/', MainHandler)
], debug=True)
