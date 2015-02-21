from psychopy import core, event
from components import Buttons

class gridPresent(Buttons):

    def __init__(self,win, prompt, pos, wdth, hght, txt, frame_dur=None, dur=2, color_change = "red",kwargsList = None, txtKwargs = None, **kwargs):
        """
        Parameters:
            win: a visual.Window
            prompt: optional TextStim that can be instructions, could be None
            pos: list of positions for each cell
            wdth: list of widths of each cell
            hght: list of heights of each cell
            txt: list of text inside each cell
            frame_dur: (More precise method of dur) length of time grid is highlighted for this many frames, default is None, if specified, it supersedes dur
            dur: length of time grid is highlighted in sec
            color_change: the color the squares should change to
            kwargsList: list of dictionary to be passed as kwargs to each Rect stim within WordBox
            txtKwargs: list of dictionary to be passed as kwargs to each text stim within WordBox
            kwargs: if kwargsList not given, kwargs is used instead
        return: creates grid to be reused throughout, whenever it is is called
        """
        Buttons.__init__(self, win, prompt, pos, wdth, hght, txt, kwargsList = None, txtKwargs = None, **kwargs)
        self.frame_dur = frame_dur
        self.dur = dur
        self.color_change = color_change
    def __call__(self, item,  **kwargs):
        """
        Parameters:
            item:  a number indicating location on the grid (0:number of boxes-1)
            dur: length of time grid is highlighted
            kwargs:
        return: Presents screen with one square highlighted
        """
        item = int(item) # change to int if item is read in as a string
        self.setFillColor(self.stimList[item], color=self.color_change) # change color of one of the squares
        if self.frame_dur: #if number of frames for presentation is specified
            for frameN in range(self.frame_dur):
                self.draw(drawText = False)
            self.win.flip()
        else:
            self.draw(drawText = False)
            self.win.flip()
            core.wait(self.dur)
        self.setFillColor(self.stimList[item], color=self.win.color)
        
class gridRecall(Buttons):
     def __init__(self,win, prompt, pos, wdth, hght, txt, kwargsList = None, txtKwargs = None, **kwargs):
        """
        Parameters:
            win: a visual.Window
            prompt: optional TextStim that can be instructions, could be None
            pos: list of positions for each cell
            wdth: list of widths of each cell
            hght: list of heights of each cell
            txt: list of text inside each cell
            frame_dur: (More precise method of dur) length of time grid is highlighted for this many frames, default is None, if specified, it supersedes dur
            dur: length of time grid is highlighted in sec
            color_change: the color the squares should change to
            kwargsList: list of dictionary to be passed as kwargs to each Rect stim within WordBox
            txtKwargs: list of dictionary to be passed as kwargs to each text stim within WordBox
            kwargs: if kwargsList not given, kwargs is used instead
        return: creates grid to be reused throughout, whenever it is is called
        """
        Buttons.__init__(self, win, prompt, pos, wdth, hght, txt, kwargsList = None, txtKwargs = None, **kwargs)
        self.myMouse = event.Mouse(win=win)

     def __call__(self, **kwargs):
        """
        Parameters:
            kwargs: Absorb whatever params are inputed
        return: Display and Record a Recall Grid
        """
        self.setAutoDraw(drawText=False) #Display all squares w/o the text
        for stim in self.stimList[-3:]: #Display text of the option squares (the final 3 in the stim list)
            stim.Text.setAutoDraw(True)
        self.prompt.setAutoDraw(True) #Show instructions, defined outside of this object
        self.win.flip()
        self.myMouse.clickReset()
        resps = []
        respsRT = []
        while not self.done: #Loop until self.done --> when'submit' is pressed
            click, time = self.myMouse.getPressed(getTime=True) #record type of click and time since last click
            if click[0] and time[0]:
                x,y = self.myMouse.getPos() #Get position of mouse (when its been clicked)
                sel = self.selButtons(x,y) 
                if sel:
                    stim, stimLab = sel #stim = a wordbox objcet; stimLab = the name of button or the position in the grid
                    resps.append(stimLab)
                    response = self.method(stim,self.respNum, self.win) #Respond to mouse click
                    respsRT.append(time[0])
                    self.draw(drawRect = True, drawText = None) #Display updated grid
                    self.win.flip()
                    self.myMouse.clickReset()
        self.prompt.setAutoDraw(False)
        self.reset()
        print resps, respsRT #TODO How to save this info
        
     def method(self, stim, stimNum, win):
        if stim.Text.text == "Clear":
            for entry in self.stimList[:-3]:
                entry.Rect.setFillColor(win.color, 'rgb')
                entry.Text.text = "0"
                entry.Text.setAutoDraw(False)
            self.respNum = 1
        elif stim.Text.text == "Submit":
            self.done = True
        elif stim.Text.text == "Blank":
            self.respNum += 1
        elif stim.Text.text == "0":
            stim.Rect.setFillColor("red")
            stim.Text.setText(self.respNum)
            stim.Text.setAutoDraw(True)
            self.respNum += 1
            return stim, stimNum
        else: return None
        return stim, stim.Text.text
