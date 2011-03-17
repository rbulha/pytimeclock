'''
Created on 04/02/2011

@author: rogerio_bulha
'''
import wx 
import time

#from datetime import date
from datetime import timedelta
from datetime import datetime

from GUI_xrc import xrcCOneDayReport
from DialogMark import CDialogMark

class CReportVirtualList(wx.ListCtrl):
    def __init__(self, parent, PontoDB,target_date):
        wx.ListCtrl.__init__(
            self, parent, -1, 
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
            )

        self.parent = parent
        self.cPontoDB = PontoDB
        self.target_date = target_date
        
        self.currentItem = None
        
        self.week_day = ['MON','TUE','WED','THU','FRI','SAT','SUN']
        
        self.ch_week_1 = timedelta(hours=9,minutes=06)
        self.ch_week_2 = timedelta(hours=7,minutes=36)
        
        self.week_day_ch = [self.ch_week_1,self.ch_week_1,self.ch_week_1,self.ch_week_1,self.ch_week_2,timedelta(0),timedelta(0)]

        self.cSubType = {}
        self.cSubType[0x00] = 'NONE'
        self.cSubType[0x01] = 'NORMAL'
        self.cSubType[0x02] = 'ALMOCO'
        self.cSubType[0x03] = 'EXTRAORDINARIA'
        
        self.cTypes = {}
        self.cTypes[0x10]   = 'ENTRADA'
        self.cTypes[0x20]   = 'SAIDA'
        self.cTypes[0x30]   = 'DAYOFF'
        
        
        self.COLUMN_NAME = {}
        self.COLUMN_NAME['TIME']    = 0
        self.COLUMN_NAME['MARK']    = 1
        self.COLUMN_NAME['COMMENT'] = 2
        
        self.InsertColumn(self.COLUMN_NAME['TIME']   , "Time", wx.LIST_FORMAT_LEFT, -1) 
        self.InsertColumn(self.COLUMN_NAME['MARK']   , "Mark", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['COMMENT'], "Comment", wx.LIST_FORMAT_LEFT, -1)

        self.Report_mark_list = []
        
        self.report_one_day_statistic = {}
        self.report_one_day_statistic['DAYOFF'] = False

        self.SetItemCount(len(self.Report_mark_list))
        
        self.attr_positive = wx.ListItemAttr()
        self.attr_positive.SetBackgroundColour("light blue")

        self.attr_negative = wx.ListItemAttr()
        #self.attr_negative.SetBackgroundColour("orange")
        #self.attr_negative.SetBackgroundColour("orchid")
        self.attr_negative.SetBackgroundColour(wx.Colour(250,150,150,50))

        self.attr_dayoff = wx.ListItemAttr()
        self.attr_dayoff.SetBackgroundColour(wx.Colour(240,240,240,50))
        self.attr_dayoff.SetTextColour(wx.Colour(200,200,200,50))

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        
        '''
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        '''
    def GetSelectedItem(self): 
        if self.currentItem != None:
            return self.Report_mark_list[self.currentItem]
        else:
            return None  
          
    def DeleteSelectedItem(self):       
        if self.currentItem != None:
            target_date = self.Report_mark_list[self.currentItem]['TIME'].timetuple()
            print '[DeleteSelectedItem] - target_date: ',target_date
            old_mark = self.cPontoDB.has_mark_anywhere(target_date,
                                                       self.Report_mark_list[self.currentItem]['COMMENT'],
                                                       self.cTypes[self.Report_mark_list[self.currentItem]['MARK']&0xF0],
                                                       self.cSubType[self.Report_mark_list[self.currentItem]['MARK']&0x0F])
            if old_mark != None:
                dlg = wx.MessageDialog(self, time.strftime("%d/%m/%Y - %H:%M:%S",old_mark['time']) + '\n%s-%s'%(self.cTypes[old_mark['tipo']&0xF0],self.cSubType[old_mark['tipo']&0x0F]),
                                       'Do you want to delete this mark?',
                                       wx.YES_NO | wx.ICON_QUESTION
                                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                if( dlg.ShowModal() == wx.ID_YES):
                    print '[DeleteSelectedItem] delete mark: ',old_mark
                    self.cPontoDB.DeleteMark(old_mark)
                    self.ApplyRange(self.target_date)
                dlg.Destroy()
                            
    def OnItemSelected(self,event):
        self.currentItem = event.m_itemIndex
        print "OnItemSelected: %s\nTopItem: %s\n" %(self.GetItemText(self.currentItem), self.GetTopItem())
    def OnItemActivated(self,event):
        self.currentItem = event.m_itemIndex
        print "OnItemActivated: %s\nTopItem: %s\n" %(self.GetItemText(self.currentItem), self.GetTopItem())
        #target_time = time.strptime(self.GetItemText(self.currentItem),"%H/%M/%S")
        #target_date = datetime(self.target_date.tm_year,self.target_date.tm_mon,self.target_date.tm_mday,target_time.tm_hour,target_time.tm_min,target_time.tm_sec)
         
        #mark = dialog.GetMark()
        target_date = self.Report_mark_list[self.currentItem]['TIME'].timetuple()
        print '[OneDayReport][OnItemActivated]: ',target_date
        
        #(target_date.year,target_date.month,target_date.day,target_date.hour,target_date.minute,target_date.second),
        
        old_mark = self.cPontoDB.has_mark_anywhere(target_date,
                                                   self.Report_mark_list[self.currentItem]['COMMENT'],
                                                   self.cTypes[self.Report_mark_list[self.currentItem]['MARK']&0xF0],
                                                   self.cSubType[self.Report_mark_list[self.currentItem]['MARK']&0x0F])
        if old_mark != None:
            dialog = CDialogMark(self,target_date,self.Report_mark_list[self.currentItem]['MARK'])
            returncode = dialog.ShowModal()
            print '[CCRelogioFrame.OnButton_AddMarkBtn] - return: ',returncode
            if returncode >= 0:
                mark = dialog.GetMark()
                        
                dlg = wx.MessageDialog(self, time.strftime("%d/%m/%Y - %H:%M:%S",mark[3]) + '\n%s-%s'%(mark[0],mark[1]),
                                       'Do you want to replace this mark?',
                                       wx.YES_NO | wx.ICON_QUESTION
                                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                if( dlg.ShowModal() == wx.ID_YES):
                    print '[OnButton_AddMarkBtn] replace mark: ',old_mark
                    self.cPontoDB.DeleteMark(old_mark)
                    self.cPontoDB.TimeMark(mark[3],mark[2],mark[0],mark[1])
                    #self.cPontoDB.Print()  
                    self.ApplyRange(self.target_date)
                    #self.ColoredGauge.RefreshMark()  
                    #self.MilestonePanel.RefreshMark()                  
                dlg.Destroy()                


    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them
    def OnGetItemText(self, item, col):
        if len(self.Report_mark_list) > 0:
            if col == self.COLUMN_NAME['TIME']:
                return self.Report_mark_list[item]['TIME'].strftime("%H:%M:%S")
            elif col == self.COLUMN_NAME['MARK']:
                return '%s-%s'%(self.cTypes[self.Report_mark_list[item]['MARK']&0xF0],self.cSubType[self.Report_mark_list[item]['MARK']&0x0F])
            elif col == self.COLUMN_NAME['COMMENT']:
                return self.Report_mark_list[item]['COMMENT']
        else:
            return " - "
    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        if len(self.Report_mark_list) > 0:
            if self.cTypes[self.Report_mark_list[item]['MARK']&0xF0] == 'ENTRADA':
                return self.attr_positive
            elif self.cTypes[self.Report_mark_list[item]['MARK']&0xF0] == 'SAIDA':
                return self.attr_negative
            else:
                return None
        else:
            return None
    
    def ApplyRange(self,today_date):
        del self.Report_mark_list
        self.Report_mark_list = []
        self.DeleteAllItems()
        self.marks_len_list = []
        day_marks = self.cPontoDB.GetDate(today_date.strftime("%d/%m/%Y"))
        time_mark_list = []
        self.report_one_day_statistic['DAYOFF'] = False
        for mark in day_marks: 
            time_mark_list.append(datetime(today_date.year,today_date.month,today_date.day,mark[0],mark[1],mark[2]))
            report_entry = {}
            report_entry['TIME'] = datetime(today_date.year,today_date.month,today_date.day,mark[0],mark[1],mark[2])
            report_entry['MARK'] = mark[3]
            report_entry['COMMENT'] = mark[4]
            if mark[3] == 0x30:
                self.report_one_day_statistic['DAYOFF'] = True
            else:
                self.Report_mark_list.append(report_entry)
        time_mark_list.sort()
        
        def sort_key(entry):
            return entry['TIME']
        
        self.Report_mark_list.sort(key=sort_key)
       
        self.marks_len_list.append(len(time_mark_list))

        self.report_one_day_statistic['MARKS'] = time_mark_list
        #calculo da carga horaria
        time_in = None
        time_out = None
        delta_time = timedelta(0)
        for mark in time_mark_list:
            if time_in == None:
                time_in = mark
            elif time_out == None:
                time_out = mark
                delta_time = delta_time + (time_out-time_in)    
                time_in = None
                time_out = None
        self.report_one_day_statistic['CH'] = delta_time
        #print delta_time 
        #->HE
        if delta_time > self.week_day_ch[today_date.weekday()]:
            self.report_one_day_statistic['HE'] = delta_time - self.week_day_ch[today_date.weekday()]
        else:    
            self.report_one_day_statistic['HE'] = timedelta(0)
        #->CP
        if self.report_one_day_statistic['DAYOFF']:
            self.report_one_day_statistic['CP'] = timedelta(0)
        else:
            if delta_time < self.week_day_ch[today_date.weekday()]:
                self.report_one_day_statistic['CP'] = self.week_day_ch[today_date.weekday()] - delta_time
            else:    
                self.report_one_day_statistic['CP'] = timedelta(0)
        
        self.SetItemCount(len(self.Report_mark_list))
        #for mark_column in self.COLUMN_NAME['MARK']:
        self.SetColumnWidth(self.COLUMN_NAME['TIME'], 100)
        self.SetColumnWidth(self.COLUMN_NAME['MARK'], 160)
        self.SetColumnWidth(self.COLUMN_NAME['COMMENT'], 200)
    def GetDayOff(self):
        return self.report_one_day_statistic['DAYOFF']
        

class COneDayReport(xrcCOneDayReport):
    '''
    classdocs
    '''
    def __init__(self,parent, PontoDB,target_date):
        '''
        Constructor
        '''
        xrcCOneDayReport.__init__(self, parent)
        
        iconFile = "../res/report.ico"
        icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.cPontoDB = PontoDB
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.target_date = target_date
        
        self.cReportVirtual = CReportVirtualList(self.CReportListCtrl, PontoDB, target_date)
        self.cReportVirtual.ApplyRange(target_date)
        
        self.wxCheckDayOff.SetValue(self.cReportVirtual.GetDayOff())
        
        self.wxTitleText.SetValue(target_date.strftime(" Reporting date: %d/%m/%Y"))
        
        self.cCHTotalText.SetValue(str(self.cReportVirtual.report_one_day_statistic['CH']))
        self.cHETotalText.SetValue(str(self.cReportVirtual.report_one_day_statistic['HE']))
        self.cCPTotalText.SetValue(str(self.cReportVirtual.report_one_day_statistic['CP']))        
        
        sizer.Add(self.cReportVirtual, 1, wx.EXPAND)
        self.CReportListCtrl.SetSizer(sizer)
        self.CReportListCtrl.SetAutoLayout(True)  
        self.SetSize((510,280))

    def OnCheckbox_wxCheckDayOff(self, evt):
        print '[COneDayReport.OnCheckbox_wxCheckDayOff]',self.wxCheckDayOff.IsChecked()
        if self.wxCheckDayOff.IsChecked():
            self.cPontoDB.TimeMark(self.target_date.timetuple(),'DAY OFF','DAYOFF','NONE')
            self.cReportVirtual.ApplyRange(self.target_date)
        else:
            old_mark = self.cPontoDB.has_mark_anywhere(self.target_date.timetuple(),
                                                       'DAY OFF',
                                                       'DAYOFF',
                                                       'NONE')
            if old_mark != None:
                print '[COneDayReport.OnCheckbox_wxCheckDayOff] -  delete mark: ',old_mark
                self.cPontoDB.DeleteMark(old_mark)            

    def OnButton_wxOneDayMarkButton(self, evt):
        dialog = CDialogMark(self,self.target_date.timetuple())
        returncode = dialog.ShowModal()
        print '[COneDayReport.OnButton_wxOneDayMarkButton] - return: ',returncode
        if returncode >= 0:
            mark = dialog.GetMark()
            self.cPontoDB.TimeMark(mark[3],mark[2],mark[0],mark[1])
            self.cReportVirtual.ApplyRange(self.target_date)
            
    def OnButton_wxDeleteMarkButton(self, evt):
        self.cReportVirtual.DeleteSelectedItem()
