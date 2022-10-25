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


  def get(self):  # 初期表示

    LblMsg = ""

    if self.request.get('Code',"") != "": # 有効・無効ボタン押下時
      MstBuppin().ChgYuko(self.request.get('Code'),self.request.get('YukoFlg'))
      
    Kamoku = self.request.get('Kamoku',self.request.cookies.get('Kamoku', '11')) # Cookieより
    cookieStr = 'Kamoku=' + str(Kamoku) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = { 'LblMsg'    : LblMsg,
                        'MstKamoku' :MstKamoku().GetAll2(),
                        'Kamoku'    :int(Kamoku),
                        'Snap'      :MstBuppin().GetKamoku(Kamoku)
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9050.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item9050/', MainHandler)
], debug=True)
