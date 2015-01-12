import pandas as pd
from string import ascii_uppercase as LETTERS
import random

def simple_span_trial(items):
    trial = [{'in': ii, 'item': item, 'mode': 'learn'} for ii, item in enumerate(items)]
    trial.append({'mode': 'recall'})
    return trial

def complex_span_trial(N_mem, N_dist):
    trial = []
    for ii in range(N_mem):
        trial.append({'in': ii, 
                      'item': 'memory ' + LETTERS[ii], 
                      'mode': 'learn'
                      })

        for jj in range(N_dist): 
            trial.append({'in': ii,
                        'item': 'dist ' + LETTERS[jj],
                        'corr': random.random() > .5,
                        'mode': 'dist'
                        })

    trial.append({'mode': 'recall'})        
    return trial
