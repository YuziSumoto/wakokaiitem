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
    Busyo  = self.request.get('BUSYO')

    RecBusyo = MstBusyo().GetRec(Busyo)
    Snap = DatSeikyu().GetSnap(Hizuke,Busyo)
    wMstBuppin = MstBuppin()
    wMstKamoku = MstKamoku()
    for Rec in Snap:
      RecBuppin = wMstBuppin.GetRec(Rec.BuppinCode)
      RecKamoku = wMstKamoku.GetRec(RecBuppin.KamokuCD)
      setattr(Rec,"KamokuCD",RecKamoku.Code)
      setattr(Rec,"KamokuName",RecKamoku.Name)
      setattr(Rec,"BuppinName",RecBuppin.Name)
      setattr(Rec,"Tanni1",RecBuppin.Tanni1)
      setattr(Rec,"Tanni2",RecBuppin.Tanni2)

    Snap.sort(key=lambda x: x.KamokuCD) # 科目コードでソート
      
    KamokuCD = 0
    for Rec in Snap:
      if Rec.KamokuCD != KamokuCD:
        KamokuCD = Rec.KamokuCD
        setattr(Rec,"KamokuCD2",RecKamoku.Code)
      else:
        setattr(Rec,"KamokuCD2",0)

    template_values = {
                        'Hizuke'    : Hizuke,
                        'RecBusyo'  : RecBusyo,
                        'Snap'      : Snap,
                        'LblMsg'    : ""}
    path = os.path.join(os.path.dirname(__file__), 'item0610.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item0610/', MainHandler)
], debug=True)
