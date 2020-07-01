# -*- coding: utf-8 -*-
"""
Utils (moving cursor around, screen captures)
"""
import win32api, win32con, win32gui
import os, os.path
import time
import numpy
import PIL.ImageGrab
import cv2

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
  def __init__(self, window, outdir='frames'):
    self.outdir = outdir
    self.window = window
    self.frame = PIL.ImageGrab.grab(self.window)
    self.cvframe = numpy.array(self.frame)
    self.cvframe = self.cvframe[:,:,::-1].copy()
    self.framecount = len([name for name in os.listdir(outdir) if os.path.isfile(os.path.join(outdir,name))])
  
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
    cv2.imwrite(os.path.join(outdir,'frame%d.png'% self.framecount), self.cvframe)
    
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

# Example initializers
#cursor = Cursor()
#screen = Screen(cursor.window())