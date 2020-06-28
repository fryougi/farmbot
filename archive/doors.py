# -*- coding: utf-8 -*-
"""
40AP Hands

Mystic Code: Any
"""
import farmbot as fb

class DailyDoors(fb.Farmer):
  def __init__(self):
    fb.Farmer.__init__(self,'nox')
    
  def wave1(self):
    res = self.advancestart()
    if res < 0:
      return -1
    res = self.attack()
    if res < 0:
      return -1
    self.usecard(self.xy_npc)
    self.usecard(self.xy_card3)
    self.usecard(self.xy_npa)
    return 0
  
  def wave2(self):
    res = self.advancewave()
    if res < 0:
      return -1
    res = self.attack()
    if res < 0:
      return -1
    self.usecard(self.xy_npb)
    self.usecard(self.xy_card3)
    self.usecard(self.xy_npa)
    return 0
  
  def wave3(self):
    res = self.advancewave()
    if res < 0:
      return -1
    res = self.attack()
    if res < 0:
      return -1
    self.usecard(self.xy_npa)
    self.usecard(self.xy_card2)
    self.usecard(self.xy_card3)
    return 0
    
  def farm(self,nruns=1):
    self.runs = 0
    self.refills = 0
    self.refilltype = 'bapple' # use gapples for now
    self.supportce = 'monalisa' # lunchtime
    while True:
      # Start quest (set it up for the farmer)
      res = self.startquest()
      if res < 0:
        return -1
      # Battle procedure Wave1
      res = self.wave1()
      if res < 0:
        return -1
      # Battle prodedure Wave2
      res = self.wave2()
      if res < 0:
        return -1
      # Battle prodedure Wave3
      res = self.wave3()
      if res < 0:
        return -1
      # Finished run
      res = self.finishbattle()
      if res < 0:
        return -1
      self.runs += 1
      # Select node again if only one run
      if nruns == 1:
        res = self.nodeselect()
        break
      # Exit if finished
      if self.runs >= nruns:
        break
      # Select node again (automatic refills)
      res = self.nodeselectrefill()
      if res < 0:
        return -1
      # Select new support
      self.selectsupport()
    return self.runs

# Main Loop
farmer = DailyDoors()
farmer.activate()
#farmer.mainloop(farmer.farm)