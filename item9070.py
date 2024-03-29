#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
#from MstUser      import *   # 使用者マスタ
from MstKamoku  import *     # 科目マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):  # 初期表示

    template_values = { 'LblMsg': ""
                       ,'Snap':MstKamoku().GetAll()
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9070.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):  # ボタン押下時

    LblMsg = ""
    Code = self.request.get('Code') # 入力値受取
    Name = self.request.get('Name') # 入力値受取
    Mst = MstKamoku()
    Rec = {} 

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Mst.Code = int(Code)
      Mst.Name = Name
      Mst.AddRec(Mst)
      LblMsg = "更新完了"
    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = Mst.GetRec(self.request.get('BtnSel'))
        LblMsg = "選択完了"
      if "BtnDel" in param:  # 明細削除
        Mst.Delete(param.replace("BtnDel",""))
        LblMsg = "削除完了"

    template_values = { 'LblMsg' :LblMsg
                       ,'Rec'    :Rec
                       ,'Snap'   :Mst.GetAll()
                        }
    path = os.path.join(os.path.dirname(__file__), 'item9070.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item9070/', MainHandler)
], debug=True)
