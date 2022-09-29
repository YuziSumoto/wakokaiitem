#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
#from MstUser   import *   # 使用者マスタ
from MstSiyousya  import *   # 使用者マスタ
from MstTana      import *   # 棚マスタ
from MstSiiresaki import *   # 仕入先マスタ
from MstBuppin    import *   # 物品マスタ
from MstKamoku    import *   # 科目マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = { 'LblMsg': ""
                       ,'Snap'         :MstBuppin().GetAll()
                       ,'SnapSiiresaki':MstSiiresaki().GetAll()
                       ,'SnapTana'     :MstTana().GetAll()
                       ,'SnapKamoku'   :MstKamoku().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item950.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    Rec = {} 
    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Rec = MstBuppin()
      Rec.Code      = int(self.request.get('Code'))
      Rec.Name      = self.request.get('Name')
      Rec.Kana      = self.request.get('Kana')
      Rec.Siiresaki = int(self.request.get('Siiresaki'))
      Rec.Tanni1    = self.request.get('Tanni1')
      Rec.Tanni2    = self.request.get('Tanni2')
      Rec.Tana      = int(self.request.get('Tana'))
      if self.request.get('Code2') != "":
        Rec.Code2     = int(self.request.get('Code2'))
      if self.request.get('Tanka') != "":
        Rec.Tanka     = float(self.request.get('Tanka'))
      Rec.KamokuCD  = int(self.request.get('KamokuCD'))
      Rec.AddRec(Rec)
      LblMsg = "更新完了"

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = MstBuppin().GetRec(self.request.get('BtnSel'))
        LblMsg = "選択完了"
      if "BtnDel" in param:  # 明細削除
        MstBuppin().Delete(param.replace("BtnDel",""))
        Rec = {} 
        LblMsg = "削除完了"
      if "BtnTeisu" in param:  # 定数メンテ
        Parm = "?BuppinCode=" + param.replace("BtnTeisu","")
        self.redirect("/item960/" + Parm) #
        return

    template_values = { 'LblMsg'       :LblMsg
                       ,'Rec'          :Rec
                       ,'Snap'         :MstBuppin().GetAll()
                       ,'SnapSiiresaki':MstSiiresaki().GetAll()
                       ,'SnapTana'     :MstTana().GetAll()
                       ,'SnapKamoku'   :MstKamoku().GetAll()
                        }
    path = os.path.join(os.path.dirname(__file__), 'item950.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item950/', MainHandler)
], debug=True)
