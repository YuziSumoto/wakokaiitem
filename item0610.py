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
from DatSime     import *   # 締めデータ
from DatSeikyu   import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Hizuke = self.request.get('HIZUKE')
    Bumon  = self.request.get('Bumon')
    Busyo  = self.request.get('BUSYO')

    if self.request.get('Mode','') == "Kakunin":
      DatSeikyu().ModKakunin(Hizuke,Busyo,self.request.get('Code'))

    if Busyo == "ALL":
      SnapBusyo = MstBusyo().GetBumon(Bumon)      # 指定部門全部署
    else:
      SnapBusyo = []
      SnapBusyo.append(MstBusyo().GetRec(Busyo)) # １部署指定

    FlgFirst = True

    Snap = []
    wMstBuppin = MstBuppin()
    wMstKamoku = MstKamoku()

    for RecBusyo in SnapBusyo: # 対象病棟分処理
      RecSime = DatSime().GetRec(Hizuke,RecBusyo.Code)
      if RecSime.SimeNitizi == None: # 締め前 
        continue # 無視

      SnapSeikyu = DatSeikyu().GetSnap(Hizuke,RecBusyo.Code)
      if len(SnapSeikyu) > 0:
        Rec  = DatSeikyu()
        setattr(Rec,"BusyoCD",RecBusyo.Code)
        if FlgFirst == True: # 1ページ目
          setattr(Rec,"KamokuCD",-1)
          FlgFirst = False
        else:
          setattr(Rec,"KamokuCD",0)
        setattr(Rec,"BuppinCode",0)
        setattr(Rec,"KamokuName",RecBusyo.Name)
        setattr(Rec,"BuppinName",RecBusyo.Name)
        Snap.append(Rec)
        for Rec in SnapSeikyu:
          RecBuppin = wMstBuppin.GetRec(Rec.BuppinCode)
          RecKamoku = wMstKamoku.GetRec(RecBuppin.KamokuCD)
          setattr(Rec,"BusyoCD",RecBusyo.Code)
          setattr(Rec,"KamokuCD",RecKamoku.Code)
          setattr(Rec,"KamokuName",RecKamoku.Name)
          setattr(Rec,"BuppinName",RecBuppin.Name)
          setattr(Rec,"Tanni1",RecBuppin.Tanni1)
          setattr(Rec,"Tanni2",RecBuppin.Tanni2)
          Snap.append(Rec)

    Snap.sort(key=lambda x:(x.BusyoCD,x.KamokuCD)) # 部署CD,科目コードでソート
      
    KamokuCD = 0
    for Rec in Snap:
      if Rec.KamokuCD != KamokuCD:
        KamokuCD = Rec.KamokuCD
        setattr(Rec,"KamokuCD2",RecKamoku.Code)
      else:
        setattr(Rec,"KamokuCD2",0)

    template_values = {
                        'Hizuke'    : Hizuke,
                        'Snap'      : Snap,
                        'LblMsg'    : ""}
    path = os.path.join(os.path.dirname(__file__), 'item0610.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item0610/', MainHandler)
], debug=True)
