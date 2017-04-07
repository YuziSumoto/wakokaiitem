#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 注文者ＥＸＣＥＬ出力
#

import webapp2

#import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
import time
from calendar import monthrange
import locale

import xlwt # EXCEL 出力ライブラリ
import StringIO
import copy

from MstBusyo   import *   # 部署マスタ
from MstBuppin  import *   # 物品マスタ
from MstTeisu   import *   # 物品マスタ
from DatHizuke  import *   # 請求日付データ
from DatSeikyu  import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return


    Hizuke =  self.request.get('Hizuke') # パラメタで日付受け取り
    Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')

    RecHizuke = DatHizuke().GetRec(Hizuke)
    if RecHizuke.SimeNitizi == None:
      RecHizuke.SimeNitizi = datetime.datetime.now() + datetime.timedelta(hours=9) 
    RecHizuke.InsatuNitizi = datetime.datetime.now() + datetime.timedelta(hours=9) 
    DatHizuke().AddRec(RecHizuke)


    WorkBook =  self.ExcelSet(Hizuke)

    self.response.headers['Content-Type'] = 'application/ms-excel'
    self.response.headers['Content-Transfer-Encoding'] = 'Binary'
    self.response.headers['Content-disposition'] = 'attachment; filename="bento061.xls"'
    WorkBook.save(self.response.out)

  def ExcelSet(self,Hizuke):

    WorkBook = xlwt.Workbook()  # 新規Excelブック

    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 300
    Style.font = font

    DataRecs = MstBuppin().GetAll()

    SnapBusyo = MstBusyo().GetAll()

    GoukeiSheet = WorkBook.add_sheet(u"合計")  # シート追加
    self.SetPrintParam(GoukeiSheet) # 用紙サイズ等セット
    self.SetColSizeGoukei(GoukeiSheet,len(SnapBusyo)) # 行,列サイズセット
    self.SetTitleGoukei(GoukeiSheet,Hizuke,u"合計",DataRecs,Style)      # 固定部分セット


    GoukeiOutCol = 1
    for Rec in SnapBusyo: # 部署分ループ
      GoukeiOutCol += 1
      WorkSheet = WorkBook.add_sheet(Rec.Name)  # シート追加
      self.SetPrintParam(WorkSheet) # 用紙サイズ等セット
      self.SetColSize(WorkSheet) # 行,列サイズセット
      self.SetTitle(WorkSheet,Hizuke,Rec.Name,Style,GoukeiSheet,GoukeiOutCol)      # 固定部分セット
      self.SetData(WorkSheet,Hizuke,Rec.Code,DataRecs,Style,GoukeiSheet,GoukeiOutCol)      # データセット

    GoukeiOutCol += 1
    self.SetDataGoukei(GoukeiSheet,DataRecs,GoukeiOutCol,Style)      # 合計値データセット

    return  WorkBook
  
  def SetPrintParam(self,WorkSheet): # 用紙サイズ・余白設定
    WorkSheet.set_paper_size_code(13) # B5
    WorkSheet.set_portrait(1) # 縦
    WorkSheet.top_margin = 0.9 / 2.54    # 1インチは2.54cm
    WorkSheet.bottom_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.left_margin = 0.8 / 2.54    # 1インチは2.54cm
    WorkSheet.right_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.header_str = ''
    WorkSheet.footer_str = ''
    WorkSheet.fit_num_pages = 1
    return

  def SetColSize(self,WorkSheet):  # 行,列サイズセット

    ColWidth = ["列の幅",5,30,15,10,30]
    for i in range(1,len(ColWidth)):
      WorkSheet.col(i-1).width = int(ColWidth[i] * 400)

    return

  def SetColSizeGoukei(self,WorkSheet,BusyoSu):  # 行,列サイズセット

    WorkSheet.col(0).width = int(5 * 400)
    WorkSheet.col(1).width = int(30 * 400)
    for i in range(2,BusyoSu + 3):
      WorkSheet.col(i).width = int(10 * 400)

    return

  def SetTitle(self,WorkSheet,Hizuke,BusyoName,Style,GoukeiSheet,GoukeiOutCol):  # 固定部分セット

    OutStyle = copy.deepcopy(Style)
    OutStyle.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    OutStyle.pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
    OutStyle.font.colour_index = xlwt.Style.colour_map['white']
    
    WorkSheet.write(1,1,datetime.datetime.strftime(Hizuke, '%Y/%m/%d'),OutStyle)
    WorkSheet.write_merge(1,1,2,4,BusyoName,OutStyle)
    WorkSheet.write(3,1,u"品名",OutStyle)
    WorkSheet.write(3,2,u"定数・限度数",OutStyle)
    WorkSheet.write(3,3,u"必要数",OutStyle)
    WorkSheet.write(3,4,u"備考",OutStyle)

    GoukeiSheet.write(3,GoukeiOutCol,BusyoName,OutStyle) # 合計シートセット

    return

  def SetTitleGoukei(self,WorkSheet,Hizuke,BusyoName,DataRecs,Style):  # 固定部分セット

    OutStyle = copy.deepcopy(Style)
    OutStyle.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    OutStyle.pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
    OutStyle.font.colour_index = xlwt.Style.colour_map['white']
    
    WorkSheet.write(1,1,datetime.datetime.strftime(Hizuke, '%Y/%m/%d'),OutStyle)
    WorkSheet.write_merge(1,1,2,4,BusyoName,OutStyle)
    WorkSheet.write(3,1,u"品名",OutStyle)

    OutRow = 4
    for DataRec in DataRecs:
      WorkSheet.write(OutRow,1,DataRec.Name,Style)
      OutRow += 1

    return

  def SetData(self,WorkSheet,Hizuke,BusyoCD,DataRecs,Style,GoukeiSheet,GoukeiOutCol):  # データ部分セット

    OutRow = 4

    WkSeikyu = DatSeikyu()
    for DataRec in DataRecs:
      WorkSheet.write(OutRow,1,DataRec.Name,Style)

      RecTeisu = MstTeisu().GetRec(BusyoCD,DataRec.Code)
      if RecTeisu == {}:
        WorkSheet.write(OutRow,2,"",Style) # 定数
      else:
        WorkSheet.write(OutRow,2,RecTeisu.Suryo,Style) # 定数

      RecSeikyu = WkSeikyu.GetRec(Hizuke,BusyoCD,DataRec.Code)
      if RecSeikyu == {}:
        WorkSheet.write(OutRow,3,"",Style)
        WorkSheet.write(OutRow,4,"",Style) # 備考
        GoukeiSheet.write(OutRow,GoukeiOutCol,"",Style) # 合計シートセット
      else:
        Goukei =  getattr(DataRec,"Goukei",0)
        setattr(DataRec,"Goukei",Goukei + RecSeikyu.Suryo)
        WorkSheet.write(OutRow,3,RecSeikyu.Suryo,Style) # 数量
        WorkSheet.write(OutRow,4,RecSeikyu.Bikou,Style) # 備考
        GoukeiSheet.write(OutRow,GoukeiOutCol,RecSeikyu.Suryo,Style) # 合計シートセット
      OutRow += 1

    return

  def SetDataGoukei(self,WorkSheet,DataRecs,GoukeiOutCol,Style):  # データ部分セット

    OutStyle = copy.deepcopy(Style)
    OutStyle.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    OutStyle.pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
    OutStyle.font.colour_index = xlwt.Style.colour_map['white']
    
    WorkSheet.write(3,GoukeiOutCol,u"合計",OutStyle)

    OutRow = 4
    for DataRec in DataRecs:
      WorkSheet.write(OutRow,GoukeiOutCol,getattr(DataRec,"Goukei",0),Style)
      OutRow += 1

    return

  def SetStyle(self,Top,Bottom,Right,Left,Vert,Horz):  # セルスタイルセット

    Style = xlwt.XFStyle()
    Border = xlwt.Borders()
    if Top == "THIN":
      Border.top     = xlwt.Borders.THIN
    elif Top == "DOTTED":
      Border.top     = xlwt.Borders.DOTTED

    if Bottom == "THIN":
      Border.bottom  = xlwt.Borders.THIN
    elif Bottom == "DOTTED":
      Border.bottom     = xlwt.Borders.DOTTED

    if   Left == "THIN":
      Border.left    = xlwt.Borders.THIN
    elif Left == "DOTTED":
      Border.left    = xlwt.Borders.DOTTED

    if   Right == "THIN":
      Border.right   = xlwt.Borders.THIN
    elif Right == "DOTTED":
      Border.right   = xlwt.Borders.DOTTED

    Style.borders = Border

    Alignment      = xlwt.Alignment()

    if Vert != False:
      Alignment.vert = Vert
    if Horz != False:
      Alignment.horz = Horz

    Style.alignment = Alignment

    return Style

app = webapp2.WSGIApplication([
    ('/item610/', MainHandler)
], debug=True)
