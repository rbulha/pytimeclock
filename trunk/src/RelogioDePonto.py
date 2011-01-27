# -*- coding: UTF-8 -*-
import wx
import time

from GUI_xrc import xrcCRelogioFrame
from GUI_xrc import xrcCMarkDlg

from PontoDB            import CPontoDB
from BookMark           import CColoredGauge
from Milestones         import CMilestonePanel
from Report             import CReport
from Labeling           import CLabeling as LABELING
from wx.lib.wordwrap    import wordwrap

class CTrayBar(wx.TaskBarIcon):
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        
        self.parent = parent
        
        iconFile = "../res/timeout.ico"
        self.icon_timeout = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        
        iconFile = "../res/date.ico"
        self.icon_timeok = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)      
        
        self.ID_timeout = wx.NewId()
        self.ID_timeok  = wx.NewId()
        self.ID_show   = wx.NewId()
        self.ID_exit   = wx.NewId()
        self.ID_mark   = wx.NewId()
        self.ID_report = wx.NewId()
        
        self.Bind(wx.EVT_MENU, self.OnTimeout, id=self.ID_timeout)
        self.Bind(wx.EVT_MENU, self.OnTimeOk, id=self.ID_timeok)
        self.Bind(wx.EVT_MENU, self.OnShow, id=self.ID_show)
        self.Bind(wx.EVT_MENU, self.OnExit, id=self.ID_exit)
        self.Bind(wx.EVT_MENU, self.parent.OnButton_AddMarkBtn, id=self.ID_mark)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnShow)
        self.Bind(wx.EVT_MENU, self.parent.OnButton_CReportButton, id=self.ID_report)
        
    def Iconize(self,timeout=False):
        if timeout:
            self.SetIcon(self.icon_timeout,'Time clock\n(Timeout)')
        else:  
            self.SetIcon(self.icon_timeok,'Time clock\nPress the right button to place a mark.')
            #'Relógio de ponto\nPressione o botão direito para marcar o ponto.')
    
    def OnShow(self, event):
        self.parent.UpdateInterface()
        self.parent.Show()
        self.parent.Raise()
        self.parent.Restore()
        self.RemoveIcon()
        
    def OnExit(self, event): 
        self.RemoveIcon()   
        self.parent.Close(True)
      
    def OnTimeout(self, event):
        self.Iconize(True)
        #self.parent.OnUserLaunchSim(event)
      
    def OnTimeOk(self, event):
        self.Iconize(False)
        #self.parent.OnUserStopsSim(event)
      
    def CreatePopupMenu(self):
        menu = wx.Menu()
        #menu.Append(self.ID_start, "Start")
        #menu.Append(self.ID_stop, "Stop")
        menu.Append(self.ID_show, "Show")
        menu.Append(self.ID_mark, "Mark")
        menu.Append(self.ID_report, "Report")          
        menu.Append(self.ID_exit, "Exit")   
        return menu

class CDialogMark(xrcCMarkDlg):
    def __init__(self,parent):
        xrcCMarkDlg.__init__(self, parent)
        time_stamp = time.localtime()
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp))
        self.wxTimeSliderHour.SetValue(time_stamp.tm_hour)
        self.wxTimeSlider.SetValue(time_stamp.tm_min)
        self.wxTimeSliderSec.SetValue(time_stamp.tm_sec)
        self.wxTimeSliderDay.SetValue(time_stamp.tm_mday)
        self.wxTimeSliderMonth.SetValue(time_stamp.tm_mon)
        self.wxTimeSliderYear.SetValue(time_stamp.tm_year)
        self.wxTimeSliderYear.SetRange(time_stamp.tm_year-50,time_stamp.tm_year+50)
        
    def OnButton_CMarkBtn(self, evt):
        print '[CDialogMark] - Type:',self.CRadio_Type.GetSelection()
        print '[CDialogMark] - subType:',self.CRadio_subType.GetSelection() 
        print '[CDialogMark] - comment:',self.CCommentTextCtrl.GetValue()
        self.EndModal(self.CRadio_Type.GetSelection()|self.CRadio_subType.GetSelection())
    def OnButton_CCancelBtn(self, evt):
        self.EndModal(-1)
    def OnClose(self, evt):
        self.EndModal(-1)    
    def GetMark(self):
        tipo = ['ENTRADA','SAIDA']
        sub  = ['NORMAL','ALMOCO','EXTRAORDINARIA']
        return (tipo[self.CRadio_Type.GetSelection()],   \
                sub[self.CRadio_subType.GetSelection()], \
                self.CCommentTextCtrl.GetValue(),        \
                time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y"))
    def OnScroll_wxTimeSlider(self, evt):
        #print '[CDialogMark][OnScroll_wxTimeSlider] - evt: ',evt.GetPosition()  
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        #time_stamp[4] = evt.GetPosition()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          evt.GetPosition(),
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))
    def OnScroll_wxTimeSliderHour(self, evt):
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          evt.GetPosition(),
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))        
    def OnScroll_wxTimeSliderSec(self, evt):
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          evt.GetPosition(),
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))        
    def OnScroll_wxTimeSliderDay(self, evt):
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          evt.GetPosition(),
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))        
    def OnScroll_wxTimeSliderMonth(self, evt):
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        time_stamp_aux = (time_stamp.tm_year,
                          evt.GetPosition(),
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))        
    def OnScroll_wxTimeSliderYear(self, evt):
        time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        time_stamp_aux = (evt.GetPosition(),
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux))        
                     
