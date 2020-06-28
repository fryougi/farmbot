# -*- coding: utf-8 -*-
"""
FGO Auto-farming (BlueStacks Version 1.8)
"""
import win32api, win32con, win32gui
import os, os.path
import time
import numpy
import PIL.ImageGrab
import cv2
import winsound


class Cursor():
  def __init__(self, app='nox'):
    self.app = app
    # find window by name
    if app == 'nox':
      self.hwnd = win32gui.FindWindow(None, "NoxPlayer")
    elif app == 'blue':
      self.hwnd = win32gui.FindWindow(None, "BlueStacks")
    if self.hwnd == 0:
      self.rect = (50, 50, 900, 500)
    else:
      if app == 'blue':
        # resize window because bluestacks is dumb about resolution
        x0, y0, x1, y1 = win32gui.GetWindowRect(self.hwnd)
        win32gui.MoveWindow(self.hwnd, x0, y0, 1285, 764, True)
      self.rect = win32gui.GetWindowPlacement(self.hwnd)[-1]
    self.xres = win32api.GetSystemMetrics(0)
    self.yres = win32api.GetSystemMetrics(1)
    # FGO Screen is 640x360 (16:9 ratio)
    # (originally developed for samsung smart view)
    if app == 'nox':
      # For Nox, running 1280x720 resolution
      # Depending on screen resolution, the
      # Nox menu bar will be sized differently
      self.xleft = 1
      self.ytop = 33#33 #49
      self.xtol = 1280
      self.ytol = 720
    elif app == 'blue':
      # Just have horizontal bluestacks
      self.xleft = 2
      self.ytop = 42
      self.xtol = 1280
      self.ytol = 720
    # set valid cursor locations
    self.xmin = self.rect[0] + self.xleft
    self.xmax = self.xmin + self.xtol
    self.ymin = self.rect[1] + self.ytop
    self.ymax = self.ymin + self.ytol
    
  def activate(self):
    # Activate window by clicking it
    win32api.SetCursorPos((self.rect[0]+10,self.rect[1]+10))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,self.rect[0]+10,self.rect[1]+10,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,self.rect[0]+10,self.rect[1]+10,0,0)
  
  def window(self):
    return (self.xmin, self.ymin, self.xmax, self.ymax)
  
  def xytonoxblue(self, xy):
    x = int(round(xy[0]*2))
    y = int(round(xy[1]*2))
    return (x,y)
  
  def xytoflow(self, xy):
    x = int(round(xy[0]))
    y = int(round(xy[1]))
    return (x,y)
  
  def rel2abs(self,xy):
    # Convert relative to nox xy (from 640/360)
    xy = self.xytonoxblue(xy)
    # place cursor within bounding box of FGO game
    xabs = self.rect[0] + self.xleft + xy[0]
    yabs = self.rect[1] + self.ytop + xy[1]
    if xabs < self.xmin:
      xabs = self.xmin
    if xabs > self.xmax:
      xabs = self.xmax
    if yabs < self.ymin:
      yabs = self.ymin
    if yabs > self.ymax:
      yabs = self.ymax
    return (xabs, yabs)
  
  def click(self,xy,dt=0.015):
    x, y = self.rel2abs(xy)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(dt)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
  def moveto(self,xy,nmoves=15):
    xabs, yabs = self.rel2abs(xy)
    xcur, ycur = win32gui.GetCursorPos()
    if xabs == xcur and yabs == ycur:
      return
    xpath = numpy.linspace(xcur*65535/self.xres,xabs*65535/self.xres,nmoves)
    ypath = numpy.linspace(ycur*65535/self.yres,yabs*65535/self.yres,nmoves)
    for i in range(nmoves):
      win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE,
                           int(xpath[i]),int(ypath[i]))
      time.sleep(0.001)
    win32api.SetCursorPos((xabs,yabs))
    
  def moveclick(self,xy):
    self.moveto(xy)
    time.sleep(0.05)
    self.click(xy)
    
  # Meant to be used for present box, but now filters are a thing
  # The code here only really works on Nox anyway, there's acceleration
  # during click/drag which makes the whole process very finicky
  def scroll(self, xy_start, xy_finish, nmoves=40):
    # click
    self.moveto(xy_start)
    xstart, ystart = self.rel2abs(xy_start)
    win32api.SetCursorPos((xstart,ystart))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,xstart,ystart,0,0)
    time.sleep(0.1)
    # drag
    xfinish, yfinish = self.rel2abs(xy_finish)
    xcur, ycur = win32gui.GetCursorPos()
    if xfinish == xcur and yfinish == ycur:
      return
    xpath = numpy.linspace(xcur*65535/self.xres,xfinish*65535/self.xres,nmoves)
    ypath = numpy.linspace(ycur*65535/self.yres,yfinish*65535/self.yres,nmoves)
    for i in range(nmoves):
      win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE |
                           win32con.MOUSEEVENTF_LEFTDOWN, int(xpath[i]),int(ypath[i]))
      time.sleep(0.015)
    win32api.SetCursorPos((xfinish,yfinish))
    # release
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE |
                         win32con.MOUSEEVENTF_LEFTDOWN, int(xpath[nmoves-1]),int(ypath[nmoves-1]))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,xfinish,yfinish,0,0)
    time.sleep(0.1)
    
    
