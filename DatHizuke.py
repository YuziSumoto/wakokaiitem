# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatHizuke(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 発注日
  SimeNitizi        = db.DateTimeProperty(auto_now_add=False) # 締め日時
  InsatuNitizi      = db.DateTimeProperty(auto_now_add=False) # 印刷日時

  def GetAll(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Order By Hizuke Desc"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetRec(self,Hizuke):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def GetNext(self,Hizuke): # 指定日以降の締めていない直近取得
    Sql =  "SELECT Hizuke FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke      >= DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Sql +=  "  And  SimeNitizi=:1" # is none
    Sql +=  " Order By Hizuke"
    Snap = db.GqlQuery(Sql,None)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def Delete(self,Hizuke):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def AddRec(self,Rec):
    self.Delete(Rec.Hizuke)
    Rec.put()
    return 
