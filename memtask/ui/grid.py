from psychopy import core, event
from components import Buttons

class gridPresent(Buttons):
    def __call__(self, item, dur=2, color_change = "red", **kwargs):
        item = int(item) # item is a number indicating location on the grid
        self.setFillColor(self.stimList[item], color=color_change) # change color of one of the squares
        self.draw(drawText = False) 
        self.win.flip()
        core.wait(dur)
        self.setFillColor(self.stimList[item], color=self.win.color)
        
class gridRecall(Buttons):
    def __call__(self, item, dur=2, **kwargs):
        myMouse = event.Mouse(win = self.win)
        self.setAutoDraw(drawText=False) #Display all squares w/o the text
        for stim in self.stimList[-3:]: #Display text of the option squares (the final 3 in the stim list)
            stim.Text.setAutoDraw(True)
        self.prompt.setAutoDraw(True) #Show instructions, defined outside of this object
        self.win.flip()
        myMouse.clickReset()
        resps = []
        respsRT = []
        while not self.done: #Loop until self.done --> when'submit' is pressed
            click, time = myMouse.getPressed(getTime=True) #record type of click and time since last click
            if click[0] and time[0]:
                x,y = myMouse.getPos() #Get position of mouse (when its been clicked)
                sel = self.selButtons(x,y) 
                if sel:
                    stim, stimLab = sel #stim = a wordbox objcet; stimLab = the name of button or the position in the grid
                    resps.append(stimLab)
                    response = self.method(stim,self.respNum, self.win) #Respond to mouse click
                    respsRT.append(time[0])
                    self.draw(drawRect = True, drawText = None) #Display updated grid
                    self.win.flip()
                    myMouse.clickReset()
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
