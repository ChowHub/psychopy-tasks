from psychopy import visual, core, event
from grid import genSpatialGrid, WordBox, Buttons, RecButtons

import os
os.chdir('..')



class gridPresent(Buttons):
    def __call__(self, item, dur=2, color_change = "red", **kwargs):
        item = int(item) # item is a number indicating location on the grid
        self.setFillColor(self.stimList[item], color=color_change) # change color of one of the squares
        self.draw(drawText = False) 
        win.flip()
        core.wait(dur)
        self.setFillColor(self.stimList[item], color=win.color)
    def update(self, item, gridRecall):
        """With each call track the squares that have been called in the current trial"""
        pass
        
class gridRecall(RecButtons):
    def __call__(self, item, dur=2, **kwargs):
        self.setAutoDraw(drawText=False) #Display all squares w/o the text
        for stim in self.stimList[-3:]: #Display text of the option squares (the final 3 in the stim list)
            stim.Text.setAutoDraw(True)
        Prompt.setAutoDraw(True) #Show instructions, defined outside of this object
        win.flip()
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
                    response = self.method(stim,self.respNum, win) #Respond to mouse click
                    respsRT.append(time[0])
                    self.draw(drawRect = True, drawText = None) #Display updated grid
                    win.flip()
                    myMouse.clickReset()
        Prompt.setAutoDraw(False)
        self.reset()
        print resps, respsRT #TODO How to save this info
        
        


def run_task(design, proc_dict):
    for row in design:
        proc = proc_dict[row['mode']]
        proc(**row)


if __name__ == '__main__':
    from pandas import DataFrame
    df = DataFrame.from_csv('example/trials/spatial_span.csv')
    win = visual.Window([800,600],units="pix")
    myMouse = event.Mouse(win = win)
    recPrompt = "Select the blocks in order.  Use the blank button to skip forgotten blocks."
    Prompt = visual.TextStim(win, text =  recPrompt, pos = (0, 250), color = "black")
    Spos, Swdth, Shght, Stxt = genSpatialGrid(400*1.15,400,4,4)    #Create grid without options buttons
    P = gridPresent(win,
                    Spos, Swdth, Shght, Stxt,
                    txtKwargs = {"color":"black"},
                    lineColor = "black", lineWidth = 3, interpolate = False)
    Rpos, Rwdth, Rhght, Rtxt = genSpatialGrid(400,400,4,4, optWdth = 100, optHght = 50, optDist = 50)
    R = gridRecall(win, Rpos, Rwdth, Rhght, Rtxt,
               txtKwargs = {"color": "black"},
               lineColor = "black", fillColor = win.color, interpolate = False)
    proc_dict = {'learn': P,
                 'recall': R
                 }

    run_task([row for ii, row in df.iterrows()], proc_dict)