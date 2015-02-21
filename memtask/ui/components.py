from psychopy import visual

class WordBox:
    '''Convenience class, combining visual.ShapeStim and visual.TextStim'''
    def __init__(self, win, wdth, hght, TextStim = None, moveText=True, cntrRec = False, **kwargs):
        self.Rect = visual.ShapeStim(win,
                                     vertices = [( 0      , -hght),
                                                 ( wdth   , -hght),
                                                 ( wdth   , 0,),
                                                 ( 0      , 0)],
                                     **kwargs
                                     )
        if cntrRec: self.Rect.setPos((self.Rect.pos[0] - wdth/2., self.Rect.pos[1] + hght/2.))
        if TextStim:
            if moveText: TextStim.setPos((self.Rect.pos[0] + wdth/2., self.Rect.pos[1] - hght/2.))
        self.Text = TextStim
        self.wdth = wdth
        self.hght = hght
        self.win = win
        self.pos = self.Rect.pos
    def setAutoDraw(self, drawRect = True, drawText = True):
        if drawRect != None: self.Rect.setAutoDraw(drawRect)
        if self.Text!= None: self.Text.setAutoDraw(drawText)
    def setPos(self, pos):
        self.Rect.pos = pos
        if self.Text: self.Text.pos = (pos[0] + self.wdth, pos[1] + self.hght)
    def draw(self, drawRect = True, drawText = True):
        if drawRect: self.Rect.draw()
        if drawText: self.Text.draw()


class Buttons:
    """Generic class for selecting and interacting with rectangular objects.
    Draws N boxes with pos as top-left position, using WordBox class. Can check for mouse click within box, and respond with the
    function method().  All objects are stored as a list.

    TODO: remove hard-coded in that if text is "0", then draw differently (was done for spatial span).
          
    """
    def __init__(self, win, prompt, pos, wdth, hght, txt, kwargsList = None, txtKwargs = None, **kwargs):
        """
        Parameters:
            prompt:     unused?
            pos:        list of positions for each cell
            wdth:       list of widths of each cell
            hght:       list of heights of each cell
            txt:        list of text inside each cell
            kwargsList: list of dictionary to be passed as kwargs to each Rect stim within WordBox
            txtKwargs:  list of dictionary to be passed as kwargs to each text stim within WordBox
            kwargs:     if kwargsList not given, kwargs is used instead

        """
        try:                                    #Ensure pos,wdth,hght,txt are iterable
            pos[0][0]
            self.pos = pos
        except: self.pos = [pos]
        self.wdth, self.hght, self.txt = [],[],[]
        try:
            self.wdth.extend(wdth)
        except TypeError: self.wdth = [wdth]
        try:
            self.hght.extend(hght)
        except TypeError: self.hght = [hght]
        if type(txt) == str: self.txt = [txt]
        else: self.txt = [entry for entry in txt]
        if kwargsList: self.kwargs = kwargsList                 #kwargs are specefied for each button, or
        else: self.kwargs = [kwargs.copy() for entry in self.pos]#shallow copy kwargs dict for each button
        if not txtKwargs: self.txtKwargs = [{} for entry in self.pos]
        elif type(txtKwargs) == list or type(txtKwargs) == tuple: self.txtKwargs = txtKwargs
        else: self.txtKwargs = [txtKwargs.copy() for entry in self.pos]
        self.win = win
        self.prompt = prompt
        self.done = False
        self.stimList = []
        self.respNum = 1
        self.genStims()

    def genStims(self):
        self.stimList = []
        for pos, wdth, hght, txt, txtKwargs, kwargs in zip(self.pos, self.wdth, self.hght, self.txt, self.txtKwargs, self.kwargs):
            oneTxt = visual.TextStim(self.win, txt, **txtKwargs)
            oneStim = WordBox(self.win, wdth, hght, TextStim = oneTxt, pos = pos, **kwargs)
            self.stimList.append(oneStim)

    def reset(self):
        self.done = False
        self.respNum = 1
        self.setAutoDraw(False, False)
        self.genStims()

    def method(self, stim, stimNum):
        '''Default method for responding to button presses.  Can / should be overloaded.'''
        self.done = True
        return stim.Text.text

    def selButtons(self, x,y):
        #for pos, wdth, hght, stimNum in zip(self.pos, self.wdth, self.hght, range(len(self.pos))):
        for stimNum, stim in enumerate(self.stimList):
            if (x > stim.pos[0] and x < (stim.pos[0] + stim.wdth) and y < stim.pos[1] and y > (stim.pos[1]-stim.hght)):
                if stim.Text.text == "0":
                    return (stim, stimNum)
                else:
                    return (stim, stim.Text.text)

    def draw(self, drawRect = True, drawText = True):
        for button in self.stimList:
            button.draw(drawRect, drawText)

    def setAutoDraw(self, drawRect = True, drawText = True):
        for button in self.stimList:
            button.setAutoDraw(drawRect, drawText)

    def erase(self):
        for button in self.stimList:
            button.setAutoDraw(False)

    def setFillColor(self, stimList = None, color = "black"):
        '''Sets fill color for a list or single stimulus from stimList.

        Sets all black by default.
        '''
        if not stimList:
            stimList = self.stimList
        if hasattr(stimList, "__len__"):
            for stim in range(len(stimList)):
                if type(color) == str: stimList[stim].Rect.setFillColor(color)
                else: stimList[stim].Rect.setFillColor(color[stim], 'rgb')
        else:
            if type(color) == str: stimList.Rect.setFillColor(color)
            else: stimList.Rect.setFillColor(color, 'rgb')


