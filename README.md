# farmbot.py

Setup instructions for farmbot.py (on windows 10).

**ALWAYS SET UP YOUR BIND CODE AFTER TRANSFERING BETWEEN DEVICES**

# Install python
I like the anaconda distribution since it comes with the spyder IDE that lets me load/edit/run files all within the same program (found here: https://www.anaconda.com/distribution/).

During the installation, something that may trip up the executables is selecting between a local (user only "Just Me" option) install vs a global (all users) install. It's recommended to do the user only installation as that'll keep everything sandboxed within your own user folders and installation of packages won't need extra administrator permissions (it'll go in C:\Users\UserName\Anaconda3). It also makes uninstalling easier.

Once installed, try opening spyder as a sanity check (the application should just work...). The left large window is the editor, and this is where you'll open/edit files. The bottom right window is the console, and this is where you'll be running commands from the farming scripts.

Although the base installation installs quite a few needed python packages, there are some additional ones that'll need to be installed. The import list in the farmbot.py file should let you know what's needed. An easy way to check if you have all the dependencies installed is to open up that file in the editor and run it. It doesn't do anything noticeable if it all works correctly, but if some of the depencencies aren't there, it'll display something like a module missing error in the console.

You can install the necessary packages through the Anaconda Navigator (search packages tab) or through the Anaconda prompt using "conda install"
 - `pillow` is the thing you'd need to search for if PIL isn't installed (but it should be)
 - `pywin32` is the one you need for the windows mouse emulation and stuff (but it should be)
 - `opencv` is the thing you'll need for all the image capture and template matching functions. There seems like there could be a dependency conflict for installing this, so instead of trying to installing it through the navigator or "conda install", install it through the Anaconda Prompt through the following command: `pip install opencv-python`

# Setting up emulator
The farmbot.py was originally developed for use with samsung flow, but that got depricated fast. Then it was developed for use with Nox for a while, until updates happened and the game kept crashing. It's currently being developed for use with Bluestacks, and that's where all the newer templates are. When the emulators are running, it's best to have the Spyder IDE window resized to be non-overlapping with it.

## Setup BlueStacks
This is the preferred (and currently only supported) emulator since it's pixel perfect. Although you can set the resolution in the BlueStacks settings, it doesn't really do anything to change the window size. But you can set it to tablet (landscape) with 720x1280 resolution anyway. The way the farmbot.py script is currently set up to work, it'll resize the window so that the content is 720x1280.

