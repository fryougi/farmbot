# -*- coding: utf-8 -*-
"""
Magia Record CC farm

Autobattle in magia record makes repeating quests significantly easier.
This file is pretty hacky though, I kinda just used what was working for FGO and added a tumor... I mean rumor.
"""
import farmbot as fb

class Magia_Record(fb.Farmer):
  def __init__(self):
    fb.Farmer.__init__(self,'blue')
      
  def farm(self,nruns=1):
    self.runs = 0
    while True:
      # Start quest (set it up for the farmer)
      res = self.waituntiltrigger([self.trigger_mr_startbutton])
      if res < 0:
        return -1
      self.waitadvance(1.0)
      self.cursor.moveclick(self.xy_mr_start)
      self.waitadvance(15.0)
      res = self.waitslowuntiltrigger([self.trigger_mr_battleclear])
      if res < 0:
        return -1
      res = self.clickuntiltrigger([self.trigger_mr_menubutton, self.trigger_mr_playagain], self.xy_mr_advance)
      if res < 0:
        return -1
      self.runs += 1
      # Exit if finished
      if self.runs >= nruns:
        self.waitadvance(0.5)
        self.cursor.moveclick(self.xy_mr_advance)
        break
      if res == 1:
        self.waitadvance(0.5)
        self.cursor.moveclick(self.xy_mr_playagain)
        res = self.waituntiltrigger([self.trigger_mr_menubutton])
        if res < 0:
          return -1
        self.waitadvance(1.5)
        res = self.checktrigger([self.trigger_mr_selectsupport])
        if res >= 0:
          self.waitadvance(0.7)
          self.cursor.click(self.xy_mr_support)
        else:
          self.waitadvance(1.0)
          res = self.checktrigger([self.trigger_mr_selectsupport])
          if res >= 0:
            self.waitadvance(0.7)
            self.cursor.click(self.xy_mr_support)
          else:
            self.waitadvance(1.0)
            self.cursor.moveclick(self.xy_mr_node)
            res = self.waituntiltrigger([self.trigger_mr_selectsupport])
            if res < 0:
              return -1
            self.waitadvance(0.7)
            self.cursor.click(self.xy_mr_support)
      elif res == 0:
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
          #self.cursor.moveclick(self.xy_mr_play)
          #self.waitadvance(1.0)
          res = self.waituntiltrigger([self.trigger_mr_selectsupport])
          if res < 0:
            return -1
          self.waitadvance(0.7)
          self.cursor.click(self.xy_mr_support)
        elif res >= 0:
          self.waitadvance(0.7)
          self.cursor.click(self.xy_mr_support)
        else:
          return -1
      self.waitadvance(0.5)
    return self.runs

# Main Loop
farmer = Magia_Record()
farmer.activate()
#farmer.mainloop(farmer.farm)