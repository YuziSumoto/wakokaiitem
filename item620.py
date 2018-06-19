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
from DatSeikyu  import *   # 請求データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    WorkBook =  self.ExcelSet()

    self.response.headers['Content-Type'] = 'application/ms-excel'
    self.response.headers['Content-Transfer-Encoding'] = 'Binary'
    self.response.headers['Content-disposition'] = 'attachment; filename="bento061.xls"'
    WorkBook.save(self.response.out)

  def ExcelSet(self):

    WorkBook = xlwt.Workbook()  # 新規Excelブック

    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 300
    Style.font = font

    SnapBusyo = MstBusyo().GetAll()

    Honzitu = datetime.date.today()
    if Honzitu.month >= 10: # 10月より後
      SHizuke = str(Honzitu.year) + '/04/01' # 当年4月
      EHizuke = str(Honzitu.year) + '/10/01' # 当年4月
    else:
      SHizuke = str(Honzitu.year - 1) + '/10/01' # 前年10月
      EHizuke = str(Honzitu.year) + '/04/01' # 当年4月

    Kikan = SHizuke + u"～" + EHizuke

    for Rec in SnapBusyo: # 部署分ループ
      WorkSheet = WorkBook.add_sheet(Rec.Name)  # シート追加
      self.SetPrintParam(WorkSheet)             # 用紙サイズ等セット
      self.SetColSize(WorkSheet)                # 行,列サイズセット
      self.SetTitle(WorkSheet,Rec.Name,Kikan,Style)      # 固定部分セット
      self.SetData(WorkSheet,SHizuke,EHizuke,Rec.Code,Style)      # データセット


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

    ColWidth = ["列の幅",5,10,60,10,10,10,20]
    for i in range(1,len(ColWidth)):
      WorkSheet.col(i-1).width = int(ColWidth[i] * 400)

    return


  def SetTitle(self,WorkSheet,BusyoName,Kikan,Style):  # 固定部分セット

    OutStyle = copy.deepcopy(Style)
    OutStyle.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    OutStyle.pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
    OutStyle.font.colour_index = xlwt.Style.colour_map['white']
    
    WorkSheet.write_merge(1,1,1,2,BusyoName,OutStyle)
    WorkSheet.write_merge(1,1,4,6,Kikan,OutStyle)
    WorkSheet.write(3,1,u"庶務CD",OutStyle)
    WorkSheet.write(3,2,u"品名",OutStyle)
    WorkSheet.write(3,3,u"数量",OutStyle)
    WorkSheet.write(3,4,u"単価",OutStyle)
    WorkSheet.write(3,5,u"合計金額",OutStyle)
    WorkSheet.write(3,6,u"勘定項目",OutStyle)

    return


  def SetData(self,WorkSheet,SHizuke,EHizuke,BusyoCD,Style):  # データ部分セット

    OutRow = 4

    Snap = DatSeikyu().GetKikan(BusyoCD,SHizuke,EHizuke)
    WBuppin = MstBuppin()
    WKamoku = MstKamoku()
    for Key in Snap.keys():
      RecBuppin =  WBuppin.GetRec(Key)
      WorkSheet.write(OutRow,1,RecBuppin.Code2,Style)
      WorkSheet.write(OutRow,2,RecBuppin.Name,Style)
      WorkSheet.write(OutRow,3,Snap[Key],Style) # 合計数量
      WorkSheet.write(OutRow,4,RecBuppin.Tanka,Style)
      if RecBuppin.Tanka != None:
        WorkSheet.write(OutRow,5,Snap[Key] * RecBuppin.Tanka,Style)
      if RecBuppin.KamokuCD != None:
        WorkSheet.write(OutRow,6,WKamoku.GetRec(RecBuppin.KamokuCD).Name,Style)
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
    ('/item620/', MainHandler)
], debug=True)
