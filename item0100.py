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

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Rec = {} # 画面受け渡し用領域

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '3')) # Cookieより
    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kamoku = self.request.get('Kamoku',self.request.cookies.get('Kamoku', '11')) # Cookieより
    cookieStr = 'Kamoku=' + str(Kamoku) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', ''))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('Post',"") == "NG": 
      LblMsg = "発注者欄が未入力です。"
    else:
      LblMsg = ""

    if self.request.get('Code',"") != "": # 増減ボタン押下時
      DatSeikyu().ModRec(Hizuke,Busyo,self.request.get('Code',""),self.request.get('SURYO',""),self.request.get('MODE',""))

    DataRecs = MstBuppin().GetKamoku(Kamoku,True)
    SnapSeikyu = DatSeikyu().GetSnap(Hizuke,Busyo)
    for DataRec in DataRecs:
      setattr(DataRec,"Suryo1","")
      setattr(DataRec,"Suryo2","")
      setattr(DataRec,"Bikou","")
      for SeikyuRec in SnapSeikyu:
        if SeikyuRec.BuppinCode == DataRec.Code:
          setattr(DataRec,"Suryo1",SeikyuRec.Suryo1)
          setattr(DataRec,"Suryo2",SeikyuRec.Suryo2)
          setattr(DataRec,"Bikou",SeikyuRec.Bikou)

    Rec["Busyo"]       = Busyo
    Rec["BusyoName"]   = MstBusyo().GetRec(Busyo).Name
    Rec["Hizuke"]      = Hizuke
    Rec["Hattyuusya"]  = MstHizuke().GetRec(Hizuke,Busyo).Hattyuusya
    Rec["Kanrisya"]    = MstHizuke().GetRec(Hizuke,Busyo).Kanrisya

    if Hizuke < datetime.datetime.now().strftime('%Y/%m/%d'): #今日以前
      Sime = True # 締め処理後
    elif DatSime().GetRec(Hizuke,Busyo).SimeNitizi == None:
      Sime = False # 締め処理後
    else:
      Sime = True # 締め処理後

    Yokuzitu = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=1)
    NextDay = MstHizuke().GetNext(Yokuzitu.strftime("%Y/%m/%d"),Busyo)

    template_values = { 'Rec'       :Rec,
                        'Sime'      :Sime,
                        'PrevDay'   :MstHizuke().GetPrev(Hizuke,Busyo),
                        'NextDay'   :NextDay,
                        'MstKamoku' :MstKamoku().GetAll2(),
                        'Kamoku'    :int(Kamoku),
                        'DataRecs'  :DataRecs,
                        'LblMsg'    :LblMsg}

    path = os.path.join(os.path.dirname(__file__), 'item0100.html')
    self.response.out.write(template.render(path, template_values))
    return

  def post(self): # 発注ボタン押下時

    Hizuke      = self.request.cookies.get('Hizuke', '')
    Busyo       = self.request.cookies.get('Busyo', '')
    Hattyuusya  = self.request.get('Hattyuusya','')    # 画面より
    if Hattyuusya  == "":
      self.redirect("/item0100/?Post=NG") # 再表示
    else:
      MstHizuke().ModHattyuusya(Hizuke,Busyo,Hattyuusya)
      self.redirect("/item0130/?Busyo=" +  Busyo + "&Hizuke=" + Hizuke) # 確認画面

    return

app = webapp2.WSGIApplication([
    ('/item0100/', MainHandler)
], debug=True)
