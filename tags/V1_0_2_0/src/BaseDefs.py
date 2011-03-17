class TypeNIcons:
    NORMAL             = 0x01
    ALMOCO             = 0x02
    EXTRAORDINARIA     = 0x03
    PADRAO             = 0x04
    
    ENTRADA            = 0x10
    SAIDA              = 0x20
    MISC               = 0x30
    S_W                = 0x40
    MILESTONE          = 0x50
    
    BASE_RES_DIR            = "../res/"
        
    ICON = {}
    
    ICON[ENTRADA] = {}
    ICON[ENTRADA][NORMAL]           = BASE_RES_DIR+"a_g_down.ico"  
    ICON[ENTRADA][ALMOCO]           = BASE_RES_DIR+"l_g_down.ico"             
    ICON[ENTRADA][EXTRAORDINARIA]   = BASE_RES_DIR+"s_e_down.ico" #"small-red-diamond.ico"
    ICON[ENTRADA][PADRAO]           = BASE_RES_DIR+"sunny.ico"#"Gold_1_star.ico"#"small-blue-diamond.ico"
    
    ICON[SAIDA] = {}
    ICON[SAIDA][NORMAL]         = BASE_RES_DIR+"Up1Blue.ico"
    ICON[SAIDA][ALMOCO]         = BASE_RES_DIR+"l_b_up.ico"
    ICON[SAIDA][EXTRAORDINARIA] = BASE_RES_DIR+"s_e_up.ico"#"small-orange-diamond.ico"
    ICON[SAIDA][PADRAO]         = BASE_RES_DIR+"moon_1.ico"#"stop.ico"#"small-blue-diamond.ico"
    
    LUNCH  = 0x01
    QUESTION = 0x02
    EXTRA    = 0x03
    CLOCK    = 0x04
    CALEND   = 0x05
    
    ICON[MISC] = {}
    ICON[MISC][LUNCH] = BASE_RES_DIR+"lunch.ico"
    ICON[MISC][QUESTION] = BASE_RES_DIR+"Help.ico"
    ICON[MISC][EXTRA] = BASE_RES_DIR+"Move2Red.ico"
    ICON[MISC][CLOCK] = BASE_RES_DIR+"gauge.ico"
    ICON[MISC][CALEND] = BASE_RES_DIR+"calendar.ico"

    R2D2   = 0x01
    C3PO   = 0x02
    FALCON = 0x03
    DSTAR  = 0x04
    DVADER = 0x05

    ICON[S_W] = {}
    ICON[S_W][R2D2]     = BASE_RES_DIR+"R2D2.ico"
    ICON[S_W][C3PO]     = BASE_RES_DIR+"c3po.ico"
    ICON[S_W][FALCON]   = BASE_RES_DIR+"M_Falcon.ico"
    ICON[S_W][DSTAR]    = BASE_RES_DIR+"DeathStar.ico"
    ICON[S_W][DVADER]   = BASE_RES_DIR+"Darth_Vader.ico"
    
    EXTRA_TIME  = 0x01
    REMAIN_TIME = 0x02
    
    ICON[MILESTONE] = {}
    ICON[MILESTONE][EXTRA_TIME]  = BASE_RES_DIR+"Plus.ico"
    ICON[MILESTONE][REMAIN_TIME] = BASE_RES_DIR+"time_left.ico"
    
    
    
    
