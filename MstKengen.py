# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class MstKengen(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 備考

  def GetAll(self):
#    Sql =  "SELECT * FROM MstKengen"
#    Sql += " Order By Code"
#    Snap = db.GqlQuery(Sql)
#    if Snap.count() == 0:
#      Recs = {}
#    else:
#      Recs = Snap.fetch(Snap.count())
    Recs = []
    Rec = MstKengen()
    Rec.Code = 1
    Rec.Name = u"一般"
    Recs.append(Rec)
    Rec = MstKengen()
    Rec.Code = 2
    Rec.Name = u"管理者"
    Recs.append(Rec)
    return Recs

  def Delete(self,Code):
    Sql =  "SELECT * FROM MstKengen"
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,Code):
    Recs = []
    Rec = MstKengen()
    if Code == 1:
      Rec.Name = u"一般"
      Recs.append(Rec)
    elif Code == 2:
      Rec.Name = u"管理者"
      Recs.append(Rec)

    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
    Rec.put()
    return 
