#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

from MstBuppin  import *    # 物品マスタ
from MstBusyo    import *   # 部署マスタ
from MstTeisu    import *   # 定数マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return
    LblMsg = ""
    if self.request.get('BuppinCode') != "": # パラメタあり？
      BuppinCD = self.request.get('BuppinCode')   # パラメタ取得
      cookieStr = 'BuppinCD=' + BuppinCD + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
      LblMsg = "物品コード指定なし？？？"


    template_values = { 'LblMsg': LblMsg
                       ,'Rec'          :MstBuppin().GetRec(BuppinCD)
                       ,'Snap'         :self.GetRecs(BuppinCD)
                      }
    path = os.path.join(os.path.dirname(__file__), 'item960.html')
    self.response.out.write(template.render(path, template_values))

  def GetRecs(self,BuppinCD):

    Snap = MstBusyo().GetAll()
    for Rec in Snap:
      RecTeisu = MstTeisu().GetRec(Rec.Code,BuppinCD)
      if RecTeisu != {}:
        Rec.Suryo = int(RecTeisu.Suryo)

    return Snap

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""
    BuppinCD = int(self.request.cookies.get('BuppinCD', ''))
    BusyoCD  = int(self.request.cookies.get('BusyoCD' , '0'))

    if self.request.get('BtnMod')  != '': # 更新ボタン
      Rec = MstTeisu()
      if BusyoCD == 0: # 部署未指定なら無視
        pass
      elif self.request.get('Suryo') == "":
        Rec.Delete(BusyoCD,BuppinCD)
      else:
        Rec.BusyoCD       = BusyoCD
        Rec.BuppinCD      = BuppinCD
        Rec.Suryo         = int(self.request.get('Suryo'))
        Rec.AddRec(Rec)
      LblMsg = "更新完了"
      Rec = MstBuppin().GetRec(BuppinCD)

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        BusyoCD = param.replace("BtnSel","")
        cookieStr = 'BusyoCD=' + BusyoCD + ';'     # Cookie保存
        self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
        Rec = MstBuppin().GetRec(BuppinCD)
        Rec.BusyoName = MstBusyo().GetRec(BusyoCD).Name
        RecTeisu = MstTeisu().GetRec(BusyoCD,BuppinCD)
        if RecTeisu != {}:
          Rec.Suryo = int(RecTeisu.Suryo)
          
    Snap = MstBusyo().GetAll()
    template_values = { 'LblMsg': LblMsg
                       ,'Rec'          :Rec
                       ,'Snap'         :self.GetRecs(BuppinCD)
                      }
    path = os.path.join(os.path.dirname(__file__), 'item960.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item960/', MainHandler)
], debug=True)
