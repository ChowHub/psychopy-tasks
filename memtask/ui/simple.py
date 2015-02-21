from psychopy import visual, core, event
from memtask.tools import fixKeys

class ProcShow(object):
    """Procedure for displaying a psychopy stim object for either..
        (1) some duration of time
        (2) until a the mouse is clicked
    """
    def __init__(self, win, stim=None):
        """Initialize with psychopy components needed"""
        self.stim = visual.TextStim(win=win) if not stim else stim
        self.clock = core.Clock()
        self.win = win
        self.mouse = event.Mouse(win = win)

    def __call__(self, item, dur=None, **kwargs):
        """Display item on screen for dur seconds or until mouseclick.

        Parameters:
            item:   text to be presented on screen
            dur :   length of time in seconds to present. If False waits for mouse click.
        """
        # load item into stim
        self.stim.text = item
        t = 0
        self.clock.reset()
        if dur: 
            while t < dur:
                self.stim.draw()
                self.win.flip()
                t = self.clock.getTime()
        else:
            click, time = self.mouse.getPressed(getTime=True)
            while not click[0]:
                self.stim.draw()
                self.win.flip()

class ProcVer(object):
    """Procedure for prompting the user to click a button"""
    def __init__(self, win, myMouse, TxtStim, VerScreen):
        """Initialize with psychopy stims.

        Parameters:
            TxtStim  :  psychopy text stim object
            VerScreen:  memtask.Button object
        """
        self.win, self.myMouse, self.TxtStim, self.VerScreen = win, myMouse, TxtStim, VerScreen

    def __call__(self, ans_probe):
        return self.proc(self.win, self.myMouse, ans_probe, self.TxtStim, self.VerScreen)

    @staticmethod
    def proc(win, myMouse, ans_probe, TxtStim, VerScreen):
        TxtStim.setText(ans_probe)
        TxtStim.draw()
        VerScreen.draw()
        win.flip()
        myMouse.clickReset()                                        #TODO: replace with waitscreen
        lastTime = myMouse.getPressed(getTime = True)[1][0]
        ans = None
        while not VerScreen.done:
            click, time = myMouse.getPressed(getTime=True)
            if click[0] and time[0] != lastTime:
                x,y = myMouse.getPos()
                ans = VerScreen.selButtons(x,y)
                lastTime = time[0]
        VerScreen.reset()
        #return ans == "True", lastTime


class RecBox():
    def __init__(self, win, pos):
            self.stims = dict(box = visual.Rect(win, lineWidth=1.0, fillColor='grey', width=1, height=.12),
                              resp = visual.TextStim(win, font="Courier", wrapWidth=400, text='')
                             )
            self.stims['resp'].setPos(pos)
            self.stims['box'].setPos(pos)
            self.win = win
            self.ans = [""]
            self.kwargs = dict(win=win, pos=pos)


    def __call__(self, maxViewingTime = 100000, exitkeys=['return'], **kwargs):
        for stim in self.stims.values(): stim.setAutoDraw(True)

        ans = self.ans
        suf = "_"
        new = [""]
        while True:
            print new
            if new[0] in exitkeys: break
            elif new[0] == 'backspace':
                ans = ans[:-1]
            else: ans.extend(fixKeys(new,filt=True))
            self.stims['resp'].setText("".join(ans) + suf)
            self.stims['resp'].draw()
            self.win.flip()
            new = event.waitKeys()
        #remove suffix
        self.stims['resp'].setText("".join(ans))
        self.win.flip()

        self.ans = ans
        return new[0]

    def reset(self):
        """Reset class.  Reinitializes, so may produce unexpected behavior if referencing stim
        objects directly.

        """
        self.__init__(**self.kwargs)

    def draw(self):
        for stim in self.stims.values(): stim.draw()

    def setAutoDraw(self, val):
        for stim in self.stims.values(): stim.setAutoDraw(val)


class RecBoxMenu(object):
    def __init__(self, win, N):
        self.fields = [RecBox(win, [0, -hght / 3.]) for hght in range(N)]

    def __call__(self, **kwargs):
        for field in self.fields: field.setAutoDraw(True)
        ii = 0
        while ii < len(self.fields):
            field = self.fields[ii]
            exitkey = field(exitkeys=['return', 'up', 'down'])
            if exitkey == 'up' and ii != 0: 
                ii -= 1
            else: 
                ii += 1
