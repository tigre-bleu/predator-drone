#
# Program banner
#

from . import disp


# ============
#    Banner
# ============

R = disp.term.RED
O = disp.term.ORANGE
G = disp.term.GREEN
E = disp.term.ENDC

banner = "\n"\
+O+"                  ___  ___  ____  _  ______    ___  ___  _______  ___ __________  ___  \n"\
  +"                 / _ \/ _ \/ __ \/ |/ / __/   / _ \/ _ \/ __/ _ \/ _ /_  __/ __ \/ _ \\\n"\
  +"                / // / , _/ /_/ /    / _/    / ___/ , _/ _// // / __ |/ / / /_/ / , _/ \n"\
  +"               /____/_/|_|\____/_/|_/___/   /_/  /_/|_/___/____/_/ |_/_/  \____/_/|_|  \n\n\n"\
+E+"                                              :r7v77:\n"\
  +"                                          jBBBBBBBBBBQBBX.\n"\
  +"                                        .RBBBq:i7LJrrUKgBBBBr\n"\
  +"                                      gBBQBX        Xr 7BBBBB.\n"\
  +"                                     BBBBBQ  BBDS       dBBBBBr\n"\
  +"                                    BQBBBBB              BBQBBB:\n"\
  +"                                   BBK    LBBL.          qBBBBBB\n"\
  +"                                  .BBI     iBBBBBB       L  7BBQI\n"\
  +"                                  vBBBB.       rPBD           QBB\n"\
  +"                                  1BBQBBBS.                   BBB\n"\
  +"                                  iBBBBBB:.qQ7               BQBQ\n"\
+R+"              :r2qMBBBBBBBBQQESvi"+E+" .BBBBBB   ivBBBZ27riiiir5BBBBBr"+R+" .:v1bgBQBBBBBQBME2Li.\n"\
+R+"          iqRBBBBBDKjv77r77jIdMBBBRDdg"+E+"QBBBr    7DQI75UUUZBBBBBR"+R+"MEBBBBBEXjL77r77JIZQBQBBBbL.\n"\
+R+"       .XQQgQZL.                  :7KZbXE"+E+"BB.       :.   gBB"+R+"dqKZPUr.                 .iKQQgQEi\n"\
+R+"      rQZZZd.                         :IZdd"+E+"B.      i:  :B"+R+"PKZPr                          sMdZMP\n"\
+R+"     .BEPPq                              UMZR"+E+"2        r"+R+"MdbE:                             rEqERs\n"\
+R+"     .QZKd7                               rgbgg      2gddX                                EPPQs\n"\
+R+"      jMZdD                                KbPR2    :QEqZ                                jDPgD\n"\
+R+"       rRMgQ:           "+E+"iBBBB:"+R+"             PPdMI    .BEbd.             "+E+"BBBBB"+R+"            KRgQU\n"\
+R+"         vQQBgr         "+E+"iBBBBZ"+R+"            qDDgZ      YQZDg:           "+E+"rBBBBM"+R+"         .XBBQ5.\n"\
+R+"           :2BBBgs.       "+E+".YQBBBB5:"+R+"     rQRRdi        .XgQBU     "+E+".vBBBBBI:"+R+"       .rbBBBEr\n"\
+R+"              .7dBBBBMKvi.    "+E+".2BBBBBgL."+R+"                    "+E+".rPQBBBBg:"+R+"     :7UDBBBBgj:\n"\
+R+"                   .iL5ZMBQBMSi   "+E+":EBBQBBBgSsLr:::.::i7sUEBBBBQBB7"+R+"   :sgBBQQZPjr.\n"\
+R+"                                      "+E+"sBBQBBBQBBBBBBBBBBBBBBBb.\n"\
+R+"                      .7JXKPXPXqPbXSYr  "+E+".gQBBBBBBBBBBBBBBBB7"+R+"  :LUKKbKqXqXPSIv:\n"\
+R+"                  .LMBBS7:.         .:i   "+E+"QBBQBBBBBBBBBQBB"+R+"   ii..         :iUgBB5:\n"\
+R+"                 1BQd                   "+E+"7BBBBBQBBBBBBBBBBBBd"+R+"                   YQBg\n"\
+R+"                 qBRJ                "+E+"7BBBBBBES5Yriiirvj1qBBQBBq."+R+"                QQB\n"\
+R+"                  iDBg:        "+E+"BBBBBBBR7"+E+"                    "+E+":qBBBBBBB."+R+"       .UBQs\n"\
+R+"                    .vgRZU7:.  "+E+"dBBP:"+R+"     :1RB2                  "+E+".JBBB"+R+"  .:ruPQMS.\n"\
+R+"                         :7jUSr    iJ2IS2si.                UKIur.   .2SjLi.\n\n\n"\
+E+"     ,---.             .                   .                .        .  .                   .  .  \n"\
  +"     |   | ,-. ,-.   ,-| ,-. ,-. ,-. ,-.   |- ,-.   ,-. . . |  ,-.   |- |-. ,-. ,-,-.   ,-. |  |  \n"\
  +"     |   | | | |-'   | | |   | | | | |-'   |  | |   |   | | |  |-'   |  | | |-' | | |   ,-| |  |  \n"\
  +"     `---' ' ' `-'   `-' '   `-' ' ' `-'   `' `-'   '   `-' `' `-'   `' ' ' `-' ' ' '   `-^ `' `' \n\n"



# ====================
#    Banner printer
# ====================

def show():
    disp.banner(banner)

