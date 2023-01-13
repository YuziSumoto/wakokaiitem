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

    Snap = MstBuppin().GetAll()

    template_values = { 'LblMsg'    : LblMsg
#                        ,'MstKamoku' :MstKamoku().GetAll2()
#                        ,'Kamoku'    :int(Kamoku)
                        ,'Snap'      :Snap
                      }
    path = os.path.join(os.path.dirname(__file__), 'item9052.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/item9052/', MainHandler)
], debug=True)
