# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatSime(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 伝票日付
  Busyo             = db.IntegerProperty()                    # 部署ＣＤ
  SimeNitizi        = db.DateTimeProperty(auto_now_add=False) # 締め日時
  InsatuNitizi      = db.DateTimeProperty(auto_now_add=False) # 印刷日時

  def GetRec(self,Hizuke,Busyo):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Busyo      = " + str(Busyo)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Rec = DatSime()
      Rec.Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      Rec.Busyo  = int(Busyo)
    else:
      Rec = Snap.fetch(1)[0]
    return Rec

  def GetKikan(self,Hizuke,Days): # 指定日数分取得
    
    EndHizuke = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=Days)

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke    >= DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Hizuke    <= DATE('" + EndHizuke.strftime('%Y-%m-%d') + "')"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def AddRec(self,Rec):
    self.Delete(Rec.Hizuke,Rec.Busyo)
    Rec.put()
    return 

  def SetSime(self,Hizuke,Busyo,MODE):
    Rec = self.GetRec(Hizuke,Busyo)
    if MODE == "ON":
      Rec.SimeNitizi = datetime.datetime.now() + datetime.timedelta(hours=9) 
      Rec.put()
    else:
      Rec.delete()
    return 