class Screen():
  def __init__(self, window, app='nox', path='../'):
    self.app = app
    self.path = path
    self.window = window
    self.frame = PIL.ImageGrab.grab(self.window)
    self.cvframe = numpy.array(self.frame)
    self.cvframe = self.cvframe[:,:,::-1].copy()
    # TODO: make this configurable?
    self.framecount = len([name for name in os.listdir(self.path+'frames') if os.path.isfile(os.path.join(self.path,'frames',name))])
  
  def getframe(self):
    self.frame = PIL.ImageGrab.grab(self.window)
    self.cvframe = numpy.array(self.frame)
    self.cvframe = self.cvframe[:,:,::-1].copy()
  
  def dispframe(self):
    cv2.imshow('cvframe',self.cvframe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
  def saveframe(self):
    self.framecount +=1
    self.getframe()
    cv2.imwrite(self.path+'frames/frame%d.png'% self.framecount, self.cvframe)
    
  def matchtmpl(self,window,tmpl,mask,tol):
    cvwnd = self.cvframe[window[1]:window[3],window[0]:window[2]]
    h,w,_ = tmpl.shape
    if mask is None:
      res = cv2.matchTemplate(cvwnd, tmpl, cv2.TM_CCORR_NORMED)
    else:
      data = numpy.zeros((h,w,3),dtype=numpy.uint8)
      res = cv2.matchTemplate(cvwnd, tmpl, cv2.TM_CCORR_NORMED, data, mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val > tol

#cursor = Cursor()
#screen = Screen(cursor.window())


class Farmer():
  def __init__(self, app='nox', path='../'):
    self.app = app
    self.path = path
    self.cursor = Cursor(self.app)
    self.screen = Screen(self.cursor.window(), self.app, self.path)
    # Press F6 to escape out of a run gone awry
    self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
    self.escaped = False
    # Easy looping for babysitting CE selection, etc.
    self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
    self.quitloop = win32api.GetAsyncKeyState(win32con.VK_F4)
    self.timeout = 90.0 # 1.5 minutes (nps don't last this long)
    self.timer = 0.0
    self.retries = 0
    self.runs = 0
    self.refills = 0
    self.refilltype = 'rapple' # rapples and gapples
    self.supportce = 'none' # e.g. lunchtime, olgalesson
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
    self.xy_next = (550,340)
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
    # Raid boss title reset
    self.xy_newsclose = (622,18)
    self.xy_fpgainclose = (174,284)
    self.xy_myroom = (540,325)
    self.xy_menubutton = (595,343)
    self.xy_roomscrolluptop = (627,60)
    self.xy_roomscrollupmid = (627,110)
    self.xy_roomscrollupbot = (627,160)
    self.xy_roomscrolldntop = (627,210)
    self.xy_roomscrolldnmid = (627,260)
    self.xy_roomscrolldnbot = (627,310)
    self.xy_returntotitle = (480,250)
    self.xy_returnokay = (420,284)
    
    # While button locations can be scaled, 
    # image templates are a lot more finicky
    
    # Warning: not all functionality works with all
    # apps because the templates are missing
    
    # TODO: add CEs as needed (also update selsupport accordingly)
    # CEs need a template to read them and a tolerance (may be common)
    
    if self.app == 'nox':
      # List of template locations in window
      self.window_menubutton = (1127, 661, 1247, 701) # nox full
      self.window_selectsupport = (915, 5, 1275, 85)
      self.window_confirmsetup = (1086, 212, 1178, 258)
      self.window_startquest = (1118, 656, 1258, 696)
      self.window_attackbutton = (1067, 633, 1207, 678)
      self.window_mcskill = (1134, 254, 1254, 372)
      self.window_replacebutton = (561, 600, 721, 650)
      self.window_nextbutton = (1038, 653, 1178, 703)
      self.window_apclosebutton = (562, 594, 712, 644)
      self.window_apokbutton = (769, 538, 919, 588)
      self.window_support1ce = (52, 327, 209, 371)
      self.window_support2ce = (52, 526, 209, 570)
      self.window_lottoresetbox = (1060, 228, 1210, 261)
      self.window_lottoresetclose = (566, 536, 716, 586)
      self.window_retrybutton = (768, 542, 908, 587)
      self.window_updateclose = (565, 540, 715, 585)
      self.window_fp10xsummon = (726, 513, 926, 593)
      self.window_fpsummonokay = (760, 541, 925, 586)
      self.window_fpsummoncont = (685, 648, 844, 698)
      self.window_fpsummonclose = (566, 538, 716, 588)
      self.window_fpenhancece = (934, 6, 1274, 66)
      self.window_fpenhanceokay = (769, 565, 919, 615)
      # List of template images
      self.tmpl_menubutton = cv2.imread(self.path+'templates/nox/menubutton.png')
      self.tmpl_selectsupport = cv2.imread(self.path+'templates/nox/selectsupport.png')
      self.tmpl_confirmsetup = cv2.imread(self.path+'templates/nox/confirmsetup.png')
      self.tmpl_startquest = cv2.imread(self.path+'templates/nox/startquest.png')
      self.tmpl_attackbutton = cv2.imread(self.path+'templates/nox/attackbutton.png')
      self.tmpl_mcskill = cv2.imread(self.path+'templates/nox/mcskill.png')
      self.tmpl_mcskillmask = cv2.imread(self.path+'templates/nox/mcskillmask.png')
      self.tmpl_replacebutton = cv2.imread(self.path+'templates/nox/replacebutton.png')
      self.tmpl_nextbutton = cv2.imread(self.path+'templates/nox/nextbutton.png')
      self.tmpl_apclosebutton = cv2.imread(self.path+'templates/nox/apclosebutton.png')
      self.tmpl_apokbutton = cv2.imread(self.path+'templates/nox/apokbutton.png')
      self.tmpl_lottoresetbox = cv2.imread(self.path+'templates/nox/lottoresetbox.png')
      self.tmpl_lottoresetclose = cv2.imread(self.path+'templates/nox/lottoresetclose.png')
      self.tmpl_retrybutton = cv2.imread(self.path+'templates/nox/retrybutton.png')
      self.tmpl_updateclose = cv2.imread(self.path+'templates/nox/updateclose.png')
      self.tmpl_fp10xsummon = cv2.imread(self.path+'templates/nox/fp10xsummon.png')
      self.tmpl_fpsummonokay = cv2.imread(self.path+'templates/nox/fpsummonokay.png')
      self.tmpl_fpsummoncont = cv2.imread(self.path+'templates/nox/fpsummoncont.png')
      self.tmpl_fpsummonclose = cv2.imread(self.path+'templates/nox/fpsummonclose.png')
      self.tmpl_fpenhancece = cv2.imread(self.path+'templates/nox/fpenhancece.png')
      self.tmpl_fpenhanceokay = cv2.imread(self.path+'templates/nox/fpenhanceokay.png')
      # CEs (for full resolution, each location needs its own template)
      self.tmpl_ce_lunchtime1 = cv2.imread(self.path+'templates/nox/ce/lunchtime1.png')
      self.tmpl_ce_lunchtime2 = cv2.imread(self.path+'templates/nox/ce/lunchtime2.png')
      self.tmpl_ce_monalisa1 = cv2.imread(self.path+'templates/nox/ce/monalisa1.png')
      self.tmpl_ce_monalisa2 = cv2.imread(self.path+'templates/nox/ce/monalisa2.png')
      self.tmpl_ce_nerocheer1 = cv2.imread(self.path+'templates/nox/ce/nerocheer1.png')
      self.tmpl_ce_nerocheer2 = cv2.imread(self.path+'templates/nox/ce/nerocheer2.png')
      self.tmpl_ce_xmasmerry1 = cv2.imread(self.path+'templates/nox/ce/xmasmerry1.png')
      self.tmpl_ce_xmasmerry2 = cv2.imread(self.path+'templates/nox/ce/xmasmerry2.png')
      self.tmpl_ce_davincisoc1 = cv2.imread(self.path+'templates/nox/ce/davincisoc1.png')
      self.tmpl_ce_davincisoc2 = cv2.imread(self.path+'templates/nox/ce/davincisoc2.png')
    elif self.app == 'blue':
      # List of template locations in window
      self.window_menubutton = (1127, 666, 1247, 706) # bluestacks
      self.window_selectsupport = (951, 25, 1199, 57) #(919, 10, 1269, 60)
      self.window_confirmsetup = (1089, 213, 1179, 258)
      self.window_startquest = (1119, 657, 1259, 697)
      self.window_attackbutton = (1067, 640, 1207, 680)
      self.window_mcskill = (1137, 255, 1252, 370)
      self.window_replacebutton = (562, 602, 722, 647)
      self.window_nextbutton = (1033, 655, 1183, 705)
      self.window_apclosebutton = (571, 598, 711, 643)
      self.window_apokbutton = (779, 539, 904, 589)
      self.window_support1ce = (51, 326, 209, 371)
      self.window_support2ce = (51, 526, 209, 571)
      self.window_lottoresetbox = (1058, 229, 1218, 259)
      self.window_lottoresetclose = (571, 538, 711, 588)
      self.window_retrybutton = (773, 542, 903, 587)
      self.window_updateclose = (564, 537, 714, 587)
      self.window_repeatquest = (749, 545, 929, 590)
      self.window_sendrequest = (829, 593, 1079, 638)
      self.window_fp10xsummon = (736, 526, 916, 586)
      self.window_fpsummonokay = (789, 542, 889, 587)
      self.window_fpsummoncont = (684, 649, 844, 699)
      self.window_fpsummonclose = (565, 542, 715, 587)
      self.window_fpenhancece = (941, 9, 1271, 59)
      self.window_fpenhanceokay = (786, 565, 896, 615)
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
      self.tmpl_lottoresetbox = cv2.imread(self.path+'templates/blue/lottoresetbox.png')
      self.tmpl_lottoresetclose = cv2.imread(self.path+'templates/blue/lottoresetclose.png')
      self.tmpl_retrybutton = cv2.imread(self.path+'templates/blue/retrybutton.png')
      self.tmpl_updateclose = cv2.imread(self.path+'templates/blue/updateclose.png')
      self.tmpl_repeatquest = cv2.imread(self.path+'templates/blue/repeatquest.png')
      self.tmpl_sendrequest = cv2.imread(self.path+'templates/blue/sendrequest.png')
      self.tmpl_fp10xsummon = cv2.imread(self.path+'templates/blue/fp10xsummon.png')
      self.tmpl_fpsummonokay = cv2.imread(self.path+'templates/blue/fpsummonokay.png')
      self.tmpl_fpsummonclose = cv2.imread(self.path+'templates/blue/fpsummonclose.png')
      self.tmpl_fpsummoncont = cv2.imread(self.path+'templates/blue/fpsummoncont.png')
      self.tmpl_fpenhancece = cv2.imread(self.path+'templates/blue/fpenhancece.png')
      self.tmpl_fpenhanceokay = cv2.imread(self.path+'templates/blue/fpenhanceokay.png')
      # CEs get their own section (scaling is better in bluestacks, only one is needed)
      self.tmpl_ce_lunchtime = cv2.imread(self.path+'templates/blue/ce/lunchtime.png')
      self.tmpl_ce_monalisa = cv2.imread(self.path+'templates/blue/ce/monalisa.png')
      self.tmpl_ce_lesson = cv2.imread(self.path+'templates/blue/ce/lesson.png')
      self.tmpl_ce_training = cv2.imread(self.path+'templates/blue/ce/training.png')
      self.tmpl_ce_davincisoc = cv2.imread(self.path+'templates/blue/ce/davincisoc.png')
      
      # Magia Record
      self.xy_mr_start = (595,325)
      #self.xy_mr_advance = (315,175)
      #self.xy_mr_node = (315,95)
      self.xy_mr_advance = (275,165)
      #self.xy_mr_node = (450,75) # laby
      #self.xy_mr_node = (460,190) # story
      self.xy_mr_node = (450, 150) # tower event
      self.xy_mr_play = (535,270)
      self.xy_mr_playagain = (585,333)
      self.xy_mr_support = (335,130)
      #self.xy_mr_support = (335,220)
      self.xy_mr_greenpot = (145,300)
      self.xy_mr_redpot = (320,300)
      self.xy_mr_refillokay = (385,245)
      self.window_mr_menubutton = (1184, 26, 1254, 51)
      self.window_mr_selectsupport = (146, 612, 261, 652)
      self.window_mr_playbutton = (1013, 522, 1133, 567)
      self.window_mr_needsrefill = (242, 588, 342, 623)
      self.window_mr_startbutton = (1156, 630, 1226, 675)
      #self.window_mr_battleclear = (296, 158, 406, 208)
      self.window_mr_battleclear = (593, 327, 693, 402)
      self.window_mr_playagain = (1123, 652, 1223, 682)
      self.tmpl_mr_menubutton = cv2.imread(self.path+'templates/bluemr/menubutton.png')
      self.tmpl_mr_selectsupport = cv2.imread(self.path+'templates/bluemr/selectsupport.png')
      self.tmpl_mr_playbutton = cv2.imread(self.path+'templates/bluemr/playbutton.png')
      self.tmpl_mr_needsrefill = cv2.imread(self.path+'templates/bluemr/needsrefill.png')
      self.tmpl_mr_startbutton = cv2.imread(self.path+'templates/bluemr/startbutton.png')
      #self.tmpl_mr_battleclear = cv2.imread(self.path+'templates/bluemr/battleclear.png')
      self.tmpl_mr_battleclear = cv2.imread(self.path+'templates/bluemr/battleclear2.png')
      self.tmpl_mr_playagain = cv2.imread(self.path+'templates/bluemr/playagain.png')
      self.trigger_mr_menubutton = (self.window_mr_menubutton, self.tmpl_mr_menubutton, None, 0.9990)
      self.trigger_mr_selectsupport = (self.window_mr_selectsupport, self.tmpl_mr_selectsupport, None, 0.9990)
      self.trigger_mr_playbutton = (self.window_mr_playbutton, self.tmpl_mr_playbutton, None, 0.9990)
      self.trigger_mr_needsrefill = (self.window_mr_needsrefill, self.tmpl_mr_needsrefill, None, 0.9990)
      self.trigger_mr_startbutton = (self.window_mr_startbutton, self.tmpl_mr_startbutton, None, 0.9990)
      self.trigger_mr_battleclear = (self.window_mr_battleclear, self.tmpl_mr_battleclear, None, 0.9990)
      self.trigger_mr_playagain = (self.window_mr_playagain, self.tmpl_mr_playagain, None, 0.9990)
    else:
      # fail on other applications
      print("application {} not supported".format(self.app))
      return -1
    
    # List of tolerances for template match
    self.tol_menubutton = 0.9990
    self.tol_selectsupport = 0.9990
    self.tol_confirmsetup = 0.9990
    self.tol_startquest = 0.9990
    self.tol_attackbutton = 0.9900
    self.tol_mcskill = 0.9950
    self.tol_replacebutton = 0.9990
    self.tol_nextbutton = 0.9990
    self.tol_apclosebutton = 0.9990
    self.tol_apokbutton = 0.9990
    self.tol_lottoresetbox = 0.9990
    self.tol_lottoresetclose = 0.9990
    self.tol_retrybutton = 0.9990
    self.tol_updateclose = 0.9990
    self.tol_repeatquest = 0.9990
    self.tol_sendrequest = 0.9990
    self.tol_fp10xsummon = 0.9990
    self.tol_fpsummonokay = 0.9990
    self.tol_fpsummonclose = 0.9990
    self.tol_fpsummoncont = 0.9990
    self.tol_fpenhancece = 0.9990
    self.tol_fpenhanceokay = 0.9990
    self.tol_ceselect = 0.9990
      
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
    self.trigger_fpsummonokay = (self.window_fpsummonokay, self.tmpl_fpsummonokay, None, self.tol_fpsummonokay)
    self.trigger_fpsummoncont = (self.window_fpsummoncont, self.tmpl_fpsummoncont, None, self.tol_fpsummoncont)
    self.trigger_fpsummonclose = (self.window_fpsummonclose, self.tmpl_fpsummonclose, None, self.tol_fpsummonclose)
    self.trigger_fpenhancece = (self.window_fpenhancece, self.tmpl_fpenhancece, None, self.tol_fpenhancece)
    self.trigger_fpenhanceokay = (self.window_fpenhanceokay, self.tmpl_fpenhanceokay, None, self.tol_fpenhanceokay)

  def activate(self):
    self.cursor.activate()
    self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
    self.escaped = False
    
  def checkescape(self):
    self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
    if self.escape == 1:
      self.escaped = True
      print ("Escaped out of sequence")
    return self.escaped
  
  # Get frames until trigger event (template matched)
  def checktrigger(self,triggers):
    res = -1
    self.screen.getframe()
    for i, trigger in enumerate(triggers):
      if self.screen.matchtmpl(trigger[0],trigger[1],trigger[2],trigger[3]):
        res = i
        break
    return res
  
  def waitadvance(self,dt=0.05):
    # increments of 50ms
    t = 0
    while (t < dt):
      if self.checkescape():
        return -1
      time.sleep(0.05)
      t += 0.05
    if self.checkescape():
      return -1
    return t
  
  def clickadvance(self,xy,dt=0.05):
    # increments of 50ms
    t = 0
    while (t < dt):
      if self.checkescape():
        return -1
      self.cursor.click(xy)
      time.sleep(0.04)
      t += 0.05
    if self.checkescape():
      return -1
    return t
  
  def waituntiltrigger(self,triggers):
    res = -1
    self.timer = 0.0
    while (res < 0):
      t = self.waitadvance(0.05)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      t = self.waitadvance(0.05)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      self.timer += 0.1
      if self.timer > self.timeout:
        self.waitadvance(2)
        res = self.checktrigger([self.trigger_retrybutton])
        if res >= 0 and self.retries < 1:
          self.cursor.moveclick(self.xy_connretry)
          self.timer = 0 # Reset the timer upon retry
          self.retries += 1
          res = -1 # reset res to stay in while loop
        else:
          self.screen.saveframe()
          print("Timeout occurred")
          return -2
    self.waitadvance()
    return res
  
  
  def waitslowuntiltrigger(self,triggers):
    res = -1
    while (res < 0):
      t = self.waitadvance(0.35)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      t = self.waitadvance(0.35)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
    self.waitadvance()
    return res
    
  def clickuntiltrigger(self,triggers, xy):
    self.cursor.moveto(xy)
    self.waitadvance(0.1)
    res = -1
    self.timer = 0.0
    while (res < 0):
      t = self.waitadvance(0.05)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      t = self.clickadvance(xy)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      t = self.waitadvance(0.05)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      self.timer += 0.15
      if self.timer > self.timeout:
        self.waitadvance(2)
        res = self.checktrigger([self.trigger_retrybutton])
        if res >= 0 and self.retries < 1:
          self.cursor.moveclick(self.xy_connretry)
          self.timer = 0 # Reset the timer upon retry
          self.retries += 1
          res = -1 # reset res to stay in while loop
        else:
          self.screen.saveframe()
          print("Timeout occurred")
          return -2
    self.waitadvance()
    return res
  
  def clickslowuntiltrigger(self,triggers, xy):
    self.cursor.moveto(xy)
    self.waitadvance(0.1)
    res = -1
    while (res < 0):
      t = self.waitadvance(0.35)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
      t = self.clickadvance(xy)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      t = self.waitadvance(0.35)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
      if res >= 0:
        break
    self.waitadvance()
    return res
  
  def clickfastuntiltrigger(self,triggers, xy):
    self.cursor.moveto(xy)
    self.waitadvance(0.1)
    res = -1
    while (res < 0):
      t = self.clickadvance(xy)
      if t < 0:
        return -1
      t = self.waitadvance(0.1)
      if t < 0:
        return -1
      res = self.checktrigger(triggers)
    self.waitadvance()
    return res
  
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
    time.sleep(1.5)
    self.cursor.moveclick(self.xy_nodeselect)
    return res
  
  def nodeselectrefill(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_menubutton])
    if res < 0:
      return res
    time.sleep(1.5)
    self.cursor.moveclick(self.xy_nodeselect)
    res = self.waituntiltrigger([self.trigger_selectsupport, self.trigger_apclosebutton])
    if res == 1:
      res = self.refillsq()
      if res >= 0:
        res = self.waituntiltrigger([self.trigger_selectsupport])
    return res
  
  def norepeatquest(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_repeatquest])
    if res < 0:
      return res
    time.sleep(0.2)
    self.cursor.moveclick(self.xy_norepeat)
    return res
  
  def repeatquestrefill(self):
    self.waitadvance(0.1)
    res = self.waituntiltrigger([self.trigger_repeatquest])
    if res < 0:
      return res
    time.sleep(0.2)
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
    else: # TODO make sure these match the templates
      if self.app == 'nox':
        if self.supportce == 'lunchtime':
          trigger_tmpl1 = self.tmpl_ce_lunchtime1
          trigger_tmpl2 = self.tmpl_ce_lunchtime2
        elif self.supportce == 'monalisa':
          trigger_tmpl1 = self.tmpl_ce_monalisa1
          trigger_tmpl2 = self.tmpl_ce_monalisa2
        elif self.supportce == 'nerocheer':
          trigger_tmpl1 = self.tmpl_ce_nerocheer1
          trigger_tmpl2 = self.tmpl_ce_nerocheer2
        elif self.supportce == 'xmasmerry':
          trigger_tmpl1 = self.tmpl_ce_xmasmerry1
          trigger_tmpl2 = self.tmpl_ce_xmasmerry2
        elif self.supportce == 'davincisoc':
          trigger_tmpl1 = self.tmpl_ce_davincisoc1
          trigger_tmpl2 = self.tmpl_ce_davincisoc2
        else: # 'none' just pick first support
          self.cursor.moveclick(self.xy_support1)
          return 0
      elif self.app == 'blue':
        if self.supportce == 'lunchtime':
          trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_lunchtime
        elif self.supportce == 'monalisa':
          trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_monalisa
        elif self.supportce == 'lesson':
          trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_lesson
        elif self.supportce == 'training':
          trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_training
        elif self.supportce == 'davincisoc':
          trigger_tmpl1 = trigger_tmpl2 = self.tmpl_ce_davincisoc
        else: # 'none' just pick first support
          self.cursor.moveclick(self.xy_support1)
          return 0
    # Generate CE templates
    trigger1 = (self.window_support1ce, trigger_tmpl1, None, self.tol_ceselect)
    trigger2 = (self.window_support2ce, trigger_tmpl2, None, self.tol_ceselect)
    # check second support for ce first
    res = self.checktrigger([trigger2,trigger1])
    if res == 0:
      self.cursor.moveclick(self.xy_support2)
    elif res == 1:
      self.cursor.moveclick(self.xy_support1)
    else: # Update support list
      #if not updated:
      while True:
        self.waitadvance(0.5)
        self.cursor.moveclick(self.xy_supdate)
        self.waitadvance(0.75) # wait for dialog to pop up
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
      self.waitadvance(0.6) # get the skill started
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
      self.waitadvance(0.2)
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
  
  def playalarm(self):
    self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
    while True:
      self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
      if self.escape == 1:
        print ("Exited alarm")
        break
      else: # Loop alarm
        winsound.PlaySound('alarmsfx.wav',winsound.SND_FILENAME)
        time.sleep(0.2)
    return 0

  def mainloop(self, farm):
    print("Farming: Press F5 to run node, press F6 to quit")
    res = -1
    self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
    while True:
      if self.checkescape():
        break
      self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
      if self.runloop == 1:
        res = farm()
        if res < 0:
          break
        self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
      else: # Wait until next time
        time.sleep(1)
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
          time.sleep(0.03)
          selected += 1
          if selected >= num:
            return selected
      self.cursor.scroll(self.xy_invscroll1, self.xy_invscroll2)
      if self.checkescape():
        return -1
    return selected
  
  # Friend point summoning CE bombs
  def enhance(self):
    print("Farming: Press F5 to run node, press F4 to quit")
    numruns = 0
    self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
    self.quitloop = win32api.GetAsyncKeyState(win32con.VK_F4)
    while True:
      if self.checkescape():
        numruns = -1
        break
      self.quitloop = win32api.GetAsyncKeyState(win32con.VK_F4)
      if self.quitloop == 1:
        break
      self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
      if self.runloop == 1:
        numruns += 1
        selected = 0
        while selected < 20:
          for yexp in self.xy_expyloc:
            for xexp in self.xy_expxloc:
              xy_exp = (xexp,yexp)
              self.cursor.moveclick(xy_exp)
              time.sleep(0.02)
              selected += 1
              if selected >= 20:
                break
            if selected >= 20:
              break
        self.cursor.moveclick(self.xy_invokay)
        time.sleep(0.6)
        self.cursor.moveclick(self.xy_invenhance)
        time.sleep(0.4)
        self.cursor.moveclick(self.xy_invconfirm)
        self.runloop = win32api.GetAsyncKeyState(win32con.VK_F5)
      else: # Wait until next time
        time.sleep(1)
    return numruns
  
  def multenhance(self, num=7):
    numruns = 0
    while numruns < num:
      if self.checkescape():
        numruns = -1
        break
      selected = 0
      self.cursor.moveclick(self.xy_expfeed)
      time.sleep(0.8)
      while selected < 20:
        for yexp in self.xy_expyloc:
          for xexp in self.xy_expxloc:
            xy_exp = (xexp,yexp)
            self.cursor.moveclick(xy_exp)
            time.sleep(0.02)
            selected += 1
            if selected >= 20:
              break
          if selected >= 20:
            break
      self.cursor.moveclick(self.xy_invokay)
      res = self.waituntiltrigger([self.trigger_fpenhancece])
      if res >= 0:
        time.sleep(0.4)
        self.cursor.moveclick(self.xy_invenhance)
        time.sleep(0.2) #for good measure
        self.cursor.moveclick(self.xy_invenhance)
        res = self.waituntiltrigger([self.trigger_fpenhanceokay])
        if res >= 0:
          time.sleep(0.2)
          self.cursor.moveclick(self.xy_invconfirm)
          time.sleep(1.5) # need to get past loading
          res = self.clickuntiltrigger([self.trigger_fpenhancece],self.xy_invconfirm)
          if res >= 0:
            time.sleep(0.4)
      numruns += 1
    return numruns
  
  def fpsummon(self):
    # This is outdated
    num10xs = 0
    res = self.waituntiltrigger([self.trigger_fp10xsummon])
    while res >= 0:
      self.cursor.moveclick(self.xy_fpokay)
      # check for full inventory
      res = self.waituntiltrigger([self.trigger_fpsummonokay, self.trigger_fpsummonclose])
      if res == 0:
        self.cursor.click(self.xy_fpokay)
        num10xs += 1
        res = self.clickuntiltrigger([self.trigger_fpsummoncont], self.xy_fpempty)
        if res >= 0:
          self.cursor.moveclick(self.xy_fpsummon)
          res = self.waituntiltrigger([self.trigger_fp10xsummon])
      elif res == 1:
        return num10xs
    return res