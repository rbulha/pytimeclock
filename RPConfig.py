import time

class CRPConfig:
    C_H_NORMAL    = 9.1
    C_H_SEXTA     = 7.6
    T_ALMOCO      = 1.4
    H_E_OFICIAL   = 7.0
    H_S_OFICIAL   = 17.5
    H_S_OFICIAL_SEXTA = 16.0     
    H_S_ALMOCO    = 11.6
    H_E_ALMOCO    = 13.0  
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
