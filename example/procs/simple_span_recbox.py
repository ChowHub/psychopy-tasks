from psychopy import visual
from pandas import DataFrame
from memtask.proc import ProcShow, RecBoxMenu, run_task
df = DataFrame.from_csv('example/trials/simple_span.csv')
win = visual.Window([800,600])
P = ProcShow(win)
R = RecBoxMenu(win, 4)
proc_dict = {'learn': P,
             'recall': R
            }

run_task([row for ii, row in df.iterrows()], proc_dict)
