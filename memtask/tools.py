def fixKeys(string, filt=True):
    """Put strings over 1 char long in bracks (e.g. tab -> {tab}). If filt is 
    True, return empty string if over 1 char."""
    if type(string)==list: string = string[0]
    if len(string) <= 1: return string
    elif filt: return ''
    else: return '{' + string + '}'

def run_task(design, proc_dict):
    """Loop through design, feeding each entry as kwargs to proc in mode column"""
    for row in design:
        proc = proc_dict[row['mode']]
        #args = getargspec(proc) if isclass
        proc(**row)

