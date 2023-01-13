# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class MstBumon(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 備考
  SortNo          = db.IntegerProperty()                    # 並び順

  def GetAll(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Order By SortNo,Code"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def Delete(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Query = db.GqlQuery(Sql)
    for Rec in Query.fetch(Query.count()):
      Rec.delete()
    return

  def GetRec(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      Rec = MstBusyo()
    else:
      Rec = Query.fetch(1)[0]
    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
    Rec.put()
    return 
