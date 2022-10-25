# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime
from DatSime import * # 締めマスタ

class MstHizuke(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 発注日
  Busyo             = db.IntegerProperty()                    # 部署CD

  def ChkRec(self,Hizuke,Busyo):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Busyo      = " + str(Busyo)
    Snap = db.GqlQuery(Sql)

    if Snap.count() == 0:
      return False

    return True

  def GetWeek(self,Hizuke): # １週間分取得
    
    EndHizuke = datetime.datetime.strptime(Hizuke,"%Y/%m/%d") + datetime.timedelta(days=7)

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke    >= DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Hizuke    <= DATE('" + EndHizuke.strftime('%Y-%m-%d') + "')"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def GetNext(self,Hizuke,Busyo):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     >= DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Busyo       = " + str(Busyo)
    Sql +=  "  Order by Hizuke"
    Snap = db.GqlQuery(Sql)

    bRet = False
    for Rec in Snap.fetch(Snap.count()):
      SimeRec = DatSime().GetRec(Rec.Hizuke.strftime('%Y/%m/%d'),Busyo)
      if SimeRec.SimeNitizi == None: # 締めチェック
        bRet = Rec.Hizuke.strftime('%Y/%m/%d')
        break
      
    return bRet

  def GetPrev(self,Hizuke,Busyo):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     < DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Busyo      = " + str(Busyo)
    Sql +=  "  Order by Hizuke Desc"
    Snap = db.GqlQuery(Sql)

    Ret = False
    for Rec in Snap.fetch(Snap.count()):
      Ret = Rec.Hizuke.strftime('%Y/%m/%d')
      break
      
    return Ret

  def ChgRec(self,Hizuke,Busyo):
    if self.ChkRec(Hizuke,Busyo) == True:
      self.DelRec(Hizuke,Busyo)
    else:
      Rec = MstHizuke()
      Rec.Hizuke = datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      Rec.Busyo  = int(Busyo)
      Rec.put()
      
    return 

  def DelRec(self,Hizuke,Busyo):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  Busyo      = " + str(Busyo)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return