def genSpatialGrid(gridWdth, gridHght, nRow, nCol,
                optWdth = None, optHght = None, optDist = None,
                recHght = None, recWdth = None, letters = None, gridPos = (0,0)):
    """Convenience function for calculating the parameters necessary to make a grid of buttons.

    By default, cells will fit entire grid without spaces between them. If heights
    and/or widths are specified, then cells will be evenly spaced, but retain those
    dimensions.

    parameters:
        gridWdth:   overall width of grid
        gridHght:   overall height of grid
        nRow    :   number of rows in grid
        nCol    :   number of columns in grid
        optWdth :   width of option buttons
        optHght :   height of option buttons
        optDist :   Distance apart of option buttons
        recWdth :   width of main cells
        recHght :   height of main cells
        letters :   boolean, should text be moved

    TODO: refactor with function for doing calculations once, then use for width and height
    """

    #wdths and hghts are not calculated using floating point
    indWdth = recWdth if recWdth else gridWdth/nCol    # no spaces if width not given
    indHght = recHght if recHght else gridHght/nRow
    colSpace = (gridWdth - nCol * indWdth) / (nCol - 1) #0 if recWdth = None
    rowSpace = (gridHght - nRow * indHght) / (nRow - 1) #0 if recHght = None (no space between boxes)
    pos = []
    ltrPos = []
    for row in range(nRow):
        for col in range(nCol):
            pos.append((-gridWdth/2 + col*(indWdth + colSpace),       #Set no space between boxes
                        gridHght/2 - row*(indHght + rowSpace)))
            if letters:
                ltrPos.append([-gridWdth/2 + col*(indWdth + colSpace) + indWdth,
                            gridHght/2 - row*(indHght + rowSpace) - indHght/2])
    indWdth = [indWdth]* (nRow*nCol)#[gridWdth/nCol] * (nRow*nCol)      #list with wdth for each box
    indHght = [indHght]* (nRow*nCol)#gridHght/nRow] * (nRow*nCol)
    txt = ["0"] * (nRow*nCol)                    #boxes are empty
    #Add Clear, Submit, and Blank buttons
    if optWdth:
        indWdth.extend([optWdth]*3)
        indHght.extend([optHght]*3)
        pos.extend(
                    [( (-gridWdth)/2 - optWdth/2, -gridHght/2 - optDist),
                    ( ( gridWdth)/2 - optWdth/2, -gridHght/2 - optDist),
                    ( ( 0 - optWdth/2, -gridHght/2 - optDist/3))])
        txt.extend(["Clear", "Submit", "Blank"])
    if gridPos != (0,0):
        pos = [(indPos[0] + gridPos[0], indPos[1] + gridPos[1]) for indPos in pos]
        ltrPos =  [(indPos[0] + gridPos[0], indPos[1] + gridPos[1]) for indPos in ltrPos]
    if letters: return pos, indWdth, indHght, txt, ltrPos
    return pos, indWdth, indHght, txt
