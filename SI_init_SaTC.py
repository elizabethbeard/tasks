### SaTC Social Influence Task ###

#created by ebeard
#last updated 20190214

''' task description 
Participants will provide initial ratings on a 1-5 scale of how willing
they are to share a given piece of information (that varies on levels of 
intrusiveness). Immediately after providing their initial rating, participants
will then be shown what they believe are aggrate responses of other study
participants. In reality, these will be randomly assigned feedback such that a
proportion of the ratings are higher, lower, or the same as participants
'''

### import modules ###
from psychopy import visual, core, event, gui, data, logging
import os
import sys
import csv
import datetime
import random

##clear any pre-existing parameters##
event.globalKeys.clear()

##function to save data if you exit the experiment##
#note: this will only have save out relevant data if you quit out after MORE THAN ONE TRIAL.
def saveout():
    #save trial handler data (if there is any)
    trials.saveAsWideText(fileName=log_file.format(subj, subj), delim=',', appendFile=True)
    
    logging.data('******EXPERIMENT QUIT******')
    logging.flush()

    core.quit()

### parameters ###
DEBUG = True

# timing
globalClock = core.Clock()
timer = core.Clock()

readTime = 5
decideTime = 3
respDur = 1 #this is 1 so that the true core.wait is .8 as per https://www.psychopy.org/api/core.html#psychopy.core.wait
feedbackTime = 3
between_ITI = 2.3

# response options
# this isn't necessarily the way we have to do it but it seems helpful conceptually
#button_labels = { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5 }
#buttons = button_labels.keys()
respKeys = ('1','2','3','4','5')

# add ctrl + q as a way to quit the experiment
event.globalKeys.add(key='q', modifiers=['shift'], func=saveout) 

### GUI ###
if DEBUG:
    subj='SI900' #change with specific test number/as needed
    screen='n'
    
else:
    subjDlg=gui.Dlg(title="SaTC Initial Ratings")
    subjDlg.addField('Enter Subject ID: ') #0
    subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #1
    subjDlg.show()
    
    if gui.OK:
        subj=subjDlg.data[0]
        screen=subjDlg.data[1]
        if subj == False:
            print 'Please enter subject ID. Consult the particiant sheet for the correct ID'
            sys.exit()
    else:
        print 'Please enter study details.'
        sys.exit()

### logging ###
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)

log_file = 'logs/{}/{}_si_init.csv'

logging.LogFile('logs/%s/%s_si_init.log' % (subj, subj), level=logging.DATA, filemode='w')
logging.setDefaultClock(globalClock)

### windows ###
# setup
if screen == 'y':
    useFullScreen=True
    useDualScreen=1
if screen == 'n':
    useFullScreen=False
    useDualScreen=0
if (screen != 'y') and (screen != 'n'):
    print 'Please specify how you want to present this task. Please enter y (yes) or n (no).'

win = visual.Window([800,600], monitor='testMonitor', units='deg', fullscr=useFullScreen, 
    allowGUI=False, screen=useDualScreen)

# displays
fixation = visual.TextStim(win, text="+", height=2)
pressSpace = visual.TextStim(win, text='Press SPACE to continue.', color='white', 
    height=1, alignHoriz='center', alignVert='center', pos=(0,-2))
instruct1 = visual.TextStim(win, text='Instructions will go here.', color='white', 
    height=1, alignHoriz='center', alignVert='center')
question = visual.TextStim(win, pos=(0, 1.5), height=1.2, wrapWidth=20)
anchor1 = visual.TextStim(win, text='not at all willing', pos=(-8,-2), height=1)
anchor5 = visual.TextStim(win, text='extremely willing', pos=(8,-2), height=1)
feedback = visual.TextStim(win, pos=(0,-.5), height=1, color='yellow')

ratingStim = []
xpos = [-8,-4,0,4,8]

for rating in range(1,6):
    ratingStim.append(visual.TextStim(win, text='%i' % rating, 
    pos=(xpos[rating-1], -4.2), height=1))

### stimuli ###
# load trial stimuli
trial_data = [r for r in csv.DictReader(open('stim/Question.1.csv', 'rU'))]

