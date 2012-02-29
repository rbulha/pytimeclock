import sys
import os
import time
import shelve
import dbhash #incluidos apenas para que o instalador encontre os requisitos
import anydbm #incluidos apenas para que o instalador encontre os requisitos


CONFIGURATION_FILE = 'configuration4.dat'

class CRPConfig:
    global CONFIGURATION_FILE
    print '[CRPConfig] LOAD CONFIGURATION'
    sys_path = sys.path[0]
    if os.path.splitext(sys_path)[1] == '':
        base = sys.path[0]
    else:
        base = os.path.dirname(sys.path[0])  
        
    DB_BASE_PATH = os.path.dirname(base) + '\\data\\'     
    caminho = DB_BASE_PATH + CONFIGURATION_FILE
    DB = shelve.open(caminho)
    print '[CRPConfig] DB=',len(DB)
    if (len(DB) != 0) and DB.has_key('C_H_NORMAL') and DB.has_key('H_E_ALMOCO'):
        C_H_NORMAL    = DB['C_H_NORMAL']
        C_H_SEXTA     = DB['C_H_SEXTA']
        T_ALMOCO      = DB['T_ALMOCO']
        H_E_OFICIAL   = DB['H_E_OFICIAL']
        H_S_OFICIAL         = DB['H_S_OFICIAL']
        H_S_OFICIAL_SEXTA   = DB['H_S_OFICIAL_SEXTA']     
        H_S_ALMOCO          = DB['H_S_ALMOCO']
        H_E_ALMOCO          = DB['H_E_ALMOCO']
        START_REPORT_DAY    = DB['START_REPORT_DAY']
    else:    
        H_E_OFICIAL   = 7.5
        DB['H_E_OFICIAL']=H_E_OFICIAL
        H_S_OFICIAL   = 18.0
        DB['H_S_OFICIAL']=H_S_OFICIAL
        T_ALMOCO      = 1.4
        DB['T_ALMOCO']=T_ALMOCO
        H_S_OFICIAL_SEXTA = 16.5
        DB['H_S_OFICIAL_SEXTA']=H_S_OFICIAL_SEXTA     
        H_S_ALMOCO    = 11.6
        DB['H_S_ALMOCO']=H_S_ALMOCO
        H_E_ALMOCO    = 13.0
        DB['H_E_ALMOCO']=H_E_ALMOCO
        #total working day hours
        C_H_NORMAL    = (H_S_OFICIAL - H_E_OFICIAL) - T_ALMOCO#9.1
        DB['C_H_NORMAL']=C_H_NORMAL
        C_H_SEXTA     = (H_S_OFICIAL_SEXTA - H_E_OFICIAL) - T_ALMOCO#7.6
        DB['C_H_SEXTA']=C_H_SEXTA
        START_REPORT_DAY      = 21
        DB['START_REPORT_DAY']=START_REPORT_DAY
        DB.sync() 
           
    @staticmethod  
    def GetJorneyInSeconds():
        nowtime = time.localtime()
        if nowtime.tm_wday == 4: #Sexta-feira
            return CRPConfig.C_H_SEXTA*3600
        else:
            return CRPConfig.C_H_NORMAL*3600
    @staticmethod  
    def GetLanchTimeInSeconds():
        return CRPConfig.T_ALMOCO*3600
    @staticmethod  
    def Get_H_S_OFICIAL():
        nowtime = time.localtime()
        if nowtime.tm_wday == 4: #Sexta-feira
            return CRPConfig.H_S_OFICIAL_SEXTA
        else:
            return CRPConfig.H_S_OFICIAL

def main():
    config = CRPConfig()
    

if __name__ == '__main__':
    main()    
        