from pandas import DataFrame
from memtask.grid import genSpatialGrid
from memtask.proc_grid import gridRecall, run_task
from memtask.sentence_distract import SentenceDistractor
from memtask.proc import ProcShow
from psychopy import visual

df = DataFrame.from_csv('example/trials/complex_span.csv')
win = visual.Window([800,600],units="pix")
recPrompt = "Select the blocks in order.  Use the blank button to skip forgotten blocks."
Prompt = visual.TextStim(win, text =  recPrompt, pos = (0, 250), color = "black")
Spos, Swdth, Shght, Stxt = genSpatialGrid(400*1.15,400,4,4)    #Create grid without options buttons
P = ProcShow(win)
Rpos, Rwdth, Rhght, Rtxt = genSpatialGrid(400,400,4,4, optWdth = 100, optHght = 50, optDist = 50)
R = gridRecall(win, Prompt, Rpos, Rwdth, Rhght, Rtxt,
               txtKwargs = {"color": "black"},
               lineColor = "black", fillColor = win.color, interpolate = False)
D = SentenceDistractor(win)
proc_dict = {'learn': P,
                 'recall': R,
                 'dist': D
                 }


run_task([row for ii, row in df.iterrows()], proc_dict)
