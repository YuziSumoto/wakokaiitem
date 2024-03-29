# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class MstSiiresaki(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 備考

  def GetAll(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Order By Code"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def Delete(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,Code):

    if Code is None:
      return MstSiiresaki()

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap == None:
      Rec = MstSiiresaki()
    else:
      Rec = Snap.fetch(1)[0]

    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
    Rec.put()
    return 
