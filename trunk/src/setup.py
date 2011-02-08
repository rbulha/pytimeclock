# -*- coding: UTF-8 -*-
import os
from distutils.core import setup
import py2exe
from Labeling  import CLabeling as LABELING     

# for the versioninfo resources
class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = LABELING.VERSION
        self.company_name = LABELING.COMPANY_NAME
        self.copyright = LABELING.COPYRIGHT
        self.name = LABELING.APP_NAME
        
opts = {
        "py2exe": 
        {
            "compressed": 1,
            "bundle_files": 1,
            "optimize": 2,
            "dist_dir": os.path.join("..//",LABELING.INSTALLATION_FOLDER),
        }
       }

windows_o = Target(
    # used for the versioninfo resource
    description= LABELING.APP_NAME,
    # what to build
    script = "RelogioDePonto.py",
    icon_resources = [(1, "../res/date.ico")],
    dest_base = "bin/TimeClock")

resourcefiles = ('res',
                  [
                    '../res/a_g_down.ico',
                    '../res/a_g_up.ico',
                    '../res/AT ST.ico',
                    '../res/Boba Fett.ico',
                    '../res/Button_Help.ico',
                    '../res/c3po.ico',
                    '../res/calendar.ico',
                    '../res/clock.bmp',
                    '../res/Clock.ico',
                    '../res/clock.png',
                    '../res/Darth_Vader.ico',
                    '../res/date.ico',
                    '../res/DeathStar.ico',
                    '../res/gauge.ico',
                    '../res/Gnome-Dialog-Question.ico',
                    '../res/Gold_1_star.ico',
                    '../res/Help.ico',
                    '../res/info_ex.ico',
                    '../res/l_b_up.ico',
                    '../res/l_g_down.ico',
                    '../res/lunch.ico',
                    '../res/M_Falcon.ico',
                    '../res/Moon.ico',
                    '../res/moon_1.ico',
                    '../res/moon_btm_2.png',
                    '../res/Move2Red.ico',
                    '../res/R2D2.ico',
                    '../res/r2d2.png',
                    '../res/relogioponto.ico',
                    '../res/report.ico',
                    '../res/report_32.png',
                    '../res/Right3Green.ico',
                    '../res/RightLeft2Red.ico',
                    '../res/Rotate90AntiClockwise2Yellow.ico',
                    '../res/Rotate270AntiClockwise3Green.ico',
                    '../res/Rotate360AntiClockwise2Red.ico',
                    '../res/Strooper.ico',
                    '../res/s_o_up.ico',
                    '../res/saida.png',
                    '../res/ScoutTrooper.ico',
                    '../res/small-blue-diamond.ico',
                    '../res/small-grey-diamond.ico',
                    '../res/small-lime-diamond.ico',
                    '../res/small-orange-diamond.ico',
                    '../res/small-red-diamond.ico',
                    '../res/small-white-diamond.ico',
                    '../res/small-yellow-diamond.ico',
                    '../res/stop16_16.ico',
                    '../res/stop.ico',
                    '../res/stop.png',
                    '../res/sunny.ico',
                    '../res/timeout.ico',
                    '../res/Up1Blue.ico',
                    '../res/UpDown1Yellow.ico',
                    '../res/UpRight2Blue.ico',
                    '../res/VistaWeatherPreview.jpg',
                    '../res/clock_flat_32.ico',
                    '../res/Plus.ico',
                    '../res/time_left.ico',
                    '../res/Help_32.png',
                    '../res/Refresh_24.png',
                    '../res/W95MBX03.ICO'
                  ]
                )
 
binaries = ('bin',[ 'MSVCR71.dll',
                    'msvcp71.dll', 
                    'msvcp90.dll',
                    'msvcr90.dll',
                    'gdiplus.dll',
                    'GUI.xrc' ]) 
                    
appdata = ('data',['../data/ponto.dat']) 
 
logfiles = ('log',['../log/log.log']) 

packet_files = [binaries, resourcefiles, appdata, logfiles] 
 
py_module_list = ['RelogioDePonto',
                  'GUI_xrc',
                  'BaseDefs',
                  'BookMark',
                  'Labeling',
                  'Milestones',
                  'PontoDB',
                  'Report',
                  'RPConfig'] 
                  
setup(
      options = opts,
      name=LABELING.APP_NAME,
      version=LABELING.VERSION,
      maintainer=LABELING.COMPANY_NAME,
      py_modules=py_module_list,
      data_files = packet_files,
      zipfile = None,
      windows = [windows_o]
     )
