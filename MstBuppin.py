# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime
from MstSiiresaki    import *   # 仕入先マスタ
from MstTana         import *   # 棚マスタ
from MstKamoku       import *   # 科目マスタ

class MstBuppin(db.Model):
  KamokuCD        = db.IntegerProperty()                    # 科目CD
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 漢字名
  Kana            = db.StringProperty(multiline=False)      # カナ名
  Tanni1          = db.StringProperty(multiline=False)      # 単位1
  Tanni2          = db.StringProperty(multiline=False)      # 単位2
  Siiresaki       = db.IntegerProperty()                    # 仕入先ＣＤ
  Tanka           = db.FloatProperty()                      # 単価
  Tana            = db.IntegerProperty()                    # 棚CD
  Code2           = db.IntegerProperty()                    # 庶務CD

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
      setattr(Rec,"Kamoku",MstKamoku().GetRec(Rec.KamokuCD).Name)

    return Recs
  # 科目指定取得
  def GetKamoku(self,Kamoku):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where KamokuCD = " + Kamoku
    Sql += " Order By KamokuCD,Kana"
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
