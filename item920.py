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
from MstBusyo     import *   # 部署マスタ
from MstKengen    import *   # 権限マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = { 'LblMsg': ""
                       ,'Snap':MstSiyousya().GetAll()
                       ,'SnapBusyo':MstBusyo().GetAll()
                       ,'SnapKengen':MstKengen().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item920.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Rec = MstSiyousya()
      Rec.Code    = int(self.request.get('Code'))
      Rec.Name    = self.request.get('Name')
      Rec.BusyoCD = int(self.request.get('BusyoCD'))
      Rec.Kengen  = int(self.request.get('Kengen'))
      Rec.AddRec(Rec)
      LblMsg = "更新完了"
    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = MstSiyousya().GetRec(self.request.get('BtnSel'))
        LblMsg = "選択完了"
      if "BtnDel" in param:  # 明細削除
        MstSiyousya().Delete(param.replace("BtnDel",""))
        Rec = {} 
        LblMsg = "削除完了"

    template_values = { 'LblMsg'    :LblMsg
                       ,'Rec'       :Rec
                       ,'Snap'      :MstSiyousya().GetAll()
                       ,'SnapBusyo' :MstBusyo().GetAll()
                       ,'SnapKengen':MstKengen().GetAll()
                        }
    path = os.path.join(os.path.dirname(__file__), 'item920.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item920/', MainHandler)
], debug=True)
