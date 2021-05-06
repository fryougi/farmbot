# -*- coding: utf-8 -*-
"""
Karna
Eresh
Skader
"""
# Adding to the system path is needed
# because no longer in parent directory
# and I want to run this file as a script
import sys, os
sys.path.append(os.path.abspath('../'))
import farmbot as fb

class Farmer_Prison(fb.Farmbot):
  def __init__(self):
    fb.Farmbot.__init__(self,'blue','../')
    
  def wave1(self):
    res = self.advancestart()
    if res < 0:
      return -1
    # Skills selection (may be empty)
    res = self.useskill(self.xy_skillb3)
    if res < 0:
      return -1
    # Attack
    res = self.attack()
    if res < 0:
      return -1
    # Card selection (pick 3)
    self.usecard(self.xy_npb)
    self.usecard(self.xy_card3)
    self.usecard(self.xy_card2)
    return 0
  
  def wave2(self):
    res = self.advancewave()
    if res < 0:
      return -1
    # Skills selection (may be empty)
    res = self.useskill(self.xy_skillb2)
    if res < 0:
      return -1
    res = self.useskill(self.xy_skillc3)
    if res < 0:
      return -1
    res = self.seltarget(self.xy_targetb)
    if res < 0:
      return -1
    # Attack
    res = self.attack()
    if res < 0:
      return -1
    # Card selection (pick 3)
    self.usecard(self.xy_npb)
    self.usecard(self.xy_card3)
    self.usecard(self.xy_card2)
    # Potential cleanup
    return 0
  
  def wave3(self):
    res = self.advancewave()
    if res < 0:
      return -1
    # Skills selection (may be empty)
    res = self.useskill(self.xy_skilla1)
    if res < 0:
      return -1
    res = self.useskill(self.xy_skillc2)
    if res < 0:
      return -1
    res = self.usemcskill(self.xy_mcskill1)
    if res < 0:
      return -1
    res = self.seltarget(self.xy_targeta)
    if res < 0:
      return -1
    # Attack
    res = self.attack()
    if res < 0:
      return -1
    # Card selection (pick 3)
    self.usecard(self.xy_npa)
    self.usecard(self.xy_card2)
    self.usecard(self.xy_card3)
    # Potential cleanup
    return 0
    
  def farm(self,nruns=1):
    self.runs = 0
    self.refills = 0
    self.refilltype = 'rapple' # [rapple,gapple,sapple,bapple]
    self.supportce = 'teatime' # [lunchtime,training,lesson,monalisa,eventspecific]
    self.supportservant = 'skadi' # [waver,skadi]
    self.saveframe = False
    
    while True:
      # Start quest (set it up for the farmer)
      # Repeat quest no longer uses the party screen
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
      # Exit out to main menu if finished
      if self.runs >= nruns:
        res = self.norepeatquest()
        break
      # Repeat quest if not done (automatic refills)
      res = self.repeatquestrefill()
      if res < 0:
        return -1
      # Select new support
      res = self.selectsupport()
      if res < 0:
        return -1
    return self.runs

  def farmalarm(self, nruns=1):
    res = self.farm(nruns)
    print(res)
    self.playalarm()
    return

if __name__ == "__main__":
  farmer = Farmer_Prison()
  farmer.activate()