#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime

from MstBumon    import *   # 部門マスタ
from MstBusyo    import *   # 部署マスタ
from MstHizuke   import *   # 発注日マスタ
from DatSime     import *   # 締めデータ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    LblMsg = ""

#    LblMsg += "S=" +  str(datetime.datetime.now()) 

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', datetime.datetime.now().strftime('%Y/%m/%d')))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Bumon = int(self.request.get('Bumon',self.request.cookies.get('Bumon', '1'))) # 部門指定
    cookieStr = 'Bumon=' + str(Bumon) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('ChgHizuke','') != "": # 更新ボタン押下時
      if self.request.get('Busyo','') == "ALL":
        for Rec in MstBusyo().GetBumon(Bumon):
          MstHizuke().ChgRec(self.request.get('ChgHizuke',''),str(Rec.Code))
      else:
        MstHizuke().ChgRec(self.request.get('ChgHizuke',''),self.request.get('Busyo',''))

    Zenzitu  = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=-1)
    Zenzitu  = Zenzitu.strftime("%Y/%m/%d")
    Yokuzitu = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=1)
    Yokuzitu = Yokuzitu.strftime("%Y/%m/%d")

    wDatSime = DatSime()
    LstHizuke = []
    wHizuke = datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
    YOUBI = [u"月",u"火",u"水",u"木",u"金",u"土",u"日"]
#    for Ctr in range(0,7): # 20221117 
    for Ctr in range(0,10):
      Rec = {}
      Rec["Hizuke"] = wHizuke.strftime('%Y/%m/%d')
      Rec["sHizuke"] = wHizuke.strftime('%m/%d') + "<BR>(" + YOUBI[wHizuke.weekday()] + ")"
      LstHizuke.append(Rec)
      wHizuke +=  datetime.timedelta(days=1)

    lDatSime = DatSime().GetKikan(Hizuke,10) 
    lMstHizuke = MstHizuke().GetKikan(Hizuke,10)

    Snap = MstBusyo().GetBumon(Bumon)
    for Rec in Snap:
      RecSime = wDatSime.GetRec(Hizuke,Rec.Code)
      setattr(Rec,"SimeNitizi",RecSime.SimeNitizi)
      SnapHizuke = []
      wHizuke = datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
#      for Ctr in range(0,7): # 20221117 
      for Ctr in range(0,10):
        wRec = {"Hizuke":wHizuke.strftime('%Y/%m/%d')}
        if self.ChkSime(lDatSime,wHizuke,Rec.Code) == True: # 締め済
          wRec["Zyotai"] = 2
        elif self.ChkHizuke(lMstHizuke,wHizuke,Rec.Code) == True:# 発注日
          wRec["Zyotai"] = 1
        else: # 発注日外
          wRec["Zyotai"] = 0
        SnapHizuke.append(wRec) # 締め後
        wHizuke +=  datetime.timedelta(days=1)
      setattr(Rec,"SnapHizuke" ,SnapHizuke) # 発注日テーブルセット

#    LblMsg += "E=" +  str(datetime.datetime.now()) 

    template_values = { 'Bumon'     : int(Bumon),
                        'SnapBumon' : MstBumon().GetAll(),
                        'Hizuke'    : Hizuke,
                        'Zenzitu'   : Zenzitu,
                        'Yokuzitu'  : Yokuzitu,
                        'Snap'      : Snap,
                        'LstHizuke' : LstHizuke,
                        'LblMsg'    : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item9100.html')
    self.response.out.write(template.render(path, template_values))

  def ChkSime(self,Snap,Hizuke,Busyo):
    Ret = False
    for Rec in Snap:
      if (Rec.Hizuke == Hizuke) and (Rec.Busyo == Busyo):        
        if Rec.Hizuke == None:
          Ret = False
          break
        else:
          Ret = True
          break
    return Ret

  def ChkHizuke(self,Snap,Hizuke,Busyo):
    Ret = False
    for Rec in Snap:
      if (Rec.Hizuke == Hizuke) and (Rec.Busyo == Busyo):        
        Ret = True
        break
    return Ret

app = webapp2.WSGIApplication([
    ('/item9100/', MainHandler)
], debug=True)
