#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime
from urllib import urlopen,quote # URLパラメタエンコード

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from MstBuppin    import *   # 物品マスタ
from MstKamoku    import *   # 科目マスタ

class MainHandler(webapp2.RequestHandler):


  def get(self):  # 初期表示

    LblMsg = ""

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '')) # パラメタ無しならCookieより
    cookieStr = 'Busyo=' + Busyo + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', '')) # パラメタ無しならCookieより
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kensaku  =  self.request.get('Kensaku',"")

    if Kensaku == "":
      Snap = [] # 空スナップ
    else:
      Snap = MstBuppin().Kensaku(Kensaku)

    template_values = { 'LblMsg'    : LblMsg,
                        'Kensaku'   : Kensaku,
                        'Busyo'     : Busyo,
                        'Hizuke'    : Hizuke,
                        'Snap'      : Snap
                      }
    path = os.path.join(os.path.dirname(__file__), 'item0120.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = ""

    Busyo = self.request.get('Busyo',self.request.cookies.get('Busyo', '')) # パラメタ無しならCookieより
    cookieStr = 'Busyo=' + Busyo + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', '')) # パラメタ無しならCookieより
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kensaku = self.request.get('Kensaku')

    if Kensaku == "":
      Snap = [] # 空スナップ
    else:
      Snap = MstBuppin().Kensaku(Kensaku)

    template_values = { 'LblMsg'    : LblMsg,
                        'Kensaku'   : Kensaku,
                        'Busyo'     : Busyo,
                        'Hizuke'    : Hizuke,
                        'Snap'      : Snap
                      }
    path = os.path.join(os.path.dirname(__file__), 'item0120.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item0120/', MainHandler)
], debug=True)
