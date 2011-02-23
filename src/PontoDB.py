# -*- coding: UTF-8 -*-
import time
import shelve
import dbhash #incluidos apenas para que o instalador encontre os requisitos
import anydbm #incluidos apenas para que o instalador encontre os requisitos
import sys
import os

class CPontoDB:
    def __init__(self):
        sys_path = sys.path[0]
        if os.path.splitext(sys_path)[1] == '':
            base = sys.path[0]
        else:
            base = os.path.dirname(sys.path[0])  
            
        self.DB_BASE_PATH = os.path.dirname(base) + '\\data\\'    
        print '[CPontoDB.__init__] base path: ',os.path.dirname(base)
        
        self.cSubType = {}
        self.cSubType['NORMAL']         = 0x01
        self.cSubType['ALMOCO']         = 0x02
        self.cSubType['EXTRAORDINARIA'] = 0x03
        
        self.cTypes = {}
        self.cTypes['ENTRADA']          = 0x10
        self.cTypes['SAIDA']            = 0x20
          
    def LoadDB(self):
        caminho = self.DB_BASE_PATH + 'meu-ponto.dat'
        print '[CPontoDB.LoadDB] caminho: ',caminho
        self.DB = shelve.open(caminho)
    def Populate(self):
        today = time.localtime()
        self.TimeMark(today,'Saida extraordinaria',self.cTypes['SAIDA']|self.cSubType['EXTRAORDINARIA'])
    def TimeMark(self,timestamp=None,comentario='sem com.',tipo='ENTRADA',subtipo='NORMAL'): 
        if self.cTypes.has_key(tipo) and self.cSubType.has_key(subtipo):
            self.Mark(timestamp,comentario,self.cTypes[tipo]|self.cSubType[subtipo])
    def Mark(self,timestamp,comentario,tipo):
        if timestamp == None:
            timestamp = time.localtime()
        self.DB[time.strftime("%Y:%m:%d:%H:%M:%S",time.localtime())]={'time':timestamp, 'comentario':comentario,'tipo':tipo}
        self.DB.sync()
    def Print(self):
        for key in self.DB: 
            print key, ' =>'
            print '    Tipo.......: 0x%Xh'%self.DB[key]['tipo']
            print '    Comentario.: %s'%self.DB[key]['comentario'] 
            print '    Hora.......: %s'%time.strftime("%H:%M",self.DB[key]['time'])
            #print '    Dado cru...: ', self.DB[key] @IndentOk
    def has_mark_today(self,timestamp=None,comentario='sem com.',tipo='ENTRADA',subtipo='NORMAL'):
        today = time.localtime()
        for mark in self.DB:
            if self.DB[mark]['time'].tm_year == today.tm_year and \
            self.DB[mark]['time'].tm_mon == today.tm_mon  and \
            self.DB[mark]['time'].tm_mday == today.tm_mday and \
            subtipo != 'EXTRAORDINARIA' and \
            self.DB[mark]['tipo'] == self.cTypes[tipo]|self.cSubType[subtipo]:
                return self.DB[mark]
        return None   
    def has_mark_anywhere(self,timestamp=None,comentario='sem com.',tipo='ENTRADA',subtipo='NORMAL'):
        if timestamp != None:
            for mark in self.DB:
                if self.DB[mark]['time'].tm_year == timestamp.tm_year and \
                self.DB[mark]['time'].tm_mon == timestamp.tm_mon  and \
                self.DB[mark]['time'].tm_mday == timestamp.tm_mday and \
                subtipo != 'EXTRAORDINARIA' and \
                self.DB[mark]['tipo'] == self.cTypes[tipo]|self.cSubType[subtipo]:
                    return self.DB[mark]
                elif self.DB[mark]['time'].tm_year == timestamp.tm_year and \
                self.DB[mark]['time'].tm_mon == timestamp.tm_mon  and \
                self.DB[mark]['time'].tm_mday == timestamp.tm_mday and \
                self.DB[mark]['time'].tm_hour == timestamp.tm_hour and \
                self.DB[mark]['time'].tm_min == timestamp.tm_min and \
                subtipo == 'EXTRAORDINARIA' and \
                self.DB[mark]['tipo'] == self.cTypes[tipo]|self.cSubType[subtipo]:
                    return self.DB[mark]
            return None
        else:
            return None   
    def DeleteMark(self,target_mark): 
        for mark in self.DB:
            if self.DB[mark]['time'] == target_mark['time'] and \
               self.DB[mark]['tipo'] == target_mark['tipo']  :
                del self.DB[mark]
                self.DB.sync()
    def ClearToday(self):
        today = time.localtime()
        for mark in self.DB:
            if  self.DB[mark]['time'].tm_year == today.tm_year and \
                self.DB[mark]['time'].tm_mon == today.tm_mon  and \
                self.DB[mark]['time'].tm_mday == today.tm_mday :
                    del self.DB[mark]
        self.DB.sync()            
        return True      
    def GetToday(self):
        today = time.localtime()
        today_list = []
        for mark in self.DB:
            if  self.DB[mark]['time'].tm_year == today.tm_year and \
                self.DB[mark]['time'].tm_mon  == today.tm_mon  and \
                self.DB[mark]['time'].tm_mday == today.tm_mday :
                    mark_temp = (self.DB[mark]['time'].tm_hour, \
                                 self.DB[mark]['time'].tm_min,  \
                                 self.DB[mark]['time'].tm_sec,  \
                                 self.DB[mark]['tipo'],         \
                                 self.DB[mark]['comentario'])
                    today_list.append(mark_temp)
        return today_list            
    def GetDate(self,day):
        #today = time.localtime()
        today = time.strptime(day,"%d/%m/%Y")
        today_list = []
        for mark in self.DB:
            if  self.DB[mark]['time'].tm_year == today.tm_year and \
                self.DB[mark]['time'].tm_mon  == today.tm_mon  and \
                self.DB[mark]['time'].tm_mday == today.tm_mday :
                    mark_temp = (self.DB[mark]['time'].tm_hour, \
                                 self.DB[mark]['time'].tm_min,  \
                                 self.DB[mark]['time'].tm_sec,  \
                                 self.DB[mark]['tipo'],         \
                                 self.DB[mark]['comentario'])
                    today_list.append(mark_temp)
        return today_list            
                    
if __name__ == '__main__':
    cPontoDB = CPontoDB()
    cPontoDB.LoadDB()
    cPontoDB.Populate()
    cPontoDB.Print()
