'''
Created on 04/02/2011

@author: rogerio_bulha
'''
import time

from GUI_xrc import xrcCMarkDlg

class CDialogMark(xrcCMarkDlg):
    def __init__(self,parent,time_stamp_tuple=None,mark_type=None):
        xrcCMarkDlg.__init__(self, parent)
        if time_stamp_tuple == None:
            time_stamp = time.localtime()
        else:
            time_stamp = time_stamp_tuple    
        self.cTimeStamp.SetValue(time.strftime("%H:%M:%S %d/%m/%Y",time_stamp))
        self.wxTimeSliderHour.SetValue(time_stamp.tm_hour)
        self.SpinHour.SetValue(time_stamp.tm_hour)
        self.wxTimeSlider.SetValue(time_stamp.tm_min)
        self.SpinMin.SetValue(time_stamp.tm_min)
        self.wxTimeSliderSec.SetValue(time_stamp.tm_sec)
        self.SpinSec.SetValue(time_stamp.tm_sec)
        self.wxTimeSliderDay.SetValue(time_stamp.tm_mday)
        self.SpinDay.SetValue(time_stamp.tm_mday)
        self.wxTimeSliderMonth.SetValue(time_stamp.tm_mon)
        self.SpinMonth.SetValue(time_stamp.tm_mon)
        self.wxTimeSliderYear.SetValue(time_stamp.tm_year)
        self.SpinYear.SetValue(time_stamp.tm_year)
        self.wxTimeSliderYear.SetRange(time_stamp.tm_year-50,time_stamp.tm_year+50)
        
        if mark_type != None:
            print '[CDialogMark] mark_type=%X'%(mark_type)
            print '[CDialogMark] mark_type=%X'%((mark_type&0xF0)>>4)
            print '[CDialogMark] mark_type=%X'%((mark_type&0x0F))
            self.CRadio_Type.SetSelection(((mark_type&0xF0)>>4)-1)
            self.CRadio_subType.SetSelection(((mark_type&0x0F))-1)
            
        
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
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y") 
        except ValueError:
            time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time.localtime())
            
        return (tipo[self.CRadio_Type.GetSelection()],   \
                sub[self.CRadio_subType.GetSelection()], \
                self.CCommentTextCtrl.GetValue(),        \
                time_stamp)
    def OnScroll_wxTimeSlider(self, evt):
        #print '[CDialogMark][OnScroll_wxTimeSlider] - evt: ',evt.GetPosition()  
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
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
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinMin.SetValue(evt.GetPosition()) 
    def OnScroll_wxTimeSliderHour(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          evt.GetPosition(),
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinHour.SetValue(evt.GetPosition())        
    def OnScroll_wxTimeSliderSec(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          evt.GetPosition(),
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinSec.SetValue(evt.GetPosition())      
    def OnScroll_wxTimeSliderDay(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          evt.GetPosition(),
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinDay.SetValue(evt.GetPosition())        
    def OnScroll_wxTimeSliderMonth(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          evt.GetPosition(),
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinMonth.SetValue(evt.GetPosition())        
    def OnScroll_wxTimeSliderYear(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (evt.GetPosition(),
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.SpinYear.SetValue(evt.GetPosition())
    def OnSpin_SpinHour(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          evt.GetPosition(),
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSliderHour.SetValue(evt.GetPosition())
    def OnSpin_SpinMin(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          evt.GetPosition(),
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSlider.SetValue(evt.GetPosition())
    def OnSpin_SpinSec(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          evt.GetPosition(),
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSliderSec.SetValue(evt.GetPosition())      
    def OnSpin_SpinDay(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          time_stamp.tm_mon,
                          evt.GetPosition(),
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSliderDay.SetValue(evt.GetPosition())        
    def OnSpin_SpinMonth(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (time_stamp.tm_year,
                          evt.GetPosition(),
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSliderMonth.SetValue(evt.GetPosition())        
    def OnSpin_SpinYear(self, evt):
        try:
            time_stamp = time.strptime(self.cTimeStamp.GetValue(),"%H:%M:%S %d/%m/%Y")
        except ValueError:    
            time_stamp = time.localtime()
        time_stamp_aux = (evt.GetPosition(),
                          time_stamp.tm_mon,
                          time_stamp.tm_mday,
                          time_stamp.tm_hour,
                          time_stamp.tm_min,
                          time_stamp.tm_sec,
                          time_stamp.tm_wday,
                          time_stamp.tm_yday,
                          time_stamp.tm_isdst)
        try:
            new_time_stamp = time.strftime("%H:%M:%S %d/%m/%Y",time_stamp_aux)
            self.cTimeStamp.SetValue(new_time_stamp)
        except ValueError:    
            self.cTimeStamp.SetValue(time_stamp)
        self.wxTimeSliderYear.SetValue(evt.GetPosition())

                       
        
                       
        
        