class CCRelogioFrame(xrcCRelogioFrame):
    def __init__(self, parent):
        xrcCRelogioFrame.__init__(self, parent)
        #load application icon
        iconFile = "../res/date.ico"
        icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.SetSize((460,350))
        self.RelogioTrayBar = CTrayBar(self)
        self.RelogioTrayBar.Iconize(False)
        self.Bind(wx.EVT_ICONIZE, self.OnIconize)
        self.Bind(wx.EVT_CLOSE, self.OnUserClose)
        
        self.Hide()
        
        self.SetMinSize((460,350))
        
        #load data base
        self.cPontoDB = CPontoDB()
        self.cPontoDB.LoadDB()
        self.cPontoDB.Print()
        
        #self.ColoredGauge = CColoredGauge(self.GaugePanel, self.OnGaugeGetToday)
        self.ColoredGauge = CColoredGauge(self, self.OnGaugeGetToday)
        
        self.wxFrameBoxSizer = self.GetSizer()
        self.wxFrameBoxSizer.Add(self.ColoredGauge, 1, wx.EXPAND|wx.ALL)
        
        self.ColoredGauge.RefreshMark()
        
        #MilestoneBox = wx.StaticBox(self, -1, "Milestones")
        #MilestoneBox.SetBackgroundColour(wx.LIGHT_GREY)
        #MilestoneBox.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        #bsizer = wx.StaticBoxSizer(MilestoneBox, wx.VERTICAL)        
        
        self.MilestonePanel = CMilestonePanel(self, self.OnGaugeGetToday)
        self.MilestonePanel.RefreshMark()
        
        #t = wx.StaticText(self, -1, "Controls placed \"inside\" the box are really its siblings")
        #bsizer.Add(self.MilestonePanel, 1, wx.EXPAND|wx.ALL, 0)
        self.wxFrameBoxSizer.Add(self.MilestonePanel, 1, wx.EXPAND|wx.ALL)
        
    def OnGaugeGetToday(self):
        return self.cPontoDB.GetToday()    
        
    def OnUserClose(self, event):
        if not event.CanVeto():
            print '[CCRelogioFrame.OnUserIconize] - Destroy'
            self.Destroy()
            wx.GetApp().ExitMainLoop()
        else:    
            print '[CCRelogioFrame.OnUserIconize] - Iconize'
            self.RelogioTrayBar.Iconize(False)
            self.Hide()
            event.Veto()
                    
    def OnIconize(self, event):
        print '[CCRelogioFrame.OnIconize]', event.Iconized()
        if event.Iconized():
            self.RelogioTrayBar.Iconize(False)
            self.Hide()
        else:
            self.UpdateInterface()
            #self.SetSize(event.GetSize())
            #self.Refresh()
    def OnButton_ClearAllMarks(self, evt):
        self.ColoredGauge.DeleteAllBookMarks() 
        self.cPontoDB.ClearToday()       
    def OnButton_AddMarkBtn(self, evt):
        print '[CCRelogioFrame.OnButton_AddMarkBtn] - ShowDialog'
        dialog = CDialogMark(self)
        returncode = dialog.ShowModal()
        print '[CCRelogioFrame.OnButton_AddMarkBtn] - return: ',returncode
        if returncode >= 0:
            mark = dialog.GetMark()
            old_mark = self.cPontoDB.has_mark_anywhere(mark[3],mark[2],mark[0],mark[1])
            if old_mark != None:
                dlg = wx.MessageDialog(self, 'Do you want to replace this mark?',
                                       'Ponto',
                                       wx.YES_NO | wx.ICON_QUESTION
                                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                if( dlg.ShowModal() == wx.ID_YES):
                    print '[OnButton_AddMarkBtn] replace mark: ',mark
                    self.cPontoDB.DeleteMark(old_mark)
                    self.cPontoDB.TimeMark(mark[3],mark[2],mark[0],mark[1])
                    self.cPontoDB.Print()  
                    self.ColoredGauge.RefreshMark()  
                    self.MilestonePanel.RefreshMark()                  
                dlg.Destroy()                
            else:    
                print '[OnButton_AddMarkBtn] mark: ',mark
                self.cPontoDB.TimeMark(mark[3],mark[2],mark[0],mark[1])
                self.cPontoDB.Print()  
                self.ColoredGauge.RefreshMark() 
                self.MilestonePanel.RefreshMark()   
                
    def OnButton_ExitBtn(self, evt):               
        print '[CCRelogioFrame.OnButton_ExitBtn] - Destroy'
        self.Destroy()
        wx.GetApp().ExitMainLoop()
    def OnButton_CReportButton(self, evt):
        self.cReportFrame = CReport(None,self.cPontoDB)
        self.cReportFrame.Show(True)
    def UpdateInterface(self):
        #self.SetSize(self.GetSize())
        self.MilestonePanel.RefreshMark() 
        self.MilestonePanel.Refresh()
        self.ColoredGauge.RefreshMark()
        self.Refresh()
    def OnMaximize(self, evt):
        print '[CCRelogioFrame.OnMaximize]',evt   
    def OnButton_AboutButton(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = LABELING.APP_LONG_NAME
        info.Version = LABELING.VERSION
        info.Copyright = LABELING.COPYRIGHT
        info.Description = wordwrap(
        LABELING.ABOUT_DESCRIPTION
        ,650, wx.ClientDC(self))
        info.WebSite = (LABELING.COMPANY_WEBSITE, LABELING.COMPANY_NAME)
        info.Developers = [ LABELING.DEVELOPER_MAIN,
                            LABELING.DEVELOPER_MAIN_CONT ]
        wx.AboutBox(info)
class CRelogioApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)   
    def OnInit(self):
        self.SetExitOnFrameDelete(True)
        self.RelogioFrame = CCRelogioFrame(None)
        self.SetTopWindow(self.RelogioFrame)
        return True
        
if __name__ == '__main__':
    RelogioApp = CRelogioApp()
    RelogioApp.MainLoop()
