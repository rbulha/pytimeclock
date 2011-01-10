import time

class CRPConfig:
    C_H_NORMAL    = 9.1
    C_H_SEXTA     = 7.6
    T_ALMOCO      = 1.5
    H_E_OFICIAL   = 7.0
    H_S_OFICIAL   = 17.6
    H_S_OFICIAL_SEXTA = 16.1     
    H_S_ALMOCO    = 11.6
    H_E_ALMOCO    = 13.1  
    @staticmethod  
    def GetJorneyInSeconds():
        nowtime = time.localtime()
        if nowtime.tm_wday == 4: #Sexta-feira
            return 7*3600 + 36*60
        else:
            return 9*3600 + 6*60