'''
Created on 10/01/2011

@author: rogerio_bulha
'''
import wx 
import time

from datetime import date
from datetime import timedelta
from datetime import datetime

from GUI_xrc import xrcCReportFrame

class CReportVirtualList(wx.ListCtrl):
    def __init__(self, parent, PontoDB):
        wx.ListCtrl.__init__(
            self, parent, -1, 
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
            )

        self.parent = parent
        self.cPontDB = PontoDB
        
        self.week_day = ['MON','TUE','WED','THU','FRI','SAT','SUN']
        
        self.ch_week_1 = timedelta(hours=9,minutes=06)
        self.ch_week_2 = timedelta(hours=7,minutes=36)
        
        self.week_day_ch = [self.ch_week_1,self.ch_week_1,self.ch_week_1,self.ch_week_1,self.ch_week_2,timedelta(0),timedelta(0)]

        '''
        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        '''
        self.InsertColumn(0, "Date", wx.LIST_FORMAT_LEFT, -1) 
        self.InsertColumn(1, "week", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(2, "m1", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(3, "m2", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(4, "m3", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(5, "m4", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(6, "CH", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(7, "CH-ref", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(8, "HE", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(9, "CP", wx.LIST_FORMAT_LEFT, -1)

        self.Report_date_list = []

        self.SetItemCount(len(self.Report_date_list))
        
        '''
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        '''

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them
    def OnGetItemText(self, item, col):
        if len(self.Report_date_list) > 0:
            if col == 0:
                return self.Report_date_list[item]['DATE'].strftime("%d/%m/%Y")
            elif col == 1:
                return self.week_day[self.Report_date_list[item]['DATE'].weekday()]
            elif col == 6:
                return str(self.Report_date_list[item]['CH'])
            elif col == 7:
                return str(self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()])
            elif col == 8: #->HE
                if self.Report_date_list[item]['CH'] > self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()]:
                    HE_delta = self.Report_date_list[item]['CH'] - self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()]
                else:    
                    HE_delta = timedelta(0)
                return str(HE_delta)
            elif col == 9: #->CP
                if self.Report_date_list[item]['CH'] < self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()]:
                    HE_delta = self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()] - self.Report_date_list[item]['CH']
                else:    
                    HE_delta = timedelta(0)
                return str(HE_delta)
            elif col in [2,3,4,5]:
                day_marks = self.Report_date_list[item]['MARKS']
                if len(day_marks) > 0:
                    imark = col - 2
                    if imark < len(day_marks):
                        return day_marks[imark].strftime("%H:%M:%S")
                    else:
                        return "00:00:00" #"%d (%d)"%(col,len(day_marks))
                else:
                    return "00:00:00"                
        else:
            return " - "
    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return None
    def ApplyRange(self,start_date,end_date):
        start_date_struct = time.strptime(start_date,"%d/%m/%Y")
        end_date_struct = time.strptime(end_date,"%d/%m/%Y")
        
        cStart_date = date(start_date_struct.tm_year,start_date_struct.tm_mon,start_date_struct.tm_mday)
        cEnd_date = date(end_date_struct.tm_year,end_date_struct.tm_mon,end_date_struct.tm_mday)
        if cEnd_date > cStart_date:
            delta = cEnd_date - cStart_date
            del self.Report_date_list
            self.Report_date_list = []
            self.DeleteAllItems()

            for iday in range(0,delta.days+1):
                inter_date = cStart_date + timedelta(days=iday)
                report_entry = {}
                report_entry['DATE'] = inter_date
                day_marks = self.cPontDB.GetDate(inter_date.strftime("%d/%m/%Y"))
                time_mark_list = []
                for mark in day_marks: 
                    time_mark_list.append(datetime(inter_date.year,inter_date.month,inter_date.day,mark[0],mark[1],mark[2]))
                time_mark_list.sort()
                '''
                for teste in time_mark_list:
                    print teste
                '''    
                report_entry['MARKS'] = time_mark_list
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
                report_entry['CH'] = delta_time
                #print delta_time 
                self.Report_date_list.append(report_entry) 
                #print 'outra data'
                         
            '''   
            self.Report_date_list.append("09/01/2011")
            self.Report_date_list.append("10/01/2011")
            self.Report_date_list.append("11/01/2011")
            '''       
            self.SetItemCount(len(self.Report_date_list))
            print len(self.Report_date_list)
        

class CReport(xrcCReportFrame):
    '''
    classdocs
    '''
    def __init__(self, parent, PontoDB):
        '''
        Constructor
        '''
        xrcCReportFrame.__init__(self, parent)
        
        self.cPontDB = PontoDB
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.cReportVirtual = CReportVirtualList(self.CReportListCtrl, PontoDB)
        sizer.Add(self.cReportVirtual, 1, wx.EXPAND)
        self.CReportListCtrl.SetSizer(sizer)
        self.CReportListCtrl.SetAutoLayout(True)  
        self.SetSize((600,400))
    def OnButton_CApplyButton(self, evt):
        start_time_text = self.CStartTimeText.GetValue()
        stop_time_text = self.CStopTimeText.GetValue()
        if len(start_time_text) > 0 and len(stop_time_text) > 0:
            self.cReportVirtual.ApplyRange(start_time_text,stop_time_text)     
        