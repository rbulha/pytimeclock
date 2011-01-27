# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcCRelogioFrame(wx.Frame):
#!XRCED:begin-block:xrcCRelogioFrame.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcCRelogioFrame.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreFrame()
        self.PreCreate(pre)
        get_resources().LoadOnFrame(pre, parent, "CRelogioFrame")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.AddMarkBtn = xrc.XRCCTRL(self, "AddMarkBtn")
        self.CReportButton = xrc.XRCCTRL(self, "CReportButton")
        self.ExitBtn = xrc.XRCCTRL(self, "ExitBtn")
        self.ClearAllMarks = xrc.XRCCTRL(self, "ClearAllMarks")
        self.AboutButton = xrc.XRCCTRL(self, "AboutButton")

        self.Bind(wx.EVT_BUTTON, self.OnButton_AddMarkBtn, self.AddMarkBtn)
        self.Bind(wx.EVT_BUTTON, self.OnButton_CReportButton, self.CReportButton)
        self.Bind(wx.EVT_BUTTON, self.OnButton_ExitBtn, self.ExitBtn)
        self.Bind(wx.EVT_BUTTON, self.OnButton_ClearAllMarks, self.ClearAllMarks)
        self.Bind(wx.EVT_BUTTON, self.OnButton_AboutButton, self.AboutButton)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)

#!XRCED:begin-block:xrcCRelogioFrame.OnButton_AddMarkBtn
    def OnButton_AddMarkBtn(self, evt):
        # Replace with event handler code
        print "OnButton_AddMarkBtn()"
#!XRCED:end-block:xrcCRelogioFrame.OnButton_AddMarkBtn        

#!XRCED:begin-block:xrcCRelogioFrame.OnButton_CReportButton
    def OnButton_CReportButton(self, evt):
        # Replace with event handler code
        print "OnButton_CReportButton()"
#!XRCED:end-block:xrcCRelogioFrame.OnButton_CReportButton        

#!XRCED:begin-block:xrcCRelogioFrame.OnButton_ExitBtn
    def OnButton_ExitBtn(self, evt):
        # Replace with event handler code
        print "OnButton_ExitBtn()"
#!XRCED:end-block:xrcCRelogioFrame.OnButton_ExitBtn        

#!XRCED:begin-block:xrcCRelogioFrame.OnButton_ClearAllMarks
    def OnButton_ClearAllMarks(self, evt):
        # Replace with event handler code
        print "OnButton_ClearAllMarks()"
#!XRCED:end-block:xrcCRelogioFrame.OnButton_ClearAllMarks        

#!XRCED:begin-block:xrcCRelogioFrame.OnButton_AboutButton
    def OnButton_AboutButton(self, evt):
        # Replace with event handler code
        print "OnButton_AboutButton()"
#!XRCED:end-block:xrcCRelogioFrame.OnButton_AboutButton        

#!XRCED:begin-block:xrcCRelogioFrame.OnMaximize
    def OnMaximize(self, evt):
        # Replace with event handler code
        print "OnMaximize()"
#!XRCED:end-block:xrcCRelogioFrame.OnMaximize        


class xrcCMarkDlg(wx.Dialog):
#!XRCED:begin-block:xrcCMarkDlg.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcCMarkDlg.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "CMarkDlg")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.CRadio_Type = xrc.XRCCTRL(self, "CRadio_Type")
        self.CRadio_subType = xrc.XRCCTRL(self, "CRadio_subType")
        self.cTimeStamp = xrc.XRCCTRL(self, "cTimeStamp")
        self.wxTimeSliderHour = xrc.XRCCTRL(self, "wxTimeSliderHour")
        self.wxTimeSlider = xrc.XRCCTRL(self, "wxTimeSlider")
        self.wxTimeSliderSec = xrc.XRCCTRL(self, "wxTimeSliderSec")
        self.wxTimeSliderDay = xrc.XRCCTRL(self, "wxTimeSliderDay")
        self.wxTimeSliderMonth = xrc.XRCCTRL(self, "wxTimeSliderMonth")
        self.wxTimeSliderYear = xrc.XRCCTRL(self, "wxTimeSliderYear")
        self.CCommentTextCtrl = xrc.XRCCTRL(self, "CCommentTextCtrl")

        self.Bind(wx.EVT_RADIOBOX, self.OnRadiobox_CRadio_Type, self.CRadio_Type)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadiobox_CRadio_subType, self.CRadio_subType)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSliderHour, self.wxTimeSliderHour)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSlider, self.wxTimeSlider)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSliderSec, self.wxTimeSliderSec)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSliderDay, self.wxTimeSliderDay)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSliderMonth, self.wxTimeSliderMonth)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxTimeSliderYear, self.wxTimeSliderYear)
        self.Bind(wx.EVT_BUTTON, self.OnButton_CMarkBtn, id=xrc.XRCID('CMarkBtn'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_CCancelBtn, id=xrc.XRCID('CCancelBtn'))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

#!XRCED:begin-block:xrcCMarkDlg.OnRadiobox_CRadio_Type
    def OnRadiobox_CRadio_Type(self, evt):
        # Replace with event handler code
        print "OnRadiobox_CRadio_Type()"
#!XRCED:end-block:xrcCMarkDlg.OnRadiobox_CRadio_Type        

#!XRCED:begin-block:xrcCMarkDlg.OnRadiobox_CRadio_subType
    def OnRadiobox_CRadio_subType(self, evt):
        # Replace with event handler code
        print "OnRadiobox_CRadio_subType()"
#!XRCED:end-block:xrcCMarkDlg.OnRadiobox_CRadio_subType        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSliderHour
    def OnScroll_wxTimeSliderHour(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSliderHour()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSliderHour        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSlider
    def OnScroll_wxTimeSlider(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSlider()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSlider        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSliderSec
    def OnScroll_wxTimeSliderSec(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSliderSec()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSliderSec        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSliderDay
    def OnScroll_wxTimeSliderDay(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSliderDay()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSliderDay        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSliderMonth
    def OnScroll_wxTimeSliderMonth(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSliderMonth()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSliderMonth        

#!XRCED:begin-block:xrcCMarkDlg.OnScroll_wxTimeSliderYear
    def OnScroll_wxTimeSliderYear(self, evt):
        # Replace with event handler code
        print "OnScroll_wxTimeSliderYear()"
#!XRCED:end-block:xrcCMarkDlg.OnScroll_wxTimeSliderYear        

#!XRCED:begin-block:xrcCMarkDlg.OnButton_CMarkBtn
    def OnButton_CMarkBtn(self, evt):
        # Replace with event handler code
        print "OnButton_CMarkBtn()"
#!XRCED:end-block:xrcCMarkDlg.OnButton_CMarkBtn        

#!XRCED:begin-block:xrcCMarkDlg.OnButton_CCancelBtn
    def OnButton_CCancelBtn(self, evt):
        # Replace with event handler code
        print "OnButton_CCancelBtn()"
#!XRCED:end-block:xrcCMarkDlg.OnButton_CCancelBtn        

#!XRCED:begin-block:xrcCMarkDlg.OnClose
    def OnClose(self, evt):
        # Replace with event handler code
        print "OnClose()"
#!XRCED:end-block:xrcCMarkDlg.OnClose        


class xrcCReportFrame(wx.Frame):
#!XRCED:begin-block:xrcCReportFrame.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcCReportFrame.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreFrame()
        self.PreCreate(pre)
        get_resources().LoadOnFrame(pre, parent, "CReportFrame")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.CStartTimeText = xrc.XRCCTRL(self, "CStartTimeText")
        self.CStopTimeText = xrc.XRCCTRL(self, "CStopTimeText")
        self.CApplyButton = xrc.XRCCTRL(self, "CApplyButton")
        self.CReportListCtrl = xrc.XRCCTRL(self, "CReportListCtrl")
        self.cCHTotalText = xrc.XRCCTRL(self, "cCHTotalText")
        self.cHETotalText = xrc.XRCCTRL(self, "cHETotalText")
        self.cCPTotalText = xrc.XRCCTRL(self, "cCPTotalText")
        self.cBHToggleButton = xrc.XRCCTRL(self, "cBHToggleButton")
        self.cBHTotalText = xrc.XRCCTRL(self, "cBHTotalText")
        self.cSaldoText = xrc.XRCCTRL(self, "cSaldoText")
        self.cSaldoButton = xrc.XRCCTRL(self, "cSaldoButton")

        self.Bind(wx.EVT_BUTTON, self.OnButton_CApplyButton, self.CApplyButton)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnTogglebutton_cBHToggleButton, self.cBHToggleButton)
        self.Bind(wx.EVT_BUTTON, self.OnButton_cSaldoButton, self.cSaldoButton)

#!XRCED:begin-block:xrcCReportFrame.OnButton_CApplyButton
    def OnButton_CApplyButton(self, evt):
        # Replace with event handler code
        print "OnButton_CApplyButton()"
#!XRCED:end-block:xrcCReportFrame.OnButton_CApplyButton        

#!XRCED:begin-block:xrcCReportFrame.OnTogglebutton_cBHToggleButton
    def OnTogglebutton_cBHToggleButton(self, evt):
        # Replace with event handler code
        print "OnTogglebutton_cBHToggleButton()"
#!XRCED:end-block:xrcCReportFrame.OnTogglebutton_cBHToggleButton        

#!XRCED:begin-block:xrcCReportFrame.OnButton_cSaldoButton
    def OnButton_cSaldoButton(self, evt):
        # Replace with event handler code
        print "OnButton_cSaldoButton()"
#!XRCED:end-block:xrcCReportFrame.OnButton_cSaldoButton        




# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    __res.Load('GUI.xrc')
