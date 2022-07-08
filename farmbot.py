# -*- coding: utf-8 -*-
"""
FGO Auto-farming (BlueStacks Version 2.0)
"""
import cv2
from utils import Controller

class Farmbot(Controller):
  def __init__(self, app='blue', path='', region='na'):
    Controller.__init__(self,app,path)
    
    self.region = region
    self.runs = 0
    self.refills = 0
    self.refilltype = 'rapple' # rapples and gapples
    self.supportce = 'none' # e.g. lunchtime, olgalesson
    self.supportservant = 'none' # e.g. waver, skadi
    self.saveframe = False
    
    # List of locations (x,y)
    # Listed as original 640/360 from samsung flow
    # Preparation
    self.xy_nodeselect = (500,110)
    self.xy_support1 = (300,120)
    self.xy_support2 = (300,220)
    self.xy_support3 = (300,320)
    self.xy_supdate = (420,66)
    self.xy_supokay = (420,280)
    self.xy_supclose = (320,283)
    self.xy_connretry = (420,280)
    self.xy_startquest = (592,338)
    # Battle (Enemy: C, B, A  |  Servant: A, B, C)
    self.xy_attack = (566,300)
    self.xy_enemya = (262,22)
    self.xy_enemyb = (142,22)
    self.xy_enemyc = (22,22)
    self.xy_mcskill = (598,156)
    self.xy_mcskill1 = (454,156)
    self.xy_mcskill2 = (496,156)
    self.xy_mcskill3 = (542,156)
    self.xy_skilla1 = (33,288)
    self.xy_skilla2 = (80,288)
    self.xy_skilla3 = (127,288)
    self.xy_skillb1 = (193,288)
    self.xy_skillb2 = (240,288)
    self.xy_skillb3 = (287,288)
    self.xy_skillc1 = (353,288)
    self.xy_skillc2 = (400,288)
    self.xy_skillc3 = (447,288)
    self.xy_targeta = (172,230)
    self.xy_targetb = (322,230)
    self.xy_targetc = (472,230)
    self.xy_card1 = (66,260)
    self.xy_card2 = (192,260)
    self.xy_card3 = (318,260)
    self.xy_card4 = (444,260)
    self.xy_card5 = (580,260)
    self.xy_npa = (202,110)
    self.xy_npb = (318,110)
    self.xy_npc = (434,110)
    self.xy_swap1 = (67,175)
    self.xy_swap2 = (167,175)
    self.xy_swap3 = (267,175)
    self.xy_swap4 = (367,175)
    self.xy_swap5 = (467,175)
    self.xy_swap6 = (567,175)
    self.xy_replace = (320,313)
    self.xy_clickwave = (520,140)
    self.xy_clickdrop = (400,300)
    self.xy_clickcard = (25,140)
    #self.xy_next = (550,340)
    self.xy_next = (550,320)
    # Refills
    self.xy_close = (318,310)
    self.xy_rapple = (330,80)
    self.xy_gapple = (330,155)
    self.xy_sapple = (330,230)
    self.xy_bapple = (330,280)
    self.xy_degen = (420,280)
    self.xy_cancel = (220,280)
    self.xy_repeat = (420,280)
    self.xy_norepeat = (220,280)
    self.xy_request = (470,310)
    self.xy_norequest = (170,310)
    # Lotto
    self.xy_roll10 = (200,220)
    self.xy_lottoresetbox = (569,122)
    self.xy_resetconf = (420,284)
    self.xy_lottoresetclose = (320,284)
    # Giftbox
    self.xy_gbscroll1 = (425,330)
    self.xy_gbscroll2 = (425,125)
    self.xy_giftbox1 = (425,135)
    self.xy_giftbox2 = (425,200)
    self.xy_giftbox3 = (425,265)
    self.xy_giftbox4 = (425,330)
    # Inventory
    # should be at smallest (40 per exp)
    self.xy_invscroll1 = (136,335)
    self.xy_invscroll2 = (136,35)
    self.xy_expxloc = (70, 136, 203, 270, 336, 403, 470)
    self.xy_expyloc = (125, 195, 265, 335)
    self.xy_invokay = (578,338)
    self.xy_invenhance = (550,338)
    self.xy_invconfirm = (440,296)
    # Friend point summon
    self.xy_fpsummon = (384,338)
    self.xy_fpempty = (555,284)
    self.xy_fpokay = (420,284)
    self.xy_expfeed = (270,125)
    
    # While button locations can be scaled, 
    # image templates are a lot more finicky
    
    # TODO: add CEs as needed (also update selsupport accordingly)
    # CEs need a template to read them and a tolerance (may be common)

    if self.app == 'blue':
      # List of template locations in window
      self.window_menubutton = (1127, 666, 1247, 706) # bluestacks
      self.window_selectsupport = (951, 25, 1199, 57) #(919, 10, 1269, 60)
      self.window_confirmsetup = (1090, 213, 1178, 257)
      self.window_startquest = (1119, 657, 1259, 697)
      self.window_attackbutton = (1067, 640, 1207, 680)
      self.window_mcskill = (1137, 255, 1252, 370)
      self.window_replacebutton = (562, 602, 722, 647)
      #self.window_nextbutton = (1033, 655, 1183, 705)
      self.window_nextbutton = (1033, 617, 1183, 667)
      self.window_apclosebutton = (571, 598, 711, 643)
      self.window_apokbutton = (762, 541, 932, 586)
      self.window_support1ce = (51, 326, 209, 371)
      self.window_support2ce = (51, 526, 209, 571)
      self.window_support1servant = (51, 276, 101, 326)
      self.window_support2servant = (51, 476, 101, 526)
      #self.window_lottoresetbox = (1056, 229, 1216, 259)
      #self.window_lottoresetbox = (1074, 231, 1204, 256)
      self.window_lottoresetbox = (1067, 232, 1207, 257)
      self.window_lottoresetclose = (571, 538, 711, 588)
      self.window_retrybutton = (773, 542, 903, 587)
      self.window_updateclose = (566, 540, 716, 585)
      self.window_repeatquest = (749, 545, 929, 590)
      self.window_sendrequest = (829, 593, 1079, 638)
      self.window_fp10xsummon = (736, 526, 916, 586)
      #self.window_fp10xsummon = (685, 496, 885, 556)
      self.window_fp10xrepeat = (659, 654, 869, 694)
      self.window_fpsummonokay = (789, 542, 889, 587)
      self.window_fpsummoncont = (684, 649, 844, 699)
      self.window_fpsummonclose = (565, 542, 715, 587)
      self.window_fpenhancece = (982, 26, 1230, 58)
      self.window_fpenhancenone = (389, 259, 489, 309)
      self.window_fpenhanceselect = (7, 218, 57, 268)
      self.window_fpenhancelock = (71, 241, 91, 257)
      self.window_fpenhanceokay = (786, 565, 896, 615)
      self.window_fpenhanceservant = (1070, 8, 1270, 68)
      # List of template images
      self.tmpl_menubutton = cv2.imread(self.path+'templates/blue/menubutton.png')
      self.tmpl_selectsupport = cv2.imread(self.path+'templates/blue/selectsupport.png')
      self.tmpl_confirmsetup = cv2.imread(self.path+'templates/blue/confirmsetup.png')
      self.tmpl_startquest = cv2.imread(self.path+'templates/blue/startquest.png')
      self.tmpl_attackbutton = cv2.imread(self.path+'templates/blue/attackbutton.png')
      self.tmpl_mcskill = cv2.imread(self.path+'templates/blue/mcskill.png')
      self.tmpl_mcskillmask = cv2.imread(self.path+'templates/blue/mcskillmask.png')
      self.tmpl_replacebutton = cv2.imread(self.path+'templates/blue/replacebutton.png')
      self.tmpl_nextbutton = cv2.imread(self.path+'templates/blue/nextbutton.png')
      self.tmpl_apclosebutton = cv2.imread(self.path+'templates/blue/apclosebutton.png')
      self.tmpl_apokbutton = cv2.imread(self.path+'templates/blue/apokbutton.png')
      #self.tmpl_lottoresetbox = cv2.imread(self.path+'templates/blue/lottoresetbox.png')
      self.tmpl_lottoresetbox = cv2.imread(self.path+'templates/blue/lottoresetbox_4.png')
      self.tmpl_lottoresetclose = cv2.imread(self.path+'templates/blue/lottoresetclose.png')
      self.tmpl_retrybutton = cv2.imread(self.path+'templates/blue/retrybutton.png')
      self.tmpl_updateclose = cv2.imread(self.path+'templates/blue/updateclose.png')
      self.tmpl_repeatquest = cv2.imread(self.path+'templates/blue/repeatquest.png')
      self.tmpl_sendrequest = cv2.imread(self.path+'templates/blue/sendrequest.png')
      self.tmpl_fp10xsummon = cv2.imread(self.path+'templates/blue/fp10xsummon.png')
      #self.tmpl_fp10xsummon = cv2.imread(self.path+'templates/blue/fp10xsummon_2.png')
      self.tmpl_fp10xrepeat = cv2.imread(self.path+'templates/blue/fp10xrepeat.png')
      self.tmpl_fpsummonokay = cv2.imread(self.path+'templates/blue/fpsummonokay.png')
      self.tmpl_fpsummonclose = cv2.imread(self.path+'templates/blue/fpsummonclose.png')
      self.tmpl_fpsummoncont = cv2.imread(self.path+'templates/blue/fpsummoncont.png')
      self.tmpl_fpenhancece = cv2.imread(self.path+'templates/blue/fpenhancece.png')
      self.tmpl_fpenhancenone = cv2.imread(self.path+'templates/blue/fpenhancenone.png')
      self.tmpl_fpenhanceselect = cv2.imread(self.path+'templates/blue/fpenhanceselect.png')
      self.tmpl_fpenhancelock = cv2.imread(self.path+'templates/blue/fpenhancelock.png')
      self.tmpl_fpenhanceokay = cv2.imread(self.path+'templates/blue/fpenhanceokay.png')
      self.tmpl_fpenhanceservant = cv2.imread(self.path+'templates/blue/fpenhanceservant.png')
      # CEs get their own section (scaling is better in bluestacks, only one is needed)
      self.tmpl_ce_lunchtime = cv2.imread(self.path+'templates/blue/ce/lunchtime.png')
      self.tmpl_ce_teatime = cv2.imread(self.path+'templates/blue/ce/teatime.png')
      self.tmpl_ce_monalisa = cv2.imread(self.path+'templates/blue/ce/monalisa.png')
      self.tmpl_ce_bellalisa = cv2.imread(self.path+'templates/blue/ce/bellalisa.png')
      self.tmpl_ce_lesson = cv2.imread(self.path+'templates/blue/ce/lesson.png')
      self.tmpl_ce_training = cv2.imread(self.path+'templates/blue/ce/training.png')
      self.tmpl_ce_davincisoc = cv2.imread(self.path+'templates/blue/ce/davincisoc.png')
      self.tmpl_ce_gilckt = cv2.imread(self.path+'templates/blue/ce/gilckt.png')
      self.tmpl_ce_gilcktmlb = cv2.imread(self.path+'templates/blue/ce/gilcktmlb.png')
      self.tmpl_ce_maidenmlb = cv2.imread(self.path+'templates/blue/ce/maidenmlb.png')
      self.tmpl_ce_teatimecf = cv2.imread(self.path+'templates/blue/ce/teatimecf.png')
      # Servants also get their own section (for frontlining specific servants)
      self.tmpl_servant_waver1 = cv2.imread(self.path+'templates/blue/servant/waver1.png')
      self.tmpl_servant_waver2 = cv2.imread(self.path+'templates/blue/servant/waver2.png')
      self.tmpl_servant_waver3 = cv2.imread(self.path+'templates/blue/servant/waver3.png')
      self.tmpl_servant_skadi1 = cv2.imread(self.path+'templates/blue/servant/skadi1.png')
      self.tmpl_servant_skadi2 = cv2.imread(self.path+'templates/blue/servant/skadi2.png')
      self.tmpl_servant_skadi3 = cv2.imread(self.path+'templates/blue/servant/skadi3.png')
      self.tmpl_servant_reines1 = cv2.imread(self.path+'templates/blue/servant/reines1.png')
      self.tmpl_servant_reines2 = cv2.imread(self.path+'templates/blue/servant/reines2.png')
      self.tmpl_servant_reines3 = cv2.imread(self.path+'templates/blue/servant/reines3.png')
      self.tmpl_servant_castoria1 = cv2.imread(self.path+'templates/blue/servant/castoria1.png')
      self.tmpl_servant_castoria2 = cv2.imread(self.path+'templates/blue/servant/castoria2.png')
      self.tmpl_servant_castoria3 = cv2.imread(self.path+'templates/blue/servant/castoria3.png')
      
      # Replace some templates with jp stuff
      if self.region == 'jp':
        self.window_selectsupport = (948, 11, 1268, 61)
        self.tmpl_selectsupport = cv2.imread(self.path+'templates/blue/jpselectsupport.png')
        self.window_confirmsetup = (1090, 213, 1178, 257)
        self.tmpl_confirmsetup = cv2.imread(self.path+'templates/blue/jpconfirmsetup.png')
        self.window_updateclose = (567, 538, 707, 588)
        self.tmpl_updateclose = cv2.imread(self.path+'templates/blue/jpupdateclose.png')
        self.window_startquest = (1120, 656, 1260, 696)
        self.tmpl_startquest = cv2.imread(self.path+'templates/blue/jpstartquest.png')
        # Window for MCSkill is the same, which lets me reuse the MCSkillMask from above
        self.tmpl_mcskill = cv2.imread(self.path+'templates/blue/jpmcskill.png')
        self.window_replacebutton = (553, 601, 733, 651)
        self.tmpl_replacebutton = cv2.imread(self.path+'templates/blue/jpreplacebutton.png')
        self.window_nextbutton = (1026, 654, 1186, 704)
        self.tmpl_nextbutton = cv2.imread(self.path+'templates/blue/jpnextbutton.png')
        self.window_apclosebutton = (589, 594, 689, 644)
        self.tmpl_apclosebutton = cv2.imread(self.path+'templates/blue/jpapclosebutton.png')
        self.window_apokbutton = (789, 538, 889, 588)
        self.tmpl_apokbutton = cv2.imread(self.path+'templates/blue/jpapokbutton.png')
        self.window_repeatquest = (759, 543, 929, 588)
        self.tmpl_repeatquest = cv2.imread(self.path+'templates/blue/jprepeatquest.png')
        self.window_retrybutton = (758, 538, 918, 588)
        self.tmpl_retrybutton = cv2.imread(self.path+'templates/blue/jpretrybutton.png')
        self.window_lottoresetbox = (1054, 232, 1224, 257)
        self.tmpl_lottoresetbox = cv2.imread(self.path+'templates/blue/jplottoresetbox.png')
        self.window_lottoresetclose = (567, 537, 707, 587)
        self.tmpl_lottoresetclose = cv2.imread(self.path+'templates/blue/jplottoresetclose.png')
        self.tmpl_ce_jpscafes = cv2.imread(self.path+'templates/blue/ce/jpscafes.png')
      
    else:
      # fail on other applications
      print("application {} not supported".format(self.app))
      return -1
    
    # List of tolerances for template match
    self.tol_menubutton = 0.9990
    self.tol_selectsupport = 0.9990
    self.tol_confirmsetup = 0.9930
    self.tol_startquest = 0.9990
    self.tol_attackbutton = 0.9900
    self.tol_mcskill = 0.9930
    self.tol_replacebutton = 0.9990
    self.tol_nextbutton = 0.9970
    self.tol_apclosebutton = 0.9990
    self.tol_apokbutton = 0.9990
    self.tol_lottoresetbox = 0.9990
    self.tol_lottoresetclose = 0.9990
    self.tol_retrybutton = 0.9990
    self.tol_updateclose = 0.9990
    self.tol_repeatquest = 0.9990
    self.tol_sendrequest = 0.9990
    self.tol_fp10xsummon = 0.9900
    self.tol_fp10xrepeat = 0.9990
    self.tol_fpsummonokay = 0.9990
    self.tol_fpsummonclose = 0.9990
    self.tol_fpsummoncont = 0.9990
    self.tol_fpenhancece = 0.9990
    self.tol_fpenhancenone = 0.9990
    self.tol_fpenhanceselect = 0.9990
    self.tol_fpenhancelock = 0.9990
    self.tol_fpenhanceokay = 0.9990
    self.tol_fpenhanceservant = 0.9990
    self.tol_ceselect = 0.9970
    self.tol_servantselect = 0.9970
      
    # List of triggers for detecting template match
    # CE triggers are created on the fly in selsupport
    self.trigger_menubutton = (self.window_menubutton, self.tmpl_menubutton, None, self.tol_menubutton)
    self.trigger_selectsupport = (self.window_selectsupport, self.tmpl_selectsupport, None, self.tol_selectsupport)
    self.trigger_confirmsetup = (self.window_confirmsetup, self.tmpl_confirmsetup, None, self.tol_confirmsetup)
    self.trigger_startquest = (self.window_startquest, self.tmpl_startquest, None, self.tol_startquest)
    self.trigger_attackbutton = (self.window_attackbutton, self.tmpl_attackbutton, None, self.tol_attackbutton)
    self.trigger_mcskill = (self.window_mcskill, self.tmpl_mcskill, self.tmpl_mcskillmask, self.tol_mcskill)
    self.trigger_replacebutton = (self.window_replacebutton, self.tmpl_replacebutton, None, self.tol_replacebutton)
    self.trigger_nextbutton = (self.window_nextbutton, self.tmpl_nextbutton, None, self.tol_nextbutton)
    self.trigger_apclosebutton = (self.window_apclosebutton, self.tmpl_apclosebutton, None, self.tol_apclosebutton)
    self.trigger_apokbutton = (self.window_apokbutton, self.tmpl_apokbutton, None, self.tol_apokbutton)
    self.trigger_lottoresetbox = (self.window_lottoresetbox, self.tmpl_lottoresetbox, None, self.tol_lottoresetbox)
    self.trigger_lottoresetclose = (self.window_lottoresetclose, self.tmpl_lottoresetclose, None, self.tol_lottoresetclose)
    self.trigger_retrybutton = (self.window_retrybutton, self.tmpl_retrybutton, None, self.tol_retrybutton)
    self.trigger_updateclose = (self.window_updateclose, self.tmpl_updateclose, None, self.tol_updateclose)
    self.trigger_repeatquest = (self.window_repeatquest, self.tmpl_repeatquest, None, self.tol_repeatquest)
    self.trigger_sendrequest = (self.window_sendrequest, self.tmpl_sendrequest, None, self.tol_sendrequest)
    self.trigger_fp10xsummon = (self.window_fp10xsummon, self.tmpl_fp10xsummon, None, self.tol_fp10xsummon)
    self.trigger_fp10xrepeat = (self.window_fp10xrepeat, self.tmpl_fp10xrepeat, None, self.tol_fp10xrepeat)
    self.trigger_fpsummonokay = (self.window_fpsummonokay, self.tmpl_fpsummonokay, None, self.tol_fpsummonokay)
    self.trigger_fpsummoncont = (self.window_fpsummoncont, self.tmpl_fpsummoncont, None, self.tol_fpsummoncont)
    self.trigger_fpsummonclose = (self.window_fpsummonclose, self.tmpl_fpsummonclose, None, self.tol_fpsummonclose)
    self.trigger_fpenhancece = (self.window_fpenhancece, self.tmpl_fpenhancece, None, self.tol_fpenhancece)
    self.trigger_fpenhancenone = (self.window_fpenhancenone, self.tmpl_fpenhancenone, None, self.tol_fpenhancenone)
    self.trigger_fpenhanceselect = (self.window_fpenhanceselect, self.tmpl_fpenhanceselect, None, self.tol_fpenhanceselect)
    self.trigger_fpenhancelock = (self.window_fpenhancelock, self.tmpl_fpenhancelock, None, self.tol_fpenhancelock)
    self.trigger_fpenhanceokay = (self.window_fpenhanceokay, self.tmpl_fpenhanceokay, None, self.tol_fpenhanceokay)
    self.trigger_fpenhanceservant = (self.window_fpenhanceservant, self.tmpl_fpenhanceservant, None, self.tol_fpenhanceservant)
  
    # OCR Windows/Templates
    self.ocrwindow_wavetext = (872, 8, 942, 40)
    self.ocrtol_wavetext = 0.9800
    self.ocrtmpl_wave1 = cv2.imread(self.path+'templates/blue/ocr/1of3.png')
    self.ocrtmpl_wave1mask = cv2.imread(self.path+'templates/blue/ocr/1of3mask.png')
    self.ocrtmpl_wave2 = cv2.imread(self.path+'templates/blue/ocr/2of3.png')
    self.ocrtmpl_wave2mask = cv2.imread(self.path+'templates/blue/ocr/2of3mask.png')
    self.ocrtmpl_wave3 = cv2.imread(self.path+'templates/blue/ocr/3of3.png')
    self.ocrtmpl_wave3mask = cv2.imread(self.path+'templates/blue/ocr/3of3mask.png')
    self.ocrtrigger_wave1 = (self.ocrwindow_wavetext, self.ocrtmpl_wave1, self.ocrtmpl_wave1mask, self.ocrtol_wavetext)
    self.ocrtrigger_wave2 = (self.ocrwindow_wavetext, self.ocrtmpl_wave2, self.ocrtmpl_wave2mask, self.ocrtol_wavetext)
    self.ocrtrigger_wave3 = (self.ocrwindow_wavetext, self.ocrtmpl_wave3, self.ocrtmpl_wave3mask, self.ocrtol_wavetext)
  
  def farm(self,nruns=0):
    print("'farm' is not defined for farmbot base class, this method should be node-specific")
  
  def refillsq(self):
    if self.refilltype == 'gapple':
      self.cursor.moveclick(self.xy_gapple)
    elif self.refilltype == 'sapple':
      self.cursor.moveclick(self.xy_sapple)
    elif self.refilltype == 'bapple':
      self.cursor.moveclick(self.xy_bapple)
    else:
      self.cursor.moveclick(self.xy_rapple)
    res = self.waituntiltrigger([self.trigger_apokbutton])
    if res >= 0:
      self.cursor.moveclick(self.xy_degen)
      self.refills += 1
    return res
  
  def nodeselect(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_menubutton])
    if res < 0:
      return res
    self.waitadvance(1.5)
    self.cursor.moveclick(self.xy_nodeselect)
    return res
  
  def nodeselectrefill(self):
    # Not really used anymore due to repeat quest QoL
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_menubutton])
    if res < 0:
      return res
    self.waitadvance(1.5)
    self.cursor.moveclick(self.xy_nodeselect)
    res = self.waituntiltrigger([self.trigger_selectsupport, self.trigger_apclosebutton])
    if res == 1:
      res = self.refillsq()
      if res >= 0:
        res = self.waituntiltrigger([self.trigger_selectsupport])
    return res
  
  def norepeatquest(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_repeatquest, self.trigger_sendrequest])
    if res < 0:
      return res
    self.waitadvance(0.2)
    if res == 0:
      self.cursor.moveclick(self.xy_norepeat)
    elif res == 1:
      self.cursor.moveclick(self.xy_norequest)
    return res
  
  def repeatquestrefill(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_repeatquest])
    if res < 0:
      return res
    self.waitadvance(0.2)
    self.cursor.moveclick(self.xy_repeat)
    res = self.waituntiltrigger([self.trigger_selectsupport, self.trigger_apclosebutton])
    if res == 1:
      res = self.refillsq()
      if res >= 0:
        res = self.waituntiltrigger([self.trigger_selectsupport])
    return res
  
  def selectsupport(self):
    res = self.waituntiltrigger([self.trigger_selectsupport])
    if res < 0:
      return res
    res = self.waituntiltrigger([self.trigger_confirmsetup])
    if res < 0:
      return res
    # Just pick the CEs deterministically
    if self.supportce == 'first':
      self.cursor.moveclick(self.xy_support1)
      return 0
    elif self.supportce == 'second':
      self.cursor.moveclick(self.xy_support2)
      return 0
    elif self.supportce == 'none' and self.supportservant == 'none':
      self.cursor.moveclick(self.xy_support1)
      return 0
    else: # TODO make sure these match the templates
      if self.supportce == 'lunchtime':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_lunchtime
      elif self.supportce == 'teatime':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_teatime
      elif self.supportce == 'monalisa':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_monalisa
      elif self.supportce == 'bellalisa':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_bellalisa
      elif self.supportce == 'lesson':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_lesson
      elif self.supportce == 'training':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_training
      elif self.supportce == 'davincisoc':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_davincisoc
      elif self.supportce == 'gilckt':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_gilckt
      elif self.supportce == 'gilcktmlb':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_gilcktmlb
      elif self.supportce == 'maidenmlb':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_maidenmlb
      elif self.supportce == 'jpscafes':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_jpscafes
      elif self.supportce == 'teatimecf':
        trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_teatimecf
      else:
        trigger_tmpl1 = trigger_tmpl2 = None
      if self.supportservant == 'waver':
        trigger_tmpl3 = self.tmpl_servant_waver1
        trigger_tmpl4 = self.tmpl_servant_waver2
        trigger_tmpl5 = self.tmpl_servant_waver3
      elif self.supportservant == 'skadi':
        trigger_tmpl3 = self.tmpl_servant_skadi1
        trigger_tmpl4 = self.tmpl_servant_skadi2
        trigger_tmpl5 = self.tmpl_servant_skadi3
      elif self.supportservant == 'reines':
        trigger_tmpl3 = self.tmpl_servant_reines1
        trigger_tmpl4 = self.tmpl_servant_reines2
        trigger_tmpl5 = self.tmpl_servant_reines3
      elif self.supportservant == 'castoria':
        trigger_tmpl3 = self.tmpl_servant_castoria1
        trigger_tmpl4 = self.tmpl_servant_castoria2
        trigger_tmpl5 = self.tmpl_servant_castoria3
      else:
        trigger_tmpl3 = trigger_tmpl4 = trigger_tmpl5 = None
    # Generate CE templates
    if trigger_tmpl1 is None:
      trigger1 = trigger2 = None
    else:
      trigger1 = (self.window_support1ce, trigger_tmpl1, None, self.tol_ceselect)
      trigger2 = (self.window_support2ce, trigger_tmpl2, None, self.tol_ceselect)
    # Generate Servant templates
    if trigger_tmpl3 is None:
      trigger3 = trigger4 = trigger5 = trigger6 = trigger7 = trigger8 = None
    else:
      trigger3 = (self.window_support1servant, trigger_tmpl3, None, self.tol_servantselect)
      trigger4 = (self.window_support1servant, trigger_tmpl4, None, self.tol_servantselect)
      trigger5 = (self.window_support1servant, trigger_tmpl5, None, self.tol_servantselect)
      trigger6 = (self.window_support2servant, trigger_tmpl3, None, self.tol_servantselect)
      trigger7 = (self.window_support2servant, trigger_tmpl4, None, self.tol_servantselect)
      trigger8 = (self.window_support2servant, trigger_tmpl5, None, self.tol_servantselect)
    # Check for matches
    # Priority goes to CEs then servants
    # (most of the time servants will just be backlined anyway)
    nomatch = True
    if trigger1 is None:
      if trigger3 is None:
        # 'none' just pick first support
        self.cursor.moveclick(self.xy_support1)
        nomatch = False
      else: # Just look at servant triggers
        res = self.checktrigger([trigger8,trigger7,trigger6,trigger5,trigger4,trigger3])
        if res == 0 or res == 1 or res == 2:
          self.cursor.moveclick(self.xy_support2)
          nomatch = False
        elif res == 3 or res == 4 or res == 5:
          self.cursor.moveclick(self.xy_support1)
          nomatch = False
    else:
       # check match in support 2 first
      res = self.checktrigger([trigger2])
      if res == 0:
        if trigger3 is None:
          self.cursor.moveclick(self.xy_support2)
          nomatch = False
        else: # also check servants
          res = self.checktrigger([trigger8,trigger7,trigger6])
          if res == 0 or res == 1 or res == 2:
            self.cursor.moveclick(self.xy_support2)
            nomatch = False
      if nomatch:
        # check support 1 next
        res = self.checktrigger([trigger1])
        if res == 0:
          if trigger3 is None:
            self.cursor.moveclick(self.xy_support1)
            nomatch = False
          else: # also check servants
            res = self.checktrigger([trigger5,trigger4,trigger3])
            if res == 0 or res == 1 or res == 2:
              self.cursor.moveclick(self.xy_support1)
              nomatch = False
    if nomatch: # Update support list if nothing matches
      #if not updated:
      while True:
        self.waitadvance(0.5)
        self.cursor.moveclick(self.xy_supdate)
        self.waitadvance(2.0) # wait for dialog to pop up
        # Update support (should actually wait on both triggers)
        res = self.checktrigger([self.trigger_updateclose])
        if res < 0:
          break
        else:
          self.cursor.moveclick(self.xy_supclose)
        self.waitadvance(2.0)
      self.cursor.moveclick(self.xy_supokay)
      res = self.waituntiltrigger([self.trigger_confirmsetup])
      if res < 0:
        return res
      self.selectsupport()
      #else: # Give up and hope the third support has the CE
      #  self.cursor.moveclick(self.xy_support3)
    return 0
  
  def startquest(self):
    res = self.waituntiltrigger([self.trigger_startquest])
    self.waitadvance(1.0)
    if res >= 0:
      self.cursor.moveclick(self.xy_startquest)
      self.waitadvance(0.2)
      self.cursor.click(self.xy_startquest) # just to make sure
      self.waitadvance(0.2)
    return res
  
  def useskill(self, xy_skill):
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      self.cursor.moveclick(xy_skill)
      self.waitadvance(0.4) # get the skill started
    return res
  
  def usemcskill(self, xy_skill):
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      self.cursor.moveclick(self.xy_mcskill)
      self.waitadvance(0.8) # sometimes it lags
      self.cursor.moveclick(xy_skill)
      self.waitadvance(0.4) # get the skill started
    return res
  
  def seltarget(self, xy_target):
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      self.cursor.moveclick(xy_target)
      self.waitadvance(0.2) # get the skill started
    return res
  
  def plugsuit(self, xy_back, xy_front):
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      self.cursor.moveclick(self.xy_mcskill)
      self.waitadvance(0.8) #sometimes it lags
      self.cursor.moveclick(self.xy_mcskill3)
      self.waitadvance(0.4)
      self.cursor.moveclick(xy_back)
      self.waitadvance(0.2)
      self.cursor.moveclick(xy_front)
      self.waitadvance(0.3)
      self.cursor.moveclick(self.xy_replace)
      self.waitadvance(0.2) # get the skill started
      res = self.waituntiltrigger([self.trigger_mcskill])
      if res >= 0:
        self.waitadvance(0.5) # star redistribution
    return res
  
  def selenemy(self, xy_enemy):
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      self.cursor.moveclick(xy_enemy)
    return res
  
  def attack(self):
    self.waitadvance()
    res = self.waituntiltrigger([self.trigger_mcskill])
    if res >= 0:
      res = self.waituntiltrigger([self.trigger_attackbutton])
      if res >= 0:
        self.waitadvance(0.5)
        self.cursor.moveclick(self.xy_attack)
        self.waitadvance(2.0) # wait for cards (mostly nps) to load up
    return res
  
  def usecard(self, xy_card):
    self.waitadvance(0.2)
    self.cursor.moveclick(xy_card)
    self.waitadvance()
  
  def advancestart(self):
    self.cursor.moveto(self.xy_clickwave)
    res = self.waituntiltrigger([self.trigger_attackbutton])
    return res
  
  def advancewave(self):
    res = self.clickuntiltrigger([self.trigger_attackbutton], self.xy_clickwave)
    return res
  
  def finishbattle(self):
    res = self.clickuntiltrigger([self.trigger_nextbutton], self.xy_clickdrop)
    if res >= 0:
      if self.saveframe:
        self.waitadvance(0.2)
        self.screen.saveframe()
      self.cursor.moveclick(self.xy_next)
      self.waitadvance(0.2)
      self.cursor.click(self.xy_next) # just to make sure
      self.waitadvance(0.2)
      self.cursor.click(self.xy_next) # just to make sure
      self.waitadvance(0.4)
      self.cursor.click(self.xy_next) # ladder event extra drop page
      self.waitadvance(0.2)
      self.cursor.click(self.xy_next) # just to make sure
      self.waitadvance(0.2)
    return res
  
  def getwaveocr(self):
    wavetext = self.windowtextocr(self.ocrwindow_wavetext, invert=True)
    if wavetext is None:
      print("Warning: OCR not functioning")
      return 0
    else:
      if wavetext[0] == '1':
        return 1
      elif wavetext[0] == '2':
        return 2
      elif wavetext[0] == '3':
        return 3
      else:
        print("Warning: OCR not functioning")
        return 0
      
  def getwavetmpl(self):
    ocrtriggers = [self.ocrtrigger_wave1,self.ocrtrigger_wave2,self.ocrtrigger_wave3]
    wavecorr, waveindex = self.maxtrigger(ocrtriggers)
    if wavecorr > self.ocrtol_wavetext:
      return waveindex + 1
    else:
      print("Warning: OCR not functioning")
      return 0
      
  def cardcleanup(self,wave,warn=False):
    res = self.clickuntiltrigger([self.trigger_attackbutton, self.trigger_nextbutton], self.xy_clickcard)
    if res == 0:
      if wave == self.getwavetmpl():
        if warn:          
          print("Warning: Card cleanup needed on wave {}".format(wave))
        res = self.attack()
        if res < 0:
          return -1
        self.usecard(self.xy_card1)
        self.usecard(self.xy_card2)
        self.usecard(self.xy_card3)
        # Loop until done
        res = self.cardcleanup(wave)
        if res < 0:
          return -1
    return res
  
  # Lottery Inventory Management
  def rollbox(self, num=1):
    rolled = 0
    while rolled < num:
      res = self.clickfastuntiltrigger([self.trigger_lottoresetbox], self.xy_roll10)
      if res < 0:
        return -1
      rolled += 1
      # reset box
      self.cursor.moveclick(self.xy_lottoresetbox)
      self.waitadvance(0.6)
      self.cursor.moveclick(self.xy_resetconf)
      self.waituntiltrigger([self.trigger_lottoresetclose])
      self.cursor.moveclick(self.xy_lottoresetclose)
      self.waitadvance(0.2)
    return rolled
  
  def giftsel(self, num=99):
    selected = 0
    while selected < num:
      self.cursor.moveclick(self.xy_giftbox1)
      self.cursor.moveclick(self.xy_giftbox2)
      self.cursor.moveclick(self.xy_giftbox3)
      selected += 3
      self.cursor.scroll(self.xy_gbscroll1, self.xy_gbscroll2)
      if self.checkescape():
        return -1
    return selected
    
  def burnexp(self, num=99):
    selected = 0
    while selected < num:
      for yexp in self.xy_expyloc:
        for xexp in self.xy_expxloc:
          xy_exp = (xexp,yexp)
          self.cursor.moveclick(xy_exp)
          self.waitadvance(0.03)
          selected += 1
          if selected >= num:
            return selected
      self.cursor.scroll(self.xy_invscroll1, self.xy_invscroll2)
      if self.checkescape():
        return -1
    return selected
  
  # Friend point summoning CE bombs
  def enhancece(self, num=0):
    numruns = 0
    while (numruns < num) or (num == 0):
      if self.checkescape():
        break
      #selected = 0
      self.cursor.moveclick(self.xy_expfeed)
      # Get to the select screen
      res = self.waituntiltrigger([self.trigger_fpenhancelock,self.trigger_fpenhancenone,self.trigger_fpenhanceselect])
      # If the first CE is locked (e.g. by acquisition), finish
      if res < 2:
        break
      # This selects CEs individually based on the older version...
      #while selected < 20:
      #  for yexp in self.xy_expyloc:
      #    for xexp in self.xy_expxloc:
      #      xy_exp = (xexp,yexp)
      #      self.cursor.moveclick(xy_exp)
      #      self.waitadvance(0.02)
      #      selected += 1
      #      if selected >= 20:
      #        break
      #    if selected >= 20:
      #      break
      # This selects CEs using a click hold move release action
      xy_start = (self.xy_expxloc[0],self.xy_expyloc[0])
      xy_stop = (self.xy_expxloc[5],self.xy_expyloc[2])
      self.cursor.clickselect(xy_start,xy_stop)
      self.waitadvance(0.4)
      self.cursor.moveclick(self.xy_invokay)
      self.waitadvance(0.4)
      res = self.waituntiltrigger([self.trigger_fpenhancece])
      if res >= 0:
        self.cursor.moveclick(self.xy_invenhance)
        self.waitadvance(0.2) #for good measure
        self.cursor.moveclick(self.xy_invenhance)
        res = self.waituntiltrigger([self.trigger_fpenhanceokay])
        if res >= 0:
          self.cursor.moveclick(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          res = self.clickuntiltrigger([self.trigger_fpenhancece],self.xy_invconfirm)
          if res >= 0:
            self.waitadvance(0.4)
          else:
            break
        else:
          break
      else:
        break
      numruns += 1
    return numruns
  
  def fpsummon(self):
    # Commented out lines are from previous version of code
    # Different control logic was used
    num10xs = 0
    res = self.waituntiltrigger([self.trigger_fp10xsummon])
    # Start
    if res >= 0:
      self.cursor.moveclick(self.xy_fpokay)
    # Loop
    while res >= 0:
      #self.cursor.moveclick(self.xy_fpokay)
      # check for full inventory
      res = self.waituntiltrigger([self.trigger_fpsummonokay, self.trigger_fpsummonclose])
      if res == 0:
        self.cursor.click(self.xy_fpokay)
        # explicitly click initially to let the 10xrepeat button fade
        self.waitadvance(0.4)
        self.cursor.moveclick(self.xy_fpempty)
        self.waitadvance(0.4)
        self.cursor.click(self.xy_fpempty)
        self.waitadvance(0.4)
        self.cursor.click(self.xy_fpempty)
        num10xs += 1
        #res = self.clickuntiltrigger([self.trigger_fpsummoncont], self.xy_fpempty)
        res = self.clickuntiltrigger([self.trigger_fp10xrepeat], self.xy_fpempty)
        if res >= 0:
          # This goes immediately into a new summon
          self.cursor.moveclick(self.xy_fpsummon)
          #res = self.waituntiltrigger([self.trigger_fp10xsummon])
      elif res == 1:
        return num10xs
    return res

  # Friend point summoning CE bombs
  def enhanceservant(self, num=0):
    numruns = 0
    while (numruns < num) or (num == 0):
      if self.checkescape():
        break
      #selected = 0
      self.cursor.moveclick(self.xy_expfeed)
      # Get to the select screen
      res = self.waituntiltrigger([self.trigger_fpenhancelock,self.trigger_fpenhancenone,self.trigger_fpenhanceselect])
      # If the first CE is locked (e.g. by acquisition), finish
      if res < 2:
        break
      # This selects CEs individually based on the older version...
      #while selected < 20:
      #  for yexp in self.xy_expyloc:
      #    for xexp in self.xy_expxloc:
      #      xy_exp = (xexp,yexp)
      #      self.cursor.moveclick(xy_exp)
      #      self.waitadvance(0.02)
      #      selected += 1
      #      if selected >= 20:
      #        break
      #    if selected >= 20:
      #      break
      # This selects CEs using a click hold move release action
      xy_start = (self.xy_expxloc[0],self.xy_expyloc[0])
      xy_stop = (self.xy_expxloc[5],self.xy_expyloc[2])
      self.cursor.clickselect(xy_start,xy_stop)
      self.waitadvance(0.4)
      self.cursor.moveclick(self.xy_invokay)
      self.waitadvance(0.4)
      res = self.waituntiltrigger([self.trigger_fpenhanceservant])
      if res >= 0:
        self.cursor.moveclick(self.xy_invenhance)
        self.waitadvance(0.2) #for good measure
        self.cursor.moveclick(self.xy_invenhance)
        res = self.waituntiltrigger([self.trigger_fpenhanceokay])
        if res >= 0:
          self.cursor.moveclick(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          self.waitadvance(0.4)
          self.cursor.click(self.xy_invconfirm)
          res = self.clickuntiltrigger([self.trigger_fpenhanceservant],self.xy_invconfirm)
          if res >= 0:
            self.waitadvance(0.4)
          else:
            break
        else:
          break
      else:
        break
      numruns += 1
    return numruns
  

if __name__ == "__main__":
  farmer = Farmbot()
  farmer.activate()