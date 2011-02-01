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
        
        self.COLUMN_NAME = {}
        self.COLUMN_NAME['DATE']  = 0
        self.COLUMN_NAME['WEEK']  = 1
        self.COLUMN_NAME['MARK']  = [2,3,4,5]
        self.COLUMN_NAME['CH']    = 6
        self.COLUMN_NAME['CHREF'] = 7
        self.COLUMN_NAME['HE']    = 8
        self.COLUMN_NAME['CP']    = 9
        
        self.InsertColumn(self.COLUMN_NAME['DATE']   , "Date", wx.LIST_FORMAT_LEFT, -1) 
        self.InsertColumn(self.COLUMN_NAME['WEEK']   , "week", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['MARK'][0], "m1", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['MARK'][1], "m2", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['MARK'][2], "m3", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['MARK'][3], "m4", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['CH']     , "CH", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['CHREF']  , "CH-ref", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['HE']     , "HE", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(self.COLUMN_NAME['CP']     , "CP", wx.LIST_FORMAT_LEFT, -1)

        self.Report_date_list = []

        self.SetItemCount(len(self.Report_date_list))
        
        self.attr_positive = wx.ListItemAttr()
        self.attr_positive.SetBackgroundColour("light blue")

        self.attr_negative = wx.ListItemAttr()
        #self.attr_negative.SetBackgroundColour("orange")
        #self.attr_negative.SetBackgroundColour("orchid")
        self.attr_negative.SetBackgroundColour(wx.Colour(250,150,150,50))

        self.attr_dayoff = wx.ListItemAttr()
        self.attr_dayoff.SetBackgroundColour(wx.Colour(240,240,240,50))
        self.attr_dayoff.SetTextColour(wx.Colour(200,200,200,50))

        
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

    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them
    def OnGetItemText(self, item, col):
        if len(self.Report_date_list) > 0:
            if col == self.COLUMN_NAME['DATE']:
                return self.Report_date_list[item]['DATE'].strftime("%d/%m/%Y")
            elif col == self.COLUMN_NAME['WEEK']:
                return self.week_day[self.Report_date_list[item]['DATE'].weekday()]
            elif col == self.COLUMN_NAME['CH']:
                return str(self.Report_date_list[item]['CH'])
            elif col == self.COLUMN_NAME['CHREF']:
                return str(self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()])
            elif col == self.COLUMN_NAME['HE']: #->HE
                return str(self.Report_date_list[item]['HE'])
            elif col == self.COLUMN_NAME['CP']: #->CP
                return str(self.Report_date_list[item]['CP'])
            elif col in self.COLUMN_NAME['MARK']:
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
        if len(self.Report_date_list) > 0:
            if self.Report_date_list[item]['HE'] > self.Report_date_list[item]['CP']:
                return self.attr_positive
            elif self.Report_date_list[item]['CP'] > self.Report_date_list[item]['HE']:
                return self.attr_negative
            elif self.week_day_ch[self.Report_date_list[item]['DATE'].weekday()] == timedelta(0):
                return self.attr_dayoff
            else:
                return None
        else:
            return None
    
    def GetCPSum(self):
        cp_sum = timedelta(0)
        for report_item in self.Report_date_list:
            cp_sum = cp_sum + report_item['CP']
        return cp_sum    
    def GetHESum(self):
        he_sum = timedelta(0)
        for report_item in self.Report_date_list:
            he_sum = he_sum + report_item['HE']
        return he_sum    
    def GetCHSum(self):
        ch_sum = timedelta(0)
        for report_item in self.Report_date_list:
            ch_sum = ch_sum + report_item['CH']
        return ch_sum    
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
            self.marks_len_list = []
            for iday in range(0,delta.days+1):
                inter_date = cStart_date + timedelta(days=iday)
                report_entry = {}
                report_entry['DATE'] = inter_date
                day_marks = self.cPontDB.GetDate(inter_date.strftime("%d/%m/%Y"))
                time_mark_list = []
                for mark in day_marks: 
                    time_mark_list.append(datetime(inter_date.year,inter_date.month,inter_date.day,mark[0],mark[1],mark[2]))
                time_mark_list.sort()
                
                self.marks_len_list.append(len(time_mark_list))
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
                #->HE
                if delta_time > self.week_day_ch[inter_date.weekday()]:
                    report_entry['HE'] = delta_time - self.week_day_ch[inter_date.weekday()]
                else:    
                    report_entry['HE'] = timedelta(0)
                #->CP
                if delta_time < self.week_day_ch[inter_date.weekday()]:
                    report_entry['CP'] = self.week_day_ch[inter_date.weekday()] - delta_time
                else:    
                    report_entry['CP'] = timedelta(0)
                
                self.Report_date_list.append(report_entry) 
                #print 'outra data'
            #rebuild columns names and positions
            max_mark_number = max(self.marks_len_list)
            if max_mark_number > 4 :
                self.ClearAll()
                self.COLUMN_NAME['DATE']  = 0
                self.COLUMN_NAME['WEEK']  = 1
                #del self.COLUMN_NAME['MARK'] 
                self.COLUMN_NAME['MARK']  = list(range(2,max_mark_number+2))
                self.COLUMN_NAME['CH']    = max_mark_number+2
                self.COLUMN_NAME['CHREF'] = max_mark_number+3
                self.COLUMN_NAME['HE']    = max_mark_number+4
                self.COLUMN_NAME['CP']    = max_mark_number+5
                
                self.InsertColumn(self.COLUMN_NAME['DATE']   , "Date", wx.LIST_FORMAT_LEFT, -1) 
                self.InsertColumn(self.COLUMN_NAME['WEEK']   , "week", wx.LIST_FORMAT_LEFT, -1)
                for index,index_mark in enumerate(self.COLUMN_NAME['MARK']):
                    self.InsertColumn(index_mark, "m%d"%(index+1), wx.LIST_FORMAT_LEFT, -1)
                self.InsertColumn(self.COLUMN_NAME['CH']     , "CH", wx.LIST_FORMAT_LEFT, -1)
                self.InsertColumn(self.COLUMN_NAME['CHREF']  , "CH-ref", wx.LIST_FORMAT_LEFT, -1)
                self.InsertColumn(self.COLUMN_NAME['HE']     , "HE", wx.LIST_FORMAT_LEFT, -1)
                self.InsertColumn(self.COLUMN_NAME['CP']     , "CP", wx.LIST_FORMAT_LEFT, -1)            
                    
            self.SetItemCount(len(self.Report_date_list))
            print len(self.Report_date_list)
            for mark_column in self.COLUMN_NAME['MARK']:
                self.SetColumnWidth(mark_column, -1)
        

