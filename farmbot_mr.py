# -*- coding: utf-8 -*-
"""
Farmer for Magia Record
"""
import cv2
from utils import Controller

class Farmbot(Controller):
  def __init__(self, app='blue', path=''):
    Controller.__init__(self,app,path)
    
    self.refills = 0
    self.refilltype = 'red'
    
    # List of locations (x,y)
    # Listed as original 640/360 from samsung flow

    # Locations change depending on what kind of node it is...
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
    
    # While button locations can be scaled, 
    # image templates are a lot more finicky

    if self.app == 'blue':
      self.window_mr_menubutton = (1184, 26, 1254, 51)
      self.window_mr_selectsupport = (146, 612, 261, 652)
      self.window_mr_playbutton = (1013, 522, 1133, 567)
      self.window_mr_needsrefill = (242, 588, 342, 623)
      self.window_mr_startbutton = (1156, 630, 1226, 675)
      self.window_mr_battleclear = (593, 327, 693, 402)
      self.window_mr_playagain = (1123, 652, 1223, 682)
      self.tmpl_mr_menubutton = cv2.imread(self.path+'templates/blue_mr/menubutton.png')
      self.tmpl_mr_selectsupport = cv2.imread(self.path+'templates/blue_mr/selectsupport.png')
      self.tmpl_mr_playbutton = cv2.imread(self.path+'templates/blue_mr/playbutton.png')
      self.tmpl_mr_needsrefill = cv2.imread(self.path+'templates/blue_mr/needsrefill.png')
      self.tmpl_mr_startbutton = cv2.imread(self.path+'templates/blue_mr/startbutton.png')
      self.tmpl_mr_battleclear = cv2.imread(self.path+'templates/blue_mr/battleclear.png')
      self.tmpl_mr_playagain = cv2.imread(self.path+'templates/blue_mr/playagain.png')
      
    else:
      # fail on other applications
      print("application {} not supported".format(self.app))
      return -1
    
    # List of triggers for detecting template match
    self.trigger_mr_menubutton = (self.window_mr_menubutton, self.tmpl_mr_menubutton, None, 0.9990)
    self.trigger_mr_selectsupport = (self.window_mr_selectsupport, self.tmpl_mr_selectsupport, None, 0.9990)
    self.trigger_mr_playbutton = (self.window_mr_playbutton, self.tmpl_mr_playbutton, None, 0.9990)
    self.trigger_mr_needsrefill = (self.window_mr_needsrefill, self.tmpl_mr_needsrefill, None, 0.9990)
    self.trigger_mr_startbutton = (self.window_mr_startbutton, self.tmpl_mr_startbutton, None, 0.9990)
    self.trigger_mr_battleclear = (self.window_mr_battleclear, self.tmpl_mr_battleclear, None, 0.9990)
    self.trigger_mr_playagain = (self.window_mr_playagain, self.tmpl_mr_playagain, None, 0.9990)
    
  def nodeselectrefill(self,play=False):
    # Select node again (automatic refills)
    self.waitadvance(1.0)
    self.cursor.moveclick(self.xy_mr_node)
    self.waitadvance(0.5)
    res = self.waituntiltrigger([self.trigger_mr_selectsupport, self.trigger_mr_needsrefill])
    if res == 1:
      self.waitadvance(1.0)
      self.cursor.click(self.xy_mr_greenpot)
      self.waitadvance(1.5)
      self.cursor.click(self.xy_mr_refillokay)
      self.waitadvance(1.0)
      if play:
        self.cursor.moveclick(self.xy_mr_play)
        self.waitadvance(1.0)
      res = self.waituntiltrigger([self.trigger_mr_selectsupport])
      if res < 0:
        return res
      self.waitadvance(0.7)
      self.cursor.click(self.xy_mr_support)
    elif res >= 0:
      self.waitadvance(0.7)
      self.cursor.click(self.xy_mr_support)
    else:
      return res
    return res

if __name__ == "__main__":
  farmer = Farmbot()
  farmer.activate()