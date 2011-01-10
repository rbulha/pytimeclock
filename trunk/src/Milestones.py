import wx
import time

from BaseDefs import TypeNIcons as TNI
from RPConfig import CRPConfig

'''try:
    from agw import balloontip as BT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.balloontip as BT

'''
class CMilestone(wx.Panel):
    def __init__(self, parent, i_id=wx.ID_ANY, pos=wx.DefaultPosition, mtype=0x10, subtype=0x01, name="marca", timestamp="00:00:00"):
        wx.Panel.__init__(self,parent,i_id,pos,(206,16),wx.TRANSPARENT_WINDOW ,name) #wx.TAB_TRAVERSAL
        self.icons = wx.Icon(TNI.ICON[mtype][subtype], wx.BITMAP_TYPE_ICO, desiredWidth=16, desiredHeight=16)  
        self.Position = pos    
        self.Bind(wx.EVT_PAINT, self.OnPaintBG)  
        #BIND mouse events
        if mtype == TNI.ENTRADA:
            self.message_tip = name + ": " + timestamp
        else:   
            self.message_tip = name + ": " + timestamp
            
        self.Bind(wx.EVT_MOTION,self.OnMouseMotion) 
        '''tipballoon = BT.BalloonTip(topicon=None, toptitle='',
                                   message=self.message_tip, shape=BT.BT_ROUNDED,
                                   tipstyle=BT.BT_LEAVE)
        # Set The Target
        tipballoon.SetTarget(self)
                                   
        '''                           
                     
    def OnMouseMotion(self, event):
        pass
        #print 'sobre (%d,%d)'%(event.GetX(),event.GetY())                     
    def DrawMark(self, dc):
        dc.SetTextForeground(wx.BLACK)
        dc.DrawIcon(self.icons, 0,0)#-8, -8)
        dc.DrawText(self.message_tip,20,0)
        #print 'Milestone.DrawMark: ',self.message_tip
    def OnPaintBG(self,event):
        dc = wx.PaintDC(self)
        #dc.SetBackground(wx.LIGHT_GREY_BRUSH)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        #dc.Clear()
        self.DrawMark(dc)
        
        
