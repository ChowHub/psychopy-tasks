from pandas import DataFrame
from memtask.proc import ProcShow, RecBox, run_task
from psychopy import visual, core, event

df = DataFrame.from_csv('example/trials/simple_span.csv')
print df
win = visual.Window([800,600])
P = ProcShow(win)
R = RecBox(win, pos = [0, 0])
proc_dict = {'learn': P,
             'recall': R
             }
run_task([row for ii, row in df.iterrows()], proc_dict)