class CReport(xrcCReportFrame):
    '''
    classdocs
    '''
    def __init__(self, parent, PontoDB):
        '''
        Constructor
        '''
        xrcCReportFrame.__init__(self, parent)
        
        iconFile = "../res/report.ico"
        icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.cPontDB = PontoDB
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.cReportVirtual = CReportVirtualList(self.CReportListCtrl, PontoDB)
        sizer.Add(self.cReportVirtual, 1, wx.EXPAND)
        self.CReportListCtrl.SetSizer(sizer)
        self.CReportListCtrl.SetAutoLayout(True)  
        self.SetSize((900,450))
        
        self.CStopTimeText.SetValue(time.strftime("%d/%m/%Y"))
        today_time = datetime.fromtimestamp(time.time())
        delta_time = timedelta(days=21)
        start_time = today_time - delta_time 
        self.CStartTimeText.SetValue(start_time.strftime("%d/%m/%Y"))
        
        self.cSaldoText.SetValue("00:00:00")
        self.cBHTotalText.SetValue("0")
        
        
    def OnButton_CApplyButton(self, evt):
        start_time_text = self.CStartTimeText.GetValue()
        stop_time_text = self.CStopTimeText.GetValue()
        if len(start_time_text) > 0 and len(stop_time_text) > 0:
            self.cReportVirtual.ApplyRange(start_time_text,stop_time_text)     
            self.cCHTotalText.SetValue("%2.2f"%(self.cReportVirtual.GetCHSum().total_seconds()/3600))
            self.cHETotalText.SetValue(str(self.cReportVirtual.GetHESum()))
            self.cCPTotalText.SetValue(str(self.cReportVirtual.GetCPSum()))
    def OnButton_cSaldoButton(self, evt):
        #BH_date_struct = time.strptime(self.cBHTotalText.GetValue(),"%H:%M:%S")
        #print 'BH_date_struct: ',BH_date_struct
        #BH_date_struct = time.strptime("12/01/2011 09:25:15","%d/%m/%Y %H:%M:%S")
        #BH_date_struct = time.strptime("09:25:15","%H:%M:%S")
        #BH_time = time.mktime(BH_date_struct)
        #BH_datetime = datetime.fromtimestamp(BH_time)
        #BH_datetime = datetime(year=2000,month=1,day=1,hour=BH_date_struct.tm_hour,minute=BH_date_struct.tm_min,second=BH_date_struct.tm_sec)
        #BH_datetime = datetime.strptime(self.cBHTotalText.GetValue(),"%H:%M:%S")
        #BH_delta    = timedelta(hours=BH_date_struct.tm_hour,minutes=BH_date_struct.tm_min,seconds=BH_date_struct.tm_sec)
        try:
            BH_delta    = timedelta(hours=int(self.cBHTotalText.GetValue()))
        except:
            BH_delta    = timedelta(0)
           
        if self.cBHToggleButton.GetValue(): # - BH
            CP_delta = self.cReportVirtual.GetCPSum() + BH_delta
            HE_delta = self.cReportVirtual.GetHESum()
        else: # + BH
            CP_delta = self.cReportVirtual.GetCPSum()
            HE_delta = self.cReportVirtual.GetHESum() + BH_delta
            
        if HE_delta > CP_delta:
            Saldo_delta = HE_delta - CP_delta
            self.cSaldoText.SetValue('+'+str(Saldo_delta))
        else:
            Saldo_delta = CP_delta - HE_delta
            self.cSaldoText.SetValue('-'+str(Saldo_delta))
        
        
                 
    def OnTogglebutton_cBHToggleButton(self, evt):
        print evt.GetId()
        if self.cBHToggleButton.GetValue():
            self.cBHToggleButton.SetLabel('-')
        else:
            self.cBHToggleButton.SetLabel('+')
                