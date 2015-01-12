from psychopy import visual, core, event

class ProcShow(object):
    def __init__(self, win, stim=None):
        self.stim = visual.TextStim(win=win) if not stim else stim
        self.clock = core.Clock()
        self.win = win

    def __call__(self, item, dur=2, **kwargs):
        # load item into stim
        self.stim.text = item
        t = 0
        self.clock.reset()
        while t < 2:
            self.stim.draw()
            self.win.flip()
            t = self.clock.getTime()

def fixKeys(string, filt=True):
    """Put strings over 1 char long in bracks (e.g. tab -> {tab}). If filt is 
    True, return empty string if over 1 char."""
    if type(string)==list: string = string[0]
    if len(string) <= 1: return string
    elif filt: return ''
    else: return '{' + string + '}'

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
        while True:
            new = event.waitKeys()
            print new
            if new[0] in exitkeys: break
            elif new[0] == 'backspace':
                ans = ans[:-1]
            else: ans.extend(fixKeys(new,filt=True))
            self.stims['resp'].setText("".join(ans) + suf)
            self.stims['resp'].draw()
            self.win.flip()
        #remove suffix
        self.stims['resp'].setText("".join(ans))
        self.win.flip()

        self.ans = ans
        return new[0]

    def set(self, method, val):
        for stim in self.stims.values():
            getattr(stim, method)(val)

    def reset(self):
        """Reset class.  Reinitializes, so may produce unexpected behavior if referencing stim
        objects directly.

        """
        self.__init__(**self.kwargs)

def run_task(design, proc_dict):
    for row in design:
        proc = proc_dict[row['mode']]
        proc(**row)

if __name__ == '__main__':
    from pandas import DataFrame
    df = DataFrame.from_csv('example/trials/simple_span.csv')
    win = visual.Window([800,600])
    P = ProcShow(win)
    R = RecBox(win, pos = [0, 0])
    proc_dict = {'learn': P,
                 'recall': R
                 }

    run_task([row for ii, row in df.iterrows()], proc_dict)