class CMilestonePanel(wx.Panel):
    def __init__(self, parent, callback):
        wx.Panel.__init__(self,parent,wx.ID_ANY,wx.DefaultPosition,(-1,-1),wx.TAB_TRAVERSAL,'cplored gauge')
        self.parent = parent
        self.callback = callback
        
        self.entrada_padrao = None
        self.saida_padrao   = None
        #BookMark collection
        self.MilestoneCollection = []

        self.mark_grid = []

        self.ResizeConstraints(self.GetSize())
        
        #Repaint event
        self.Bind(wx.EVT_PAINT , self.OnEraseBG)
        #BIND mouse events
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)  
        #Size event
        self.Bind(wx.EVT_SIZE, self.OnSize) 
        
        '''--- basic marks (dummy mark only visual)
        #teste
        Xoffset_g = 30
        Xoffset_icon = Xoffset_g - self.IconCenterOff 
        Yoffset_g = 10       
        self.MilestoneCollection.append(CMilestone(self, wx.ID_ANY, (Xoffset_icon,Yoffset_g), TNI.S_W, TNI.R2D2, "Entrada","07:00:00"))
        Yoffset_g = Yoffset_g + 3*self.IconCenterOff      
        self.MilestoneCollection.append(CMilestone(self, wx.ID_ANY, (Xoffset_icon,Yoffset_g), TNI.MISC, TNI.LUNCH, "Almoco","11:36:00"))
        Yoffset_g = Yoffset_g + 3*self.IconCenterOff      
        self.MilestoneCollection.append(CMilestone(self, wx.ID_ANY, (Xoffset_icon,Yoffset_g), TNI.S_W, TNI.DVADER, "Saida","17:36:00"))

        Xoffset_g = self.Xoffset+(7*self.XbarDist)
        Xoffset_icon = Xoffset_g - self.IconCenterOff        
        self.entrada_padrao = CBookMark(self, wx.ID_ANY, (Xoffset_icon,self.CenterY+21), TNI.ENTRADA, TNI.PADRAO, "Entrada padrao","07:00:00")

        Xoffset_g = self.Xoffset+(11.6*self.XbarDist)
        Xoffset_icon = Xoffset_g - self.IconCenterOff        
        self.lunch_padrao = CBookMark(self, wx.ID_ANY, (Xoffset_icon,self.CenterY+21), TNI.MISC, TNI.LUNCH, "Almoco padrao","11:36:00")        

        Xoffset_g = self.Xoffset+(17*self.XbarDist)+(30*(self.XbarDist/60))
        Xoffset_icon = Xoffset_g - self.IconCenterOff        
        self.saida_padrao   = CBookMark(self, wx.ID_ANY, (Xoffset_icon,self.CenterY+21), TNI.SAIDA, TNI.PADRAO, "Saida padrao","17:36:00")
        #-------------
        
        '''
    def get_xy_offset(self):
        for i,mark in enumerate(self.mark_grid):
            if not mark[2]:
                self.mark_grid[i][2] = 1
                return (mark[0],mark[1])  
                
    def reset_xy_offset(self):        
        for i in range(len(self.mark_grid)):
            self.mark_grid[i][2] = 0
                    
    def AnalyseToday(self):
        today = self.callback()
        print "[Milestone.AnalyseToday]: ",today
        saida_almoco = 0.0
        entrada_almoco = 0.0   
        extra_out = 0.0
        extra_in = 0.0   
        out_of_office = 0.0  
        tempo_lunch = 0.0
        start_time = 0.0
        end_time   = 0.0
        journey_time = 0.0
        remain_time = 0.0
        estimated_time = 0.0
        for entry in today:
            if entry[3] == 0x11:
                offset = self.get_xy_offset() 
                start_time = entry[2] + 60*entry[1] + 3600*entry[0]      
                self.MilestoneCollection.append(\
                                                CMilestone(self, \
                                                           wx.ID_ANY, \
                                                           offset, \
                                                           TNI.ENTRADA, \
                                                           TNI.PADRAO, \
                                                           "Day start", \
                                                           "%02d:%02d:%02d"%(entry[0],entry[1],entry[2])))
            elif entry[3] == 0x21:
                end_time = entry[2] + 60*entry[1] + 3600*entry[0]    
            elif entry[3] == 0x22:
                saida_almoco = entry[2] + 60*entry[1] + 3600*entry[0]    
            elif entry[3] == 0x12:
                entrada_almoco = entry[2] + 60*entry[1] + 3600*entry[0] 
            elif entry[3] == 0x23:
                extra_out = entry[2] + 60*entry[1] + 3600*entry[0]
            elif entry[3] == 0x13:
                if extra_out != 0:
                    extra_in = entry[2] + 60*entry[1] + 3600*entry[0]
                    out_of_office = out_of_office + (extra_in - extra_out)
                    extra_out = 0.0
                    extra_in = 0.0   
        
        if start_time != 0.0 and end_time != 0.0:
            journey_time = end_time - start_time
        elif start_time != 0.0:
            now_time = time.localtime()[3]*3600 + time.localtime()[4]*60 + time.localtime()[5]
            journey_time = now_time - start_time        
                                   
        if (entrada_almoco - saida_almoco) > 0:
            offset = self.get_xy_offset()
            tempo_lunch = entrada_almoco - saida_almoco 
            if journey_time > 0 and journey_time > tempo_lunch:
                journey_time = journey_time - tempo_lunch
            if tempo_lunch < 3600:    
                self.MilestoneCollection.append(\
                                                CMilestone(self, \
                                                           wx.ID_ANY, \
                                                           offset, \
                                                           TNI.MISC, \
                                                           TNI.LUNCH, \
                                                           "Lunch time", \
                                                           "%0.2f min"%(tempo_lunch/60)))
            else:
                self.MilestoneCollection.append(\
                                                CMilestone(self, \
                                                           wx.ID_ANY, \
                                                           offset, \
                                                           TNI.MISC, \
                                                           TNI.LUNCH, \
                                                           "Lunch time", \
                                                           "%02d:%02d h"%(tempo_lunch/3600,(journey_time%3600.0)/60)))
                
        if out_of_office > 0:
            offset = self.get_xy_offset()
            if journey_time > 0 and journey_time > out_of_office:
                journey_time = journey_time - out_of_office
            
            self.MilestoneCollection.append(\
                                            CMilestone(self, \
                                                       wx.ID_ANY, \
                                                       offset, \
                                                       TNI.MISC, \
                                                       TNI.EXTRA, \
                                                       "Out of the office", \
                                                       "%0.2f min"%(out_of_office/60)))                        
        if journey_time > 0:
            if journey_time < 3600:
                output_text = "%0.2f min"%(float(journey_time)/60.0)
            else:
                o_hora = journey_time/3600.0
                o_min  = (journey_time%3600.0)/60
                output_text = "%02d:%02d h"%(o_hora,o_min)
                
            offset = self.get_xy_offset()
            self.MilestoneCollection.append(\
                                            CMilestone(self, \
                                                       wx.ID_ANY, \
                                                       offset, \
                                                       TNI.MISC, \
                                                       TNI.CLOCK, \
                                                       "Journey", \
                                                       output_text )) 
            if journey_time < CRPConfig.GetJorneyInSeconds():
                remain_time = CRPConfig.GetJorneyInSeconds() -  journey_time
                offset = self.get_xy_offset()
                o_hora = remain_time/3600.0
                o_min  = (remain_time%3600.0)/60
                output_text = "%02d:%02d h"%(o_hora,o_min)                
                self.MilestoneCollection.append(\
                                                CMilestone(self, \
                                                           wx.ID_ANY, \
                                                           offset, \
                                                           TNI.MISC, \
                                                           TNI.CLOCK, \
                                                           "Remain", \
                                                           output_text ))  
                #estimated out time
                if tempo_lunch > 0:
                    estimated_time = start_time + journey_time + remain_time + tempo_lunch
                else:
                    estimated_time = start_time + journey_time + remain_time + 5400
                        
                offset = self.get_xy_offset()
                o_hora = estimated_time/3600.0
                o_min  = (estimated_time%3600.0)/60
                output_text = "%02d:%02d h"%(o_hora,o_min)                
                self.MilestoneCollection.append(\
                                                CMilestone(self, \
                                                           wx.ID_ANY, \
                                                           offset, \
                                                           TNI.SAIDA, \
                                                           TNI.NORMAL, \
                                                           "Estimated", \
                                                           output_text ))                              
            else:                                            
                remain_time = 0  

    def DeleteAll(self):
        for bm in self.MilestoneCollection:
            print '[CColoredGauge.DeleteAllBookMarks]destroy: ',bm.Destroy()
        self.MilestoneCollection = []  
        self.reset_xy_offset()  
    def ResizeConstraints(self, size):
        self.CenterX = size.GetWidth() / 2
        self.CenterY = size.GetHeight() / 2
        self.Xoffset = size.GetWidth() * 0.03
        self.XbarDist = (size.GetWidth() - (self.Xoffset*2)) / 24
        print '[CColoredGauge.ResizeConstraints] XbarDist: ',self.XbarDist
        self.IconCenterOff = 16 / 2
        
        self.mark_grid = [[10,10,0],[10,30,0],[10,50,0],[10,70,0], \
                          [self.CenterX,10,0],[self.CenterX,30,0],[self.CenterX,50,0],[self.CenterX,70,0]]        
        
        self.RefreshMark()
    
    def OnSize(self,event):
        self.SetSize(event.GetSize())
        print '[CColoredGauge.OnSize] event.GetSize: ',event.GetSize()
        self.ResizeConstraints(event.GetSize())
        self.Refresh()
                     
    def OnEraseBG(self,event):
        #dc = event.GetDC()
        screen_dc = wx.PaintDC(self)
        #self.RefreshMark()
        dc = wx.MemoryDC(wx.EmptyBitmap(self.GetSize().GetWidth(),self.GetSize().GetHeight(),-1))
        dc.SetBackground(wx.LIGHT_GREY_BRUSH) 
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK,2))
        dc.SetBrush(wx.Brush(wx.Colour(220,220,220),wx.SOLID))
        dc.DrawRoundedRectangle(5,5,self.GetSize().GetWidth()-10,self.GetSize().GetHeight()-10,5)
        screen_dc.Blit(0,0,self.GetSize().GetWidth(),self.GetSize().GetHeight(),dc,0,0,wx.COPY)        
    def RefreshMark(self):
        self.DeleteAll()
        self.AnalyseToday()
    def OnMouseMotion(self, event):
        pass
        #print 'movi (%d,%d)'%(event.GetX(),event.GetY())     
        
