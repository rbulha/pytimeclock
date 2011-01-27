import wx
import time

from BaseDefs import TypeNIcons as TNI
from RPConfig import CRPConfig

try:
    from agw import balloontip as BT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.balloontip as BT

class CBookMark(wx.Panel):
    def __init__(self, parent, i_id=wx.ID_ANY, pos=wx.DefaultPosition, mtype=0x10, subtype=0x01, name="marca", timestamp="00:00:00"):
        wx.Panel.__init__(self,parent,i_id,pos,(16,16),wx.TRANSPARENT_WINDOW ,name) #wx.TAB_TRAVERSAL
        #[mtype][subtype]
        self.icons = wx.Icon(TNI.ICON[mtype][subtype], wx.BITMAP_TYPE_ICO, desiredWidth=16, desiredHeight=16)  
        self.Position = pos    
        self.Bind(wx.EVT_PAINT, self.OnPaintBG)  
        #BIND mouse events
        '''
        if mtype == TNI.ENTRADA:
            message_tip = "Entrada: " + timestamp + "\n" + name
        elif mtype == TNI.SAIDA:
            message_tip = "Saida: " + timestamp + "\n" + name
        else:    
            message_tip = name + "\n" + timestamp
        
        '''      
        message_tip = name + "\n" + timestamp
            
        self.Bind(wx.EVT_MOTION,self.OnMouseMotion) 
        tipballoon = BT.BalloonTip(topicon=None, toptitle='',
                                   message=message_tip, shape=BT.BT_ROUNDED,
                                   tipstyle=BT.BT_LEAVE)
        # Set The Target
        tipballoon.SetTarget(self)
        tipballoon.SetEndDelay(2000)
                     
    def OnMouseMotion(self, event):
        pass
        #print 'sobre (%d,%d)'%(event.GetX(),event.GetY())                     
    def DrawMark(self, dc):
        dc.DrawIcon(self.icons, 0,0)#-8, -8)
    def OnPaintBG(self,event):
        dc = wx.PaintDC(self)
        #dc.SetBackground(wx.LIGHT_GREY_BRUSH)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        #dc.Clear()
        self.DrawMark(dc)
        
