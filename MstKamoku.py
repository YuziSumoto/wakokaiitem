# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

# Csv取込用
import wsgiref.handlers
import os
import csv
from StringIO import StringIO

class MstKamoku(db.Model):
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

  def GetAll2(self): # 新システム用
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code >= 10"
    Sql += " Order By Code"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetDic(self): # 辞書形式取得
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code >= 10"
    Sql += " Order By Code"
    Snap = db.GqlQuery(Sql)
    Dic = {}
    for Rec in Snap.fetch(Snap.count()):
      Dic[Rec.Code] = Rec.Name
    return Dic

  def Delete(self,Code):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,Code):
    if Code == None:
      return MstKamoku()
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Rec = MstKamoku()
    else:
      Rec = Snap.fetch(1)[0]
    return Rec

  def AddRec(self,Rec):
    self.Delete(Rec.Code)
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
        Rec = MstKamoku(
           Code            = int(unicode(row[0], 'cp932'))  # ＣＤ
          ,Name            = unicode(row[1], 'cp932')       # 漢字名
        )
        Rec.put()
        Msg +=  unicode(row[0], 'cp932') + " "
        Msg +=  unicode(row[1], 'cp932') + "<BR>"
      
    return Msg

