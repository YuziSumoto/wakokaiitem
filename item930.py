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
from MstTana  import *     # 棚マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = { 'LblMsg': ""
                       ,'Snap':MstTana().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item930.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""
    Code = self.request.get('Code') # 入力値受取
    Name = self.request.get('Name') # 入力値受取
    TanaMst = MstTana()
    Rec = {} 

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      TanaMst.Code = int(Code)
      TanaMst.Name = Name
      TanaMst.AddRec(TanaMst)
      LblMsg = "更新完了"
    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = TanaMst.GetRec(self.request.get('BtnSel'))
        LblMsg = "選択完了"
      if "BtnDel" in param:  # 明細削除
        TanaMst.Delete(param.replace("BtnDel",""))
        LblMsg = "削除完了"

    template_values = { 'LblMsg' :LblMsg
                       ,'Rec'    :Rec
                       ,'Snap'   :MstTana().GetAll()
                        }
    path = os.path.join(os.path.dirname(__file__), 'item930.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item930/', MainHandler)
], debug=True)
