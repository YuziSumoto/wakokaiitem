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

    Rec["Busyo"]     = Busyo
    Rec["BusyoName"] = MstBusyo().GetRec(Busyo).Name
    Rec["Hizuke"]    = Hizuke

    if Hizuke < datetime.datetime.now().strftime('%Y/%m/%d'): #今日以前
      Sime = True # 締め処理後
    elif DatSime().GetRec(Hizuke,Busyo).SimeNitizi == None:
      Sime = False # 締め処理後
    else:
      Sime = True # 締め処理後

    template_values = { 'Rec'       :Rec,
                        'Sime'      :Sime,
                        'PrevDay'   :MstHizuke().GetPrev(Hizuke,Busyo),
                        'NextDay'   :MstHizuke().GetNext(Hizuke,Busyo),
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
