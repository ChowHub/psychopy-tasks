from psychopy import visual, event

class CntrlDistractor(object):
    def __init__(self):
        self.correct = 0
        self.total = 0

    def update_score(self, corr_resp):
        self.total += 1
        if corr_resp: self.correct += 1
        print self.total, self.correct

class SentenceDistractor(object):
    def __init__(self, win, test = None, stim=None, controller=None):
        self.stim = visual.TextStim(win=win) if not stim else stim
        self.win = win
        self.mouse = event.Mouse(win = self.win)
        self.test = test
        self.instruct1 = visual.TextStim(win=self.win, text="Click mouse when ready to continue.", pos= (0,-100))
        self.controller = controller

    def __call__(self, corr, item, **kwargs):
        """Takes item and corr, displays item,
        waits for a mouse click, and then asks whether it was True/False,
        verifies whether the response was correct"""
        self.stim.text = item
        click, time = self.mouse.getPressed(getTime=True)
        while not click[0]:
            self.stim.draw()
            self.instruct1.draw()
            self.win.flip()
        print time[0]
        if self.test is None:
            instruct = visual.TextStim(win=self.win, text="Hit 't' for true or 'f' for false.")
            key_presses = []
            while 't' not in key_presses and 'f' not in key_presses:
                instruct.draw()
                self.win.flip()
                key_presses = event.waitKeys()
            # Score Response
            score_resp = corr == ("t" in key_presses)
            print "Correct" if score_resp else "Incorrect"
            if self.controller: self.controller.update_score(score_resp)
        else:
            self.test(corr)

