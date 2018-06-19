# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatSeikyu(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 発注日
  BusyoCode         = db.IntegerProperty()                    # 部署CD
  BuppinCode        = db.IntegerProperty()                    # 物品CD
  Suryo             = db.IntegerProperty()                    # 数量
  Bikou             = db.StringProperty(multiline=False)      # 備考

  def GetRec(self,Hizuke,BusyoCode,BuppinCode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Sql +=  "  And  BusyoCode  = " + str(BusyoCode)
    Sql +=  "  And  BuppinCode = " + str(BuppinCode)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def GetKikan(self,BusyoCode,SHizuke,EHizuke):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where  Hizuke     >= DATE('" + SHizuke.replace("/","-") + "')"
    Sql +=  "  And   Hizuke     <  DATE('" + EHizuke.replace("/","-") + "')"
    Sql +=  "  And   BusyoCode  = " + str(BusyoCode)
    Snap = db.GqlQuery(Sql)
    Recs = {}  # 空の辞書
    for Rec in  Snap:
      if Recs.has_key(Rec.BuppinCode):# 既出?
        Recs[Rec.BuppinCode] = Recs[Rec.BuppinCode] + Rec.Suryo # 加算
      else:
        Recs[Rec.BuppinCode] = Rec.Suryo # セット
    
    return Recs

  def Delete(self,Hizuke,BusyoCode,BuppinCode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Sql +=  "  And  BusyoCode  = " + str(BusyoCode)
    Sql +=  "  And  BuppinCode = " + str(BuppinCode)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def AddRec(self,Rec):
    self.Delete(Rec.Hizuke,Rec.BusyoCode,Rec.BuppinCode)
    Rec.put()
    return 
