# farmbot

setup instructions for farmbot.py (may be outdatd at the moment, will try to edit later)

# ALWAYS SET UP YOUR BIND CODE AFTER TRANSFERING BETWEEN DEVICES

# Install python
I like the anaconda distribution since it comes with the spyder IDE that lets me load/edit/run files all within the same program (https://www.anaconda.com/distribution/).
During the installation, something that may trip up the executables is selecting between a local (user only "Just Me" option) install vs a global (all users) install. It is probably safer to do the user only installation as that'll keep everything sandboxed within your own user folders and installation of packages won't need extra administrator permissions. (it'll go in C:\Users\UserName\Anaconda3). It also makes uninstalling easier. By the way, this was all done on windows 10.

Once installed, try opening spyder as a sanity check (the application should just work...).
The left large window is the editor, and this is where you'll open/edit files
The bottom right window is the console, and this is where you'll be running commands from the farming scripts
Although the base installation installs quite a few needed python packages, there are some additional ones that'll need to be installed (like opencv (imported as cv2))
The import list for the farmbot.py file should let you know what's needed. An easy way to check if you have all the dependencies installed is to open up that file in the editor and run it. It doesn't do anything noticeable if it all works correctly, but if some of the depencencies aren't there, it'll display something like a module missing error in the console.

You can install these through the navigator (maybe?) or through the Anaconda prompt using "conda install"
- pillow is the thing you'd need to search for if PIL isn't installed (but it should be)
- pywin32 is the one you need for the windows mouse emulation and stuff (but it should be)
- opencv is the thing you'll need for all the image capture and template matching functions. There seems like there could be a dependency conflict for installing this, so instead of trying to installing it through the navigator or "conda install", install it through the Anaconda Prompt through the following command: pip install opencv-python

# Setup Nox
Due to the way templates get matched, the resolution of Nox needs to be set specifically so that the image grab is of the right size.
The resolution should be 720x1280, and for the most hassle free results, the scaling of the display resolution should just be 100% (and it should at least be 1280 height? not sure if this is fine if the horizontal version works)
One more thing to note: With FGO opened in Nox, it's best to have the spyder IDE window resized to be non-overlapping with it

# Setup BlueStacks
Alternatively, you can set up FGO on BlueStacks (this is now the preferred emulator since it's pixel perfect).
Although you can set the resolution in the BS settings, it doesn't really do anything to change the window size.
Set it to tablet (landscape) with 720x1280 resolution anyway.
The way the farmbot.py script is currently set up to work, it'll resize the window so that the FGO content is 720x1280

# Loading/activating scripts
Although farmbot.py is where most of the functionality is, because there's a bunch of different nodes to farm, the actual farming scripts that you'll want to run are separate files (now located in /nodes/).
These files (e.g. arakawa.py) are structured to first import the farmbot.py functions, and then define a Farmer specific to the relevant node (Note: whatever you name the class at the top of the script should be the same name used in the "farmer = Class_Name()" at the bottom of the file)
This will consist of the individual waves and an outer loop that controls running through the waves in order and refilling between nodes and stuff.
For the most part, you won't need to edit anything in farmbot.py (except for adding new CE templates), and just focus on the functions called within the waves and various settings on which CEs to take, and what to refill with

From the spyder IDE, these files can be run simply by using the run button in the top banner
(Note: this will simply activate the script not start the actual farming, but will locate where Nox is on the screen and move the mouse to the top-left corner of the menu bar to indicate that it found the nox window)
Note: if restarting a script takes forever, it may be due to autoreload issues (you can disable this by unsetting the User Module Reloader (UMR) option for the python interpreter in preferences)

# Calibrating the screen grab
The menu bar size may be different on some combinations of nox and display size (around line 37 of the farmbot.py file should have a place you can swap out the numbers)
Something that can help with setting up Nox is that after you have FGO running on Nox, just activate any farming script (e.g. arakawa.py)
After this, you can run the command (without quotes): "farmer.screen.dispframe()" to see what the farmbot is seeing (Note: press any key to exit out of the displayed image instead of pressing the 'X' in the top right, as that'll hang the program and make you have to restart the IDE to reset it)
For whatever reason, the correct image you'll want has a single pixel width black line all around it.
For bluestacks, it's currently calibrated to a menu bar of 41 pixels, hopefully it'll work on other machines...

# Editing scripts (outer loop)
The settings that should need to be changed should be pretty minimal.
In a farming script (e.g. arakawa.py), after the "def farm(self,nruns=1)" line, there's a number of things to change
The refill type can be one of [rapple,gapple,sapple,bapple]
The support CE depends on the templates available (located in the folder templates/noxfull/ce), and will probably be something like "davincisoc" for the Da Vinci lotto
If you don't care what support CE is brought, you can also use "first" for this setting (what happens is that if the CE isn't found in the first two supports shown, the script will refresh the support list until it finds one)
There is an optional "self.saveframe = True" line you can put to save screenshots of the drops (if this line isn't there, this variable just defaults to False. (screenshots are saved in the "frames" folder)
In some of the included files, there's an additonal "farmalarm" function after the "farm" function. This is because Nox crashes, and in the case of a timeout (or regular exit), plays an alarm sound to let you know of a crash in case you're not looking, or sleeping.

# Editing scripts (waves)
For the main waves, there are a number of things to edit (e.g. using a skill, swapping using plugsuit, and which NPs/cards to use to clear the wave)

The main block of lines to add/edit is for using skills, and this will look like:
```
	res = self.useskill(self.xy_skillc2)
	if res < 0:
	  return -1
```  
This main block is basically copied/pasted as needed, with the things to edit being the argument that tells the function which skill to use (if you're curious, the res assignment and the check is included so that if you press F6 to exit out at that point in the script, it'll break out of the farming loop)
The ordering of your servants are: A, B, C (and skills 1,2,3) from left to right on the screen.
The above example will activate skill 2 of servant C

To use an MC skill, the code block is slightly different:
```
	res = self.usemcskill(self.xy_mcskill1)
	if res < 0:
	  return -1
```	  
This will activate MC skill 1 (from left to right)

To use the plugsuit swap specifically, the code block is:
```
	res = self.plugsuit(self.xy_swap3,self.xy_swap4)
	if res < 0:
	  return -1
```	  
This will swap servants 3 and 4 (from left to right order)

Some skills have a target, and this code block looks like the following (this should be used after a regular servant skill or an MC skill that has a target to select):
```
	res = self.seltarget(self.xy_targetb)
	if res < 0:
	  return -1
```	  
This will select servant B

You can also select an enemy if need be:
```
	res = self.selenemy(self.xy_enemyc)
	if res < 0:
	  return -1
```	  
Unlike the order of servants, the enemy order is reversed: C, B, A (as A is the default selected enemy)
To take a closer look at what functions are available here, you can look around line 860 in the farmbot.py file

Finally, after all the skills that are needed have been pressed (if any), there's the card selection after the "attack" codeblock:
```
	self.usecard(self.xy_npa)
	self.usecard(self.xy_card2)
	self.usecard(self.xy_card3)
```	
There will always be three of these, and the options after the xy_ prefix are: [npa,npb,npc,card1,card2,card3,card4,card5], where the letters and numbers are in left to right order

# Running scripts
After you've edited and loaded the farming script following the above steps, running the script is pretty simple.
For the setup, in Nox/FGO, you'll want to open up the node, select a support, and get your team ready to start the quest.
In the console, the command to run is "farmer.farm()" to run the node one time, or "farmer.farm(100)" to run it 100 times.
If you want the farming script to play an alarm if timed out (provided the additional farmalarm function is there), you can run "farmer.farmalarm(300)" to run it 300 times or until whenever Nox crashes.
To exit out of a farming run, the key that the script is currently set to watch for is <F6>
This means that during farming, if you press F6 (you may need to hold down/press it a few times for it to register some times), it should escape from wherever between code blocks the script is at you pressed it (play around with this to get a feel of how much you need to press it, it doesn't check for it all the time, as much as I'd like)
For the "farmalarm" option, you'll have to press F6 again to exit out of the alarm. Unfortunately, it's set to check if F6 was pressed between loops of playing the alarm, so you'll have to listen to the alarm at least once (but it's short enough hopefully).

# Manual selection of support
At the bottom of the farming scripts, I have a "farmer.mainloop(farmer.farm)" line commented out.
If you want to manually select support between nodes, this option basically just wraps the "farm" function to run once, giving up control between nodes for manual input.
Here, the key it's watching for is <F5> to start each farming run (i.e. you select a support, press F5, wait until it brings you back to the support page, and repeat).
I haven't used this function in a while, but it may still work just fine.

# Adding templates
Mostly for CEs, there's a couple of places in the farmbot.py file that need to be edited/added to to let the program know where to look for any new templates.
For any given CE, you'll want to take a screenshot of the nox screen (I've just used Snipping Tool, window mode) and crop out the CE (because of weird scaling effects on Nox, you'll need to crop out both the CE in the first slot and the second slot).
The screenshots I save in "screencaps/noxfull" folder, and the CE templates in the "templates/noxfull/ce" folder.
To get the dimensions of a template, there's a helper script "getrect.py" that draws a box around where the template is in the screenshot.
For the CE templates though, I use the same windows for all CEs, so as a sanity check, make sure the output of the getrect.py script matches the following windows:
	self.window_support1ce = (52, 327, 209, 371)
	self.window_support2ce = (52, 526, 209, 570)
