# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatSeikyuH(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 発注日
  BusyoCode         = db.IntegerProperty()                    # 部署CD
  DenpyoNo          = db.IntegerProperty()                    # 伝票No(0:定期,1～臨時)
  Sime              = db.DateTimeProperty(auto_now_add=False) # 締め日時
  Print             = db.DateTimeProperty(auto_now_add=False) # 印刷日時

  def GetSnap(self,Hizuke,BusyoCode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  BusyoCode  = " + str(BusyoCode)
    Snap = db.GqlQuery(Sql)
    Recs = Snap.fetch(Snap.count())
    return Snap

  def GetRec(self,Hizuke,BusyoCode,BuppinCode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Sql +=  "  And  BusyoCode  = " + str(BusyoCode)
    Sql +=  "  And  BuppinCode = " + str(BuppinCode)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def ModRec(self,Hizuke,Busyo,Code,Suryo,Mode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.replace("/","-") + "')"
    Sql +=  "  And  BusyoCode  = " + str(Busyo)
    Sql +=  "  And  BuppinCode = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0: # レコード無し
      if Mode == "PLUS":
        Rec = DatSeikyu()
        Rec.Hizuke     = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
        Rec.BusyoCode  = int(Busyo)
        Rec.BuppinCode = int(Code)
        if Suryo == "1":
          Rec.Suryo1   = 1
        else:
          Rec.Suryo2   = 1
        Rec.put()
    else:
      Rec = Snap.fetch(1)[0]
      if Suryo == "1":
        if Mode == "PLUS":
          Rec.Suryo1 = (Rec.Suryo1 or 0) + 1 
          Rec.put()
        else:
          Rec.Suryo1 = (Rec.Suryo1 or 0) - 1 
          Rec.put()
      else: # Suryo2
        if Mode == "PLUS":
          Rec.Suryo2 = (Rec.Suryo2 or 0) + 1 
          Rec.put()
        elif (Rec.Suryo2 == None) or (Rec.Suryo2 == 0):
          pass
        else:
          Rec.Suryo2 = Rec.Suryo2 - 1 
          Rec.put()

    return 

  def GetKikan(self,BusyoCode,SHizuke,EHizuke):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where  Hizuke     >= DATE('" + SHizuke.replace("/","-") + "')"
    Sql +=  "  And   Hizuke     <  DATE('" + EHizuke.replace("/","-") + "')"
    Sql +=  "  And   BusyoCode  = " + str(BusyoCode)
    Snap = db.GqlQuery(Sql)
    Recs = {}  # 空の辞書
    for Rec in  Snap:
      if Recs.has_key(Rec.BuppinCode):# 既出?
        Recs[Rec.BuppinCode] = Recs[Rec.BuppinCode] + Rec.Suryo # 加算
      else:
        Recs[Rec.BuppinCode] = Rec.Suryo # セット
    
    return Recs

  def Delete(self,Hizuke,BusyoCode,BuppinCode):
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where Hizuke     = DATE('" + Hizuke.strftime("%Y-%m-%d") + "')"
    Sql +=  "  And  BusyoCode  = " + str(BusyoCode)
    Sql +=  "  And  BuppinCode = " + str(BuppinCode)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def AddRec(self,Rec):
    self.Delete(Rec.Hizuke,Rec.BusyoCode,Rec.BuppinCode)
    Rec.put()
    return 
