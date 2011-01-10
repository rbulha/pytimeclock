'''
Created on 10/01/2011

@author: rogerio_bulha
'''
import wx 

from GUI_xrc import xrcCReportFrame

class CReportVirtualList(wx.ListCtrl):
    def __init__(self, parent, PontoDB):
        wx.ListCtrl.__init__(
            self, parent, -1, 
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
            )

        self.parent = parent
        self.cPontDB = PontoDB

        '''
        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        '''
        self.InsertColumn(0, "Date", wx.LIST_FORMAT_LEFT, -1) 
        self.InsertColumn(1, "m1", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(2, "m2", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(3, "m3", wx.LIST_FORMAT_LEFT, -1)
        self.InsertColumn(4, "m4", wx.LIST_FORMAT_LEFT, -1)

        self.Report_date_list = []
        self.Report_date_list.append("09/01/2011")
        self.Report_date_list.append("10/01/2011")
        self.Report_date_list.append("11/01/2011")
                
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
        if col == 0:
            return self.Report_date_list[item]
        else:
            day_marks = self.cPontDB.GetDate(self.Report_date_list[item])
            if col <= len(day_marks):
                return "%02d:%02d:%02d" % (day_marks[col-1][0],day_marks[col-1][1],day_marks[col-1][2])
            else:
                return "00:00:00" #"%d (%d)"%(col,len(day_marks))

    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return None

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
        self.SetSize((400,350))
              
        