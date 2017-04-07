# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime
from MstSiiresaki    import *   # 仕入先マスタ
from MstTana         import *   # 棚マスタ

class MstBuppin(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 氏名
  Tanni1          = db.StringProperty(multiline=False)      # 単位1
  Tanni2          = db.StringProperty(multiline=False)      # 単位2
  Siiresaki       = db.IntegerProperty()                    # 仕入先ＣＤ
  Tana            = db.IntegerProperty()                    # 棚CD

  def GetAll(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Order By Siiresaki,Code"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    for Rec in Recs:
      setattr(Rec,"SiiresakiName",MstSiiresaki().GetRec(Rec.Siiresaki).Name)
      setattr(Rec,"TanaName",MstTana().GetRec(Rec.Tana).Name)

    return Recs

  def Delete(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
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
