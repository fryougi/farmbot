# -*- coding: utf-8 -*-
"""
Cursors, Mouse Emulation, Screen Capture, Template Matching, etc.
"""
import win32api, win32con, win32gui
import os, os.path
import time
import winsound
import numpy
import PIL.ImageGrab
import cv2

# Tesseract OCR
# Accuracy of this is pretty bad...
import sys, shutil
try:
  import pytesseract
except:
  pass

class Cursor():
  def __init__(self, app='blue'):
    self.app = app
    # find window by name
    if self.app == 'blue':
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
    if app == 'blue':
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
  
  def xytoblue(self, xy):
    x = int(round(xy[0]*2))
    y = int(round(xy[1]*2))
    return (x,y)
  
  def rel2abs(self,xy):
    # Convert relative to nox xy (from 640/360)
    xy = self.xytoblue(xy)
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
    
  def clickselect(self,xy_start,xy_stop):
    # click down, hold, move, release
    self.moveto(xy_start)
    x, y = self.rel2abs(xy_start)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(1.0)
    self.moveto(xy_stop)
    time.sleep(0.2)
    x, y = self.rel2abs(xy_stop)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
  # Meant to be used for present box, but now filters are a thing
  # The code here only really worked on Nox anyway, there's acceleration
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
  def __init__(self, window, outdir='screencaps'):
    self.outdir = outdir
    self.window = window
    self.frame = PIL.ImageGrab.grab(self.window)
    self.cvframe = numpy.array(self.frame)
    self.cvframe = self.cvframe[:,:,::-1].copy()
    self.framecount = len([name for name in os.listdir(self.outdir) if os.path.isfile(os.path.join(self.outdir,name))])
    
  def getframe(self):
    self.frame = PIL.ImageGrab.grab(self.window)
    self.cvframe = numpy.array(self.frame)
    self.cvframe = self.cvframe[:,:,::-1].copy()
  
  def dispframe(self):
    cv2.imshow('cvframe',self.cvframe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
  def saveframe(self):
    self.getframe()
    cv2.imwrite(os.path.join(self.outdir,'frame%d.png'% self.framecount), self.cvframe)
    self.framecount +=1
    
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
  
  def corrtmpl(self,window,tmpl,mask):
    cvwnd = self.cvframe[window[1]:window[3],window[0]:window[2]]
    h,w,_ = tmpl.shape
    if mask is None:
      res = cv2.matchTemplate(cvwnd, tmpl, cv2.TM_CCORR_NORMED)
    else:
      data = numpy.zeros((h,w,3),dtype=numpy.uint8)
      res = cv2.matchTemplate(cvwnd, tmpl, cv2.TM_CCORR_NORMED, data, mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val


class Controller():
  def __init__(self, app='blue', path=''):
    self.app = app
    self.path = path
    self.cursor = Cursor(self.app)
    self.screen = Screen(self.cursor.window(), self.path+'screencaps')
    # Press F6 to escape out of a run gone awry
    self.escape = win32api.GetAsyncKeyState(win32con.VK_F6)
    self.escaped = False
    self.timeout = 90.0 # 1.5 minutes (nps don't last this long)
    self.timer = 0.0
    self.retries = 0
    
    # Tesseract OCR (tests to see if it's usable)
    self.ocr = True
    if shutil.which('tesseract') is None:
      self.ocr = False
    if 'pytesseract' not in sys.modules:
      self.ocr = False

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
  
  def maxtrigger(self,triggers):
    corr = numpy.zeros(len(triggers))
    self.screen.getframe()
    for i, trigger in enumerate(triggers):
      corr[i] = self.screen.corrtmpl(trigger[0],trigger[1],trigger[2])
    return numpy.max(corr), numpy.argmax(corr)
  
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
    self.retries = 1
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
        if res >= 0 and self.retries < 2:
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
    self.retries = 1
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
        if res >= 0 and self.retries < 2:
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
  
  def windowtextocr(self,window,invert=False):
    if self.ocr:
      cvwnd = self.screen.cvframe[window[1]:window[3],window[0]:window[2]]
      cvwnd = cv2.cvtColor(cvwnd, cv2.COLOR_BGR2GRAY)
      if invert:
        cvwnd = cv2.threshold(255-cvwnd, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
      wave = pytesseract.image_to_string(cvwnd, config=r'-l eng --oem 3 --psm 7')
      return wave
    else:
      return None
