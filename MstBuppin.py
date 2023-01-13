# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime
from MstSiiresaki    import *   # 仕入先マスタ
from MstTana         import *   # 棚マスタ
from MstKamoku       import *   # 科目マスタ

# Csv取込用
import wsgiref.handlers
import os
import csv
from StringIO import StringIO

class MstBuppin(db.Model):
  Bunrui1         = db.IntegerProperty()                    # 大分類
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
  YukoFlg         = db.BooleanProperty()                    # 有効フラグ(True:有効)

  def GetAll(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Order By KamokuCD,Kana"
    Query = db.GqlQuery(Sql)
    Snap  = Query.fetch(Query.count())

    DicKamoku = MstKamoku().GetDic()

    for Rec in Snap:
      setattr(Rec,"SiiresakiName","") #MstSiiresaki().GetRec(Rec.Siiresaki).Name)
      setattr(Rec,"TanaName","") # MstTana().GetRec(Rec.Tana).Name)
      setattr(Rec,"Kamoku",DicKamoku[Rec.KamokuCD])

    return Snap

  def Kensaku(self,Kensaku):

    SnapKamoku = MstKamoku().GetAll()

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where YukoFlg = True"
    Sql += " Order By KamokuCD,Name"
    Query = db.GqlQuery(Sql)
    Snap = []
    Snap = [Rec for Rec in Query.fetch(Query.count()) if ((Kensaku in Rec.Name) or (Kensaku in Rec.Kana))]

    for Rec in Snap:
      for KamokuRec in SnapKamoku:
        if KamokuRec.Code == Rec.KamokuCD:
          setattr(Rec,"Kamoku",KamokuRec.Name)
          break

    return Snap

  # 科目指定取得
  def GetKamoku(self,Kamoku,YukoFlg=False):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where KamokuCD = " + Kamoku
    if YukoFlg == True:
      Sql += " And YukoFlg = True"
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

  def GetNewCD(self):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Order By Code Desc"
    Snap  = db.GqlQuery(Sql)
    NewCD = Snap.fetch(1)[0].Code + 1
    return NewCD

  def GetRec(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Rec      = MstBuppin()
      Rec.Code = MstBuppin().GetNewCD()
    else:
      Rec = Snap.fetch(1)[0]
    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
    Rec.put()
    return 

  def ChgYuko(self,Code,YukoFlg):
    Rec = self.GetRec(Code)
    Rec.YukoFlg = (YukoFlg == "True")
    Rec.put()
    return 

  def CSVGet(self,rawfile):

    Msg = ""

    Sql =  "SELECT * FROM " + self.__class__.__name__   # 現データ削除
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
      Rec.delete()

    csvfile = csv.reader(StringIO(rawfile))
    for row in csvfile:
      if unicode(row[0], 'cp932').isnumeric() == True:          
        Rec = MstBuppin(
           Bunrui1         = int(unicode(row[0], 'cp932'))  # 大分類
          ,KamokuCD        = int(unicode(row[1], 'cp932'))  # 科目CD
          ,Code            = int(unicode(row[2], 'cp932'))  # ＣＤ
          ,Name            = unicode(row[3], 'cp932')       # 漢字名
          ,Kana            = unicode(row[4], 'cp932')       # カナ名
          ,Tanni1          = unicode(row[5], 'cp932')       # 単位1
          ,Tanni2          = ""                             # 単位2
#          Siiresaki       = db.IntegerProperty()                    # 仕入先ＣＤ
          ,Tanka           = float(unicode(row[6], 'cp932'))         # 単価
#          Tana            = db.IntegerProperty()                    # 棚CD
#          Code2           = db.IntegerProperty()                    # 庶務CD
          ,YukoFlg         = True                    # 有効フラグ(True:有効)
		  )
        Rec.put()
        Msg +=  unicode(row[0], 'cp932') + " "
        Msg +=  unicode(row[1], 'cp932') + " "
        Msg +=  unicode(row[2], 'cp932') + " "
        Msg +=  unicode(row[3], 'cp932') + "<BR>"
      
    return Msg
