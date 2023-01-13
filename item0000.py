#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime

from MstBumon   import *   # 部門マスタ
from MstBusyo   import *   # 部署マスタ
from MstHizuke  import *   # 発注日マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    LblMsg = ""

    Bumon = int(self.request.get('Bumon',self.request.cookies.get('Bumon', '1'))) # 部門指定
    Busyo = self.request.get('Busyo',self.request.cookies.get('Bumon', '1')) # 部署指定
    SnapBusyo = MstBusyo().GetBumon(Bumon)

    if MstBusyo().GetRec(int(Busyo)).Bumon == None:
      pass
    elif Bumon != int(MstBusyo().GetRec(int(Busyo)).Bumon) : # 部門変更時      
      Busyo = SnapBusyo[0].Code # 最初の部署に→１件もないなら落ちろ！

    Hizuke = datetime.datetime.now().strftime('%Y/%m/%d') # 今日

    NextDay = MstHizuke().GetNext(Hizuke,Busyo)

    if NextDay == False:
      LblMsg += u"次回発注日は未定です。"
    else:
      LblMsg += u"次回発注日は" + NextDay + u"です。"

    if self.request.get('MODE',' ') == "KANRYO":   # 発注完了戻り
      LblMsg = "発注完了しました。"

    if NextDay != False:
      Hizuke = NextDay
    else:
      PrevDay = MstHizuke().GetPrev(Hizuke,Busyo)
      if PrevDay != False:
        Hizuke = PrevDay
      else:
        Huzuke = False

    cookieStr = 'Bumon=' + str(Bumon) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    cookieStr = 'Busyo=' + str(Busyo) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = { 'Bumon'     : int(Bumon),
                        'Busyo'     : int(Busyo),
                        'Hizuke'    : Hizuke,
                        'SnapBumon' : MstBumon().GetAll(),
                        'MstBusyo'  : SnapBusyo,
                        'LblMsg'    : LblMsg}
    path = os.path.join(os.path.dirname(__file__), 'item0000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = ""

    Bumon = int(self.request.get('Bumon',"0"))
    Busyo = int(self.request.get('BusyoCD',"0"))

    self.redirect("/item0000/?Bumon=" + str(Bumon) + "&Busyo=" + str(Busyo)) # 部署変更

    return

app = webapp2.WSGIApplication([
    ('/item0000/', MainHandler)
], debug=True)
