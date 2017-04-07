# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime
from MstKengen    import *   # 権限マスタ
from MstBusyo     import *   # 部署マスタ

class MstSiyousya(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  BusyoCD         = db.IntegerProperty()                    # 部署ＣＤ
  Name            = db.StringProperty(multiline=False)      # 氏名
  Kengen          = db.IntegerProperty()                    # 権限

  def GetAll(self):
    Sql =  "SELECT * FROM MstSiyousya"
    Sql += " Order By BusyoCD,Code"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    WMstBusyo = MstBusyo()
    for Rec in Recs:
      setattr(Rec,"KengenName",MstKengen().GetRec(Rec.Kengen).Name)
      setattr(Rec,"BusyoName",WMstBusyo.GetRec(Rec.BusyoCD).Name)

    return Recs

  def Delete(self,Code):
    Sql =  "SELECT * FROM MstSiyousya"
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,Code):
    Sql =  "SELECT * FROM MstSiyousya"
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap == None:
      Rec = {}
    else:
      Rec = Snap.fetch(1)[0]
    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
    Rec.put()
    return 