# set up trial handler
trials = data.TrialHandler(trial_data[:3], nReps=1, method='random')

# feedback conditions
condition_labels = {1: 'HIGHER', 2:'LOWER', 3: 'same', 4:'not rated'}

## use counters to pseudo-randomize trial conditions
conditions = [1]*15 + [2]*15 + [3]*15 + [4]*15

random.seed(int(subj[-3:])) #this allows us to replicate it if you have to run it a second time/it breaks in the middle
random.shuffle(conditions)

#https://www.quora.com/How-do-I-remove-an-item-from-a-python-list

### TASK ###
#instructions
instruct1.draw()
pressSpace.draw()
win.flip()
event.waitKeys(keyList='space')

#task loop
def do_run(trials):
    
    # if you had to wait for a scanner trigger you would do so here
    # reset globalCLock for beginning of task
    globalClock.reset()
    logging.log(level=logging.DATA, msg='** SUBJ %s STARTED **' % (subj))
    
    # loop through trials
    for trial in trials:
        idx = trials.thisIndex # we might not need this
        
        timer.reset()
        event.clearEvents()
        answer=0
        
        logging.log(level=logging.DATA, msg='Trial Onset -- Question ID: %s, Category: %s' 
            % (trial['ID'], trial['Category']))
        
        #set question text for trial
        question.setText(trial['Question'])
        
        #reset rating scale color
        for rate in ratingStim:
            rate.setColor('white')
        
        questionOnset = globalClock.getTime()
        trials.addData('questionOnset', questionOnset)
        logging.log(level=logging.DATA, msg='Question Onset')
        
        while timer.getTime() <= readTime:
            question.draw()
            win.flip()
        
        timer.reset()
        logging.log(level=logging.DATA, msg='Initial Rating Onset')
        initRating_StimOnset = globalClock.getTime()
        trials.addData('initRating_StimOnset', initRating_StimOnset)
        
        question.draw()
        anchor1.draw()
        anchor5.draw()
        for resp in ratingStim:
            resp.draw()
        win.flip()
        
        while timer.getTime() <= decideTime:
            
            resp = event.getKeys(keyList=respKeys)
            
            if len(resp) > 0:
                resp_value = int(resp[0])
                initRating_RespOnset = globalClock.getTime()
                ratingStim[resp_value-1].setColor('red')
                
                answer=1
                
                initRating_Resp = resp_value
                initRating_rt = initRating_StimOnset-questionOnset
                
                
                #redraw the ratingStim with proper color
                question.draw()
                anchor1.draw()
                anchor5.draw()
                for resp in ratingStim:
                    resp.draw()
                win.flip()
                core.wait(respDur)
                break
                
            if answer == 0:
                resp_value = 'NA'
                initRating_RespOnset = 'NA'
                initRating_Resp = 'NA'
                initRating_rt = 'NA'
                
        trials.addData('initRating_Resp', resp_value)
        trials.addData('initRating_rt', initRating_rt)
        logging.log(level=logging.DATA, msg='Initial Rating: %s, RT: %s, RespOnset: %s' 
            % (resp_value, initRating_rt, initRating_RespOnset))
        
        event.clearEvents()
        timer.reset()
        
        feedbackOnset = globalClock.getTime()
        trials.addData('feedbackOnset', feedbackOnset)
        logging.log(level=logging.DATA, msg='Feedback Onset')
        
        # feedback logic
        # need to add in something to skip/mismatch the feedback if the resp is too low
        
        condition = conditions[trials.thisIndex]
        feedback.setText('Average: %s' % condition_labels[condition])
        
        while timer.getTime() < feedbackTime:
            
            feedback.draw()
            question.draw()
            anchor1.draw()
            anchor5.draw()
            for resp in ratingStim:
                resp.draw()
            win.flip()
        
        trials.addData('feedbackCond', condition)
        logging.log(level=logging.DATA, msg='Feedback Condition: %s' % 
            (condition_labels[conditions[trials.thisIndex]]))
            
    trials.saveAsWideText(log_file.format(subj, subj), delim=',', appendFile=True)
    logging.data('*****END INITIAL RATINGS *****')

do_run(trials)