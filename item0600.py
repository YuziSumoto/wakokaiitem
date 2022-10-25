#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
from MstBusyo    import *   # 部署マスタ
from MstHizuke   import *   # 発注日マスタ
from DatSime     import *   # 締めデータ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    Hizuke = self.request.get('Hizuke',self.request.cookies.get('Hizuke', datetime.datetime.now().strftime('%Y/%m/%d')))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('SIME','') != "":
      DatSime().SetSime(Hizuke,self.request.get('BUSYO',''),self.request.get('SIME',''))

    Zenzitu  = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=-1)
    Zenzitu  = Zenzitu.strftime("%Y/%m/%d")
    Yokuzitu = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=1)
    Yokuzitu = Yokuzitu.strftime("%Y/%m/%d")

    Snap = MstBusyo().GetAll()
    wDatSime = DatSime()
    for Rec in Snap:
      if MstHizuke().ChkRec(Hizuke,Rec.Code) == True:
        setattr(Rec,"HattyuBi","YES")
        RecSime = wDatSime.GetRec(Hizuke,Rec.Code)
        setattr(Rec,"SimeNitizi",RecSime.SimeNitizi)
      else:
        setattr(Rec,"HattyuBi","NO")

    template_values = {
                        'Hizuke'    : Hizuke,
                        'Zenzitu'   : Zenzitu,
                        'Yokuzitu'  : Yokuzitu,
                        'Snap'      : Snap,
                        'LblMsg'    : ""}
    path = os.path.join(os.path.dirname(__file__), 'item0600.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item0600/', MainHandler)
], debug=True)
