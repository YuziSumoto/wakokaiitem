# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class MstTeisu(db.Model):
  BusyoCD         = db.IntegerProperty()                    # 部署CD
  BuppinCD        = db.IntegerProperty()                    # 物品CD
  Suryo           = db.IntegerProperty()                    # 定数・限度数

  def GetRec(self,BusyoCD,BuppinCD):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where BusyoCD  = " + str(BusyoCD)
    Sql += " And   BuppinCD = " + str(BuppinCD)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def Delete(self,BusyoCD,BuppinCD):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where BusyoCD  = " + str(BusyoCD)
    Sql += " And   BuppinCD = " + str(BuppinCD)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def AddRec(self,Rec):
    self.Delete(Rec.BusyoCD,Rec.BuppinCD)
    Rec.put()
    return 