class CColoredGauge(wx.Panel):
    def __init__(self, parent, callback):
        wx.Panel.__init__(self,parent,wx.ID_ANY,wx.DefaultPosition,parent.GetSize(),wx.TAB_TRAVERSAL,'cplored gauge')
        self.parent = parent
        self.callback = callback
        self.entrada_padrao = None
        self.saida_padrao   = None
        #BookMark collection
        self.BookMarkCollection = []
        
        self.ResizeConstraints(self.GetSize())
        #Repaint event
        self.Bind(wx.EVT_PAINT , self.OnEraseBG)
        #BIND mouse events
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)  
        #Size event
        self.Bind(wx.EVT_SIZE, self.OnSize) 

    def DeleteAllBookMarks(self):
        for bm in self.BookMarkCollection:
            print '[CColoredGauge.DeleteAllBookMarks]destroy: ',bm.Destroy()
        self.BookMarkCollection = []    
    def ResizeConstraints(self, size):
        self.Value = size.GetWidth() / 2
        self.CenterY = size.GetHeight() / 2
        self.Yoffset = size.GetHeight() * 0.1
        self.Xoffset = size.GetWidth() * 0.03
        self.XbarDist = (size.GetWidth() - (self.Xoffset*2)) / 24
        print '[CColoredGauge.ResizeConstraints] XbarDist: ',self.XbarDist
        self.IconCenterOff = 16 / 2
        '''#--- basic marks (dummy mark only visual)
        if self.entrada_padrao and self.saida_padrao:
            Xoffset_g = self.Xoffset+(7*self.XbarDist)
            Xoffset_icon = Xoffset_g - self.IconCenterOff        
            self.entrada_padrao.MoveXY(Xoffset_icon,self.CenterY+21)
            Xoffset_g = self.Xoffset+(11.6*self.XbarDist)
            Xoffset_icon = Xoffset_g - self.IconCenterOff        
            self.lunch_padrao.MoveXY(Xoffset_icon,self.CenterY+21)            
            Xoffset_g = self.Xoffset+(17*self.XbarDist)+(30*(self.XbarDist/60))
            Xoffset_icon = Xoffset_g - self.IconCenterOff        
            self.saida_padrao.MoveXY(Xoffset_icon,self.CenterY+21)
        #-------------
        
        '''
        self.RefreshMark()
    
    def OnSize(self,event):
        self.SetSize(event.GetSize())
        print '[CColoredGauge.OnSize] event.GetSize: ',event.GetSize()
        self.ResizeConstraints(event.GetSize())
        self.Refresh()
    def analysetoday(self):
        today = self.callback()
        nowtime = time.localtime()
        today_marks = {}
        today_marks['now'] = float(nowtime[3] + float(nowtime[4])/60.0)
        today_marks['extra_out'] = []
        today_marks['extra_in'] = []  
        for entry in today:
            if entry[3] == 0x11:
                today_marks['start'] = float(entry[0] + float(entry[1])/60.0)
            elif entry[3] == 0x22:
                today_marks['lunch_start'] = float(entry[0] + float(entry[1])/60.0)
            elif entry[3] == 0x12:
                today_marks['lunch_end'] = float(entry[0] + float(entry[1])/60.0)
            elif entry[3] == 0x13:
                today_marks['extra_in'].append(float(entry[0] + float(entry[1])/60.0))
            elif entry[3] == 0x23:
                today_marks['extra_out'].append(float(entry[0] + float(entry[1])/60.0))
        return today_marks        
    def DrawCalendar(self,x,y,w,h,dc):
        dc.SetPen(wx.Pen(wx.BLACK,2))
        dc.SetBrush(wx.Brush(wx.Colour(220,220,220),wx.SOLID))
        dc.DrawRoundedRectangle(x,y,w,h,5)
        calendar = wx.Icon(TNI.ICON[TNI.MISC][TNI.CALEND], wx.BITMAP_TYPE_ICO, desiredWidth=16, desiredHeight=16)
        dc.DrawIcon(calendar, x+10,y+5)
        out_data = time.strftime("%d/%m/%Y - %H:%M:%S",time.localtime()) 
        dc.DrawText(out_data,x+30,y+5.5)
    def OnEraseBG(self,event):
        today = self.analysetoday()
        print '[CColoredGauge.OnEraseBG] marks: ',today   
        #dc = event.GetDC()
        screen_dc = wx.PaintDC(self)
        #screen_dc.Clear()
        
        dc = wx.MemoryDC(wx.EmptyBitmap(self.GetSize().GetWidth(),self.GetSize().GetHeight(),-1))

        dc.SetBackground(wx.LIGHT_GREY_BRUSH)
        dc.Clear()
        rainbow = wx.Pen(wx.RED,2)
        daylong = wx.Pen(wx.BLUE,2)
        
        self.DrawCalendar(5, 5, self.GetSize().GetWidth()-10, 25, dc)
        
        tempo = 0.0
        for hora in range(0,24):
            #hora_list = [item for item in mark_list if item[0]==hora]
            for mint in range(0,60,10): #10 in 10 minutes
                #Xoffset_g = self.Xoffset+hora*5+mint
                tempo = float(hora + float(mint)/60.0)
                '''
                min_list = [item for item in hora_list if item[1]>=mint and item[1]<(mint+10)]
                for item in min_list:
                    tipo = item[3] & 0xF0
                    sub  = item[3] & 0x0F
                    Xoffset_g = self.Xoffset+(hora*self.XbarDist)+(item[1]*(self.XbarDist/60))
                    Xoffset_icon = Xoffset_g - self.IconCenterOff
                    dc.DrawIcon(wx.Icon(TNI.ICON[tipo][sub], wx.BITMAP_TYPE_ICO), Xoffset_icon,self.CenterY-40)
                '''
                Xoffset_g = self.Xoffset+(hora*self.XbarDist)+(mint*(self.XbarDist/60))
            
                if tempo >= CRPConfig.H_E_OFICIAL and tempo <= CRPConfig.H_S_OFICIAL:
                    if tempo >= CRPConfig.H_S_ALMOCO and tempo <= CRPConfig.H_E_ALMOCO:
                        rainbow.SetColour((150,150,150,255))
                    else:
                        rainbow.SetColour((255-((tempo-7)*20),(tempo-7)*4,(tempo-7)*20,255))
                elif tempo < CRPConfig.H_E_OFICIAL:
                    rainbow.SetColour((15*tempo+50,15*tempo+50,15*tempo+50,255))
                else:
                    #rainbow.SetColour((255-(15*tempo)+50),255-(15*tempo)+50,(255-(15*tempo)+50,255))  
                    rainbow.SetColour((150,150,150,255))
                #desenha linhas temporais em degrade  
                daylong.SetColour((150,150,150,255))
                if today.has_key('start'): 
                    if tempo > today['start'] and tempo < today['now']: 
                        if today.has_key('lunch_start') and \
                        today.has_key('lunch_end')   and \
                        tempo > today['lunch_start'] and \
                        tempo < today['lunch_end']:
                            daylong.SetColour((160,160,160,255))
                        else: 
                            out_of_office = False
                            for extra_in,extra_out in enumerate(today['extra_out']):
                                if tempo > extra_out and extra_in < len(today['extra_in']):
                                    if tempo < today['extra_in'][extra_in]:
                                        out_of_office = True
                            if out_of_office:
                                daylong.SetColour((150,150,150,255))
                            else:                
                                delay = today['start']#CRPConfig.H_E_OFICIAL - today['start']     
                                daylong.SetColour((255-((tempo-delay)*20), \
                                                  (tempo-delay)*4, \
                                                  (tempo-delay)*20,255))#daylong.SetColour((0,0,255,255))
                    else: 
                        daylong.SetColour((150,150,150,255))
                dc.SetPen(rainbow)
                dc.DrawLine(Xoffset_g,self.Yoffset+self.CenterY+2,Xoffset_g,self.Yoffset+self.CenterY+20)
                dc.SetPen(daylong)
                dc.DrawLine(Xoffset_g,self.Yoffset+self.CenterY-15,Xoffset_g,self.Yoffset+self.CenterY)
        
        screen_dc.Blit(0,0,self.GetSize().GetWidth(),self.GetSize().GetHeight(),dc,0,0,wx.COPY)        
        #event.Skip()
    def RefreshMark(self):
        mark_list = self.callback() 
        self.DeleteAllBookMarks()
        self.Refresh()
        self.AddDefaultMarks()
        for hora in range(24):
            hora_list = [item for item in mark_list if item[0]==hora]
            for mint in range(0,60,10): #10 in 10 minutes
                min_list = [item for item in hora_list if item[1]>=mint and item[1]<(mint+10)]
                for item in min_list:
                    tipo = item[3] & 0xF0
                    sub  = item[3] & 0x0F
                    Xoffset_g = self.Xoffset+(hora*self.XbarDist)+(item[1]*(self.XbarDist/60))
                    Xoffset_icon = Xoffset_g - self.IconCenterOff
                    #dc.DrawIcon(wx.Icon(TNI.ICON[tipo][sub], wx.BITMAP_TYPE_ICO), Xoffset_icon,self.CenterY-40)
                    timestamp = "%d:%d:%d"%(item[0],item[1],item[2])
                    self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, (Xoffset_icon,self.Yoffset+self.CenterY-32), tipo, sub, item[4],timestamp))
                    
    def AddDefaultMarks(self):
        nowtime = time.localtime()
        Xoffset_g = self.Xoffset+10
        Xoffset_icon = Xoffset_g - self.IconCenterOff        
        self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, \
                                                 (Xoffset_icon,self.Yoffset+self.CenterY+4), \
                                                 TNI.MISC, \
                                                 TNI.QUESTION, \
                                                 "Perfect Day",\
                                                 "full journey for reference"))
        self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, \
                                                 (Xoffset_icon,self.Yoffset+self.CenterY-14), \
                                                 TNI.MISC, TNI.QUESTION, \
                                                 "Your Day",\
                                                 "Survey in real-time you journey"))
        Xoffset_icon = self.Xoffset + (CRPConfig.H_E_OFICIAL*self.XbarDist) - self.IconCenterOff 
        self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, \
                                                 (Xoffset_icon,self.Yoffset+self.CenterY+21), \
                                                 TNI.ENTRADA, TNI.PADRAO, \
                                                 "Start","07:00:00"))
        Xoffset_icon = self.Xoffset + (CRPConfig.H_S_ALMOCO*self.XbarDist) - self.IconCenterOff
        self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, \
                                                 (Xoffset_icon,self.Yoffset+self.CenterY+21), \
                                                 TNI.MISC, TNI.LUNCH, \
                                                 "Lunch","11:36:00")) 
        if nowtime.tm_wday == 4: #Sexta-feira
            time_stamp = "16:00:00"
            Xoffset_icon = self.Xoffset + (CRPConfig.H_S_OFICIAL_SEXTA*self.XbarDist) - self.IconCenterOff
        else:   
            time_stamp = "17:30:00"           
            Xoffset_icon = self.Xoffset + (CRPConfig.H_S_OFICIAL*self.XbarDist) - self.IconCenterOff        
        self.BookMarkCollection.append(CBookMark(self, wx.ID_ANY, \
                                                 (Xoffset_icon,self.Yoffset+self.CenterY+21), \
                                                 TNI.SAIDA, TNI.PADRAO, \
                                                 "Out",time_stamp))
        #-------------

    def OnMouseMotion(self, event):
        pass
        #print 'movi (%d,%d)'%(event.GetX(),event.GetY())     
        
