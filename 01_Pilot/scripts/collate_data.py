import os, json
import numpy as np
from os.path import dirname
from pandas import DataFrame, concat
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DIR = os.path.join(ROOT_DIR, 'raw')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Main loop.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Locate files.
files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('.json')])

## Preallocate space.
METADATA = []
SURVEYS = []
DATA = []

for f in files:
    
    ## Load file.
    subject = f.replace('json','')
    with open(os.path.join(RAW_DIR, f), 'r') as f:
        JSON = json.load(f)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble behavioral data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Assemble learning trials.
    games = [dd for dd in JSON if dd['trial_type'] == 'horizons-task']
    games = games[2:]    # drop practice trials
    
    ## Iteratively re-construct trials.
    dd = dict(Block=[], Trial=[], Horizon=[], Info=[], mu_L=[], mu_R=[], Choice=[], RT=[], Outcome=[])
    
    for i, g in enumerate(games):
                
        ## Compute game information.
        info = np.where(np.in1d(g['forced_choices'], 'leftarrow'), 0.5, -0.5).sum().astype(int)
            
        ## Unpack and store game data.
        dd['Block']   += [i+1 for _ in range(g['horizon'])]
        dd['Trial']   += [i+1 for i in range(g['horizon'])]
        dd['Horizon'] += [g['horizon'] for _ in range(g['horizon'])]
        dd['Info']  += [info for _ in range(g['horizon'])]
        dd['mu_L']    += [g['left_mu'] for _ in range(g['horizon'])]
        dd['mu_R']    += [g['right_mu'] for _ in range(g['horizon'])]
        dd['Choice']  += g['keys_pressed']
        dd['RT']      += g['response_times']
        dd['Outcome'] += np.where( 
            np.in1d(g['keys_pressed'], 'leftarrow'), 
            np.array(g['left_numbers']), 
            np.array(g['right_numbers'])
        ).tolist()
        
    ## Convert to DataFrame.
    dd = DataFrame(dd)
    
    ## Format data.
    dd.Choice = dd.Choice.replace({'leftarrow':1, 'rightarrow':0})
    dd.RT *= 1e-3
    
    ## Insert additional columns.
    dd.insert(0, 'Subject', subject)
    dd.insert(7, 'delta', dd['mu_L'] - dd['mu_R'])
    dd.insert(10, 'Accuracy', ((dd['mu_L'] > dd['mu_R']).astype(int) == dd.Choice).astype(int))
    
    ## Append information.
    DATA.append(dd)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble survey data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
    ## Initialize dictionary.
    dd = dict(Subject=subject)
    
    ## Gather surveys.
    templates = [dd for dd in JSON if dd['trial_type'] == 'survey-template']
    
    for prefix in ['pswq','ius12']:
        
        ## Extract survey.
        survey = [d for d in templates if prefix in d.get('survey', d['trial_type'])]
        if survey: survey, = survey
        else: continue
        
        ## Update dictionary.
        dd[f'{prefix}-rt'] = np.copy(np.round(survey['rt'] * 1e-3, 3))
        
        dd[f'{prefix}-radio'] = len(survey['radio_events'])
        dd[f'{prefix}-key'] = len(survey['key_events'])
        dd[f'{prefix}-mouse'] = len(survey['mouse_events'])
        dd[f'{prefix}-ipi'] = np.round(np.median(np.diff(survey['radio_events']) * 1e-3), 3)
                
        ## Reformat responses.
        survey = {f'{prefix}-{k.lower()}': survey['responses'][k] for k in sorted(survey['responses'])}
    
        ## Update dictionary.
        dd.update(survey)
        
    ## Append.
    SURVEYS.append(dd)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble metadata.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Gather surveys.
    DEMO, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
    DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
    COMP, = [dd for dd in JSON if dd['trial_type'] == 'horizons-comprehension']
    
    ## Assemble dictionary.
    dd = dict(Subject = subject)
    dd.update({k.capitalize():v for k, v in DEMO['responses'].items()})
    dd['Comprehension'] = COMP['responses']
    dd['Errors'] = COMP['num_errors']
    dd.update({k.capitalize():v for k, v in DEBRIEF['responses'].items()})
    
    ## Append.
    METADATA.append(dd)
        
## Concatenate data.
METADATA = DataFrame(METADATA, columns=dd.keys()).sort_values('Subject')
SURVEYS = DataFrame(SURVEYS).sort_values('Subject')
DATA = concat(DATA).sort_values(['Subject','Block','Trial'])

## Save.
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)
SURVEYS.to_csv(os.path.join(DATA_DIR, 'surveys.csv'), index=False)
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)