## Setup Nox
Alternatively, you can try to set Nox (but you'll have to get your own templates and stuff). Due to the way templates get matched, the resolution of Nox needs to be set specifically so that the image grab is of the right size. The resolution should be 720x1280, and for the most hassle free results, the scaling of the display resolution should just be 100%. There's some weird cases where if the height of the display is too short, the size of the menu bar is rescaled, and this will mess with the screen grab.

## Calibrating the screen grab
The menu bar size may be different on some combinations of nox and display size (around line 37 of the farmbot.py file should have a place you can swap out the numbers).

Something that can help with setting up Nox is that after you have FGO running, just activate any farming script (e.g. arakawa.py).
After this, you can run the command (in the Spyder console): `farmer.screen.dispframe()` to see what the farmbot is seeing (Note: press any key to exit out of the displayed image instead of pressing the 'X' in the top right, as that'll hang the program and make you have to restart the IDE to reset it).

For nox, the correct image you'll want has a single pixel width black line all around it (its scaling is bad).
For bluestacks, it's currently calibrated to a menu bar height of 41 pixels, and hopefully you don't have to change this.

# Using the farming scripts
Although farmbot.py is where most of the functionality is, because there's a bunch of different nodes to farm, the actual farming scripts that you'll want to run are separate files (located in /nodes/).

## Loading/activating scripts
These files (e.g. arakawa.py) are structured to first import the farmbot.py functions, and then define a Farmer specific to the relevant node (Note: whatever you name the class at the top of the script should be the same name used in the `farmer = Class_Name()` at the bottom of the file).
This will consist of the individual waves and an outer loop that controls running through the waves in order and refilling between nodes and stuff.
For the most part, you won't need to edit anything in farmbot.py (except for adding new CE templates), and just focus on the functions called within the waves and various settings on which CEs to take, and what to refill with.

From the spyder IDE, these files can be run simply by using the run button in the top banner. Note: this will simply activate the script, not start the actual farming, but will locate where Nox/BS is on the screen and move the mouse to the top-left corner of the menu bar to indicate that it found the emulator window.

## Editing scripts (outer loop)
The settings that should need to be changed should be pretty minimal.
In a farming script (e.g. arakawa.py), after the `def farm(self,nruns=1)` line, there's a number of things to change:
 - The refill type can be one of: `[rapple,gapple,sapple,bapple]` (you should be able to guess what these refer to)
 - The support CE depends on the templates available (located in the folder templates/blue/ce), and will probably be something like "davincisoc" for the Da Vinci lotto, or "lunchtime" in general. If you don't care what support CE is brought, you can also use "none" for this setting.
 - There's also the option for a support servant (templates available in templates/blue/servant), which is only "waver" for now. You can set this if you don't care about the CE, but need a specific servant from the support list. (Note: combining both a servant and a ce will make sure only those combinations are selected, and the script will update the support list until a match is found).
 - There is an optional `self.saveframe = True` line you can put to save screenshots of the drops (if this line isn't there, this variable just defaults to False. Screenshots are saved in the "frames" folder.
 - In some of the included files, there's an additonal `farmalarm` function after the `farm` function. This was added because of Nox crashes, and in the case of a timeout (or regular exit), the script plays an alarm sound to let you know of a crash in case you're not looking (or sleeping).

## Editing scripts (waves)
For the main waves, there are a number of things to edit (e.g. using a skill, swapping using plugsuit, and which NPs/cards to use to clear the wave)

### Use skill
The main block of lines to add/edit is for using skills, and this will look like:
```python
res = self.useskill(self.xy_skillc2)
if res < 0:
  return -1
```  
This main block is basically copied/pasted as needed, with the things to edit being the argument that tells the function which skill to use (Note: the res assignment and the check is included so that if you press F6 to exit out at that point in the script, it'll break out of the farming loop).

The ordering of your servants are: A, B, C (and skills 1,2,3) from left to right on the screen. The above example will activate skill 2 of servant C.

### MC skill
To use an MC skill, the code block is slightly different:
```python
res = self.usemcskill(self.xy_mcskill1)
if res < 0:
  return -1
```
This will activate MC skill 1 (from left to right)

### Plugsuit skill
To use the plugsuit swap specifically, the code block is:
```python
res = self.plugsuit(self.xy_swap3,self.xy_swap4)
if res < 0:
  return -1
```
This will swap servants 3 and 4 (from left to right order)

### Targeted skills
Some skills have a target, and this code block looks like the following (this should be used after a regular servant skill or an MC skill that has a target to select):
```python
res = self.seltarget(self.xy_targetb)
if res < 0:
  return -1
```
This will select servant B

### Target enemy
You can also select an enemy if need be:
```python
res = self.selenemy(self.xy_enemyc)
if res < 0:
  return -1
```
Unlike the order of servants, the enemy order is reversed: C, B, A (as A is the default selected enemy)

### Attack card selection
Finally, after all the skills that are needed have been pressed (if any), there's the card selection after the "attack" codeblock:
```python
self.usecard(self.xy_npa)
self.usecard(self.xy_card2)
self.usecard(self.xy_card3)
```
There will always be three of these, and the options after the xy_ prefix are: `[npa,npb,npc,card1,card2,card3,card4,card5]`, where the letters and numbers are in left to right order.

## Running scripts
After you've edited and loaded the farming script following the above steps, running the script is pretty simple. For the setup, in BS/FGO, you'll want to open up the node, select a support, and get your team ready to start the quest.

In the console, the command to run is `farmer.farm()` to run the node one time, or `farmer.farm(100)` to run it 100 times.
If you want the farming script to play an alarm if timed out (provided the additional farmalarm function is there), you can run `farmer.farmalarm(300)` to run it 300 times or until whenever Nox crashes.
Since the introduction of repeating quests, after running the farm command, click on the "start quest" button to get things started (the script no longer needs to handle exiting out to menu and reselecting the node between quests, it goes directly into a quest after selecting a new support).

To exit out of a farming run, the key that the script is currently set to watch for is `<F6>`
This means that during farming, if you press F6 (you may need to hold down/press it a few times for it to register some times), it should escape from wherever between code blocks the script is at you pressed it (play around with this to get a feel of how much you need to press it, it doesn't check for it all the time, as much as I'd like).

For the "farmalarm" option, you'll have to press F6 again to exit out of the alarm. Unfortunately, it's set to check if F6 was pressed between loops of playing the alarm, so you'll have to listen to the alarm at least once (but it's short enough hopefully). BlueStacks doesn't crash like Nox does, so I haven't needed to use this in a while.

## Manual selection of support
At the bottom of the farming scripts, I have a `farmer.mainloop(farmer.farm)` line commented out. If you want to manually select support between nodes, this option basically just wraps the "farm" function to run once, giving up control between nodes for manual input. Here, the key it's watching for is <F5> to start each farming run (i.e. you select a support, press F5, wait until it brings you back to the support page, and repeat).
I haven't used this function in a while, it's probably broken at the moment.

# Adding templates
Mostly for CEs, there's a couple of places in the farmbot.py file that need to be edited/added to to let the program know where to look for any new templates (marked by TODO).

For any given CE, you'll want to take a screenshot of the game screen (the easiest way is `farmer.screen.saveframe()`). This will be saved in the "frames" folder automatically, but you can move it out to the "screenshots" folder. Open it up in something like GIMP and crop out the CE (Note: because of weird scaling effects on Nox, you'll need to crop out both the CE in the first slot and the second slot). For bluestacks, the dimensions should be 158x45px.

## CE template windows
To get the window of where the template should be matched, there's a helper script "getrect.py" that draws a box around where the template is in the screenshot.
For the CE templates, I use the same windows for all CEs, so as a sanity check, make sure the output of the getrect.py script matches the following windows (for Nox):
```python
self.window_support1ce = (52, 327, 209, 371)
self.window_support2ce = (52, 526, 209, 570)
```
For BlueStacks, since the templates are pixel perfect, something grabbed in support slot 1 should also work in support slot 2. In any case the windows to check for are:
```python
self.window_support1ce = (51, 326, 209, 371)
self.window_support2ce = (51, 526, 209, 571)
```

# Other games
Although the main game that the farmbot was developed for was FGO (since there's no autofarming option), the scripts can be adapted to other games as well, as long as the right templates to match for are collected and the right control logic for repeating nodes is made. Getting locations to click and templates to match and how to go from one to the next is basically the way to edit the script for something new (maybe take a look at the MR scripts for ideas). Note: since the original development was for samsung flow at a resolution of 640x360px, most of the locations are defaulted on this grid and scaled up to the 1280x720px resolution.
