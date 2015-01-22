from psychopy import visual, core, event

class SentenceDistractor(object):
    def __init__(self, win, test = None, stim=None):
        self.stim = visual.TextStim(win=win) if not stim else stim
        self.win = win
        self.test = test
        self.tally = (0,0)
        self.instruct1 = visual.TextStim(win=self.win, text="Click mouse when ready to continue.", pos= (0,-100))

    def __call__(self, corr, item, **kwargs):
        """Takes item and corr, displays item,
        waits for a mouse click, and then asks whether it was True/False,
        verifies whether the response was correct"""
        self.stim.text = item
        myMouse = event.Mouse(win = self.win)
        click, time = myMouse.getPressed(getTime=True)
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
            if corr:
                if "t" in key_presses:
                    print "Correct"
                    self.track_score(True)
                else:
                    print "Incorrect"
                    self.track_score(False)
            else:
                if "f" in key_presses:
                    print "Correct"
                    self.track_score(True)
                else:
                    print "Incorrect"
                    self.track_score(False)
        else:
            self.test(corr)

    def track_score(self, corr_resp):
        correct, total = self.tally
        if corr_resp:
            correct += 1
        total += 1
        self.tally = (correct, total)
        print self.tally








