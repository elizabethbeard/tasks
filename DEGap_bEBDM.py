##### EBDM #####

#ebeard
#created: 20180820
#last updated: 20190128

##### description #####
# add task description here

##### task #####
##import modules##

from psychopy import visual, core, event, gui, data, logging
import os
import sys
import csv
import datetime
import random
from numpy.random import choice as np_choice

##clear any pre-existing parameters##
event.globalKeys.clear()

##function to save data if you exit the experiment##
#note: this will only have save out relevant data if you quit out after MORE THAN ONE TRIAL.
def saveout():
    #save trial handler data (if there is any)
    if run == 1:
        trials_run1.saveAsWideText(fileName=log_file.format(subj_id, subj_id, run), delim=',', appendFile=True)
    elif run == 2:
        trials_run2.saveAsWideText(fileName=log_file.format(subj_id, subj_id, run), delim=',', appendFile=True)

    logging.data('******EXPERIMENT QUIT******')
    logging.flush()

    core.quit()

### parameters ###
#debugging
DEBUG = False

#timing
instruct_dur=3
present_dur=1.5
think_dur=3
decision_dur=2
feedback_dur=.5 #this is .5 so that the true core.wait is .3 as per https://www.psychopy.org/api/core.html#psychopy.core.wait
##randomized ITIs determined using easy-optimize-x (http://www.bobspunt.com/easy-optimize-x/)
ITI_1 = [1.3679, 1.233, 1.0587, 2.4102, 1.048, 1.2377, 1.7267, 1.5966, 2.274, 1.3248, 1.2135, 2.2012, 1.4961, 4.653, 5.4629, 1.8631, 5.4629 ,1.0098]
ITI_2=[1.3975 ,1.2245 ,1.5734 ,4.6191 ,1.0887 ,1.2853 ,1.1477 ,1.8808 ,1.1749 ,2.3911 ,2.5575 ,1.0113 ,1.2297 ,1.4411 ,5.0846 ,3.6695 ,1.3267,1.0098]
sampling_dur1=[15,15,15,15,15,15,15,15,16,16,16,16,17,17,17,18,18,18,19,19]
sampling_dur2=[15,15,15,15,15,15,15,15,16,16,16,16,17,17,17,18,18,18,19,19]

globalClock = core.Clock()
timer = core.Clock()

#response options
responseKeys=('1','2')
event.globalKeys.add(key='q', modifiers=['shift'], func=saveout) #add ctrl + q as a way to quit the experiment

### gui ###
if DEBUG:
    subj_id='DE902' #change with specific test number/as needed
    specific_run='2'
    run=2
    screen='n'

else:
    subjDlg=gui.Dlg(title="Experiencing Point Machine")
    subjDlg.addField('Enter Subject ID (DE###): ') #0
    subjDlg.addField('Select Round (1 or 2):') #1
    subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #2
    subjDlg.addText('******IF YOU NEED TO QUIT THE TASK, PRESS [SHIFT+Q]******')
    subjDlg.show()

    if gui.OK:
        subj_id=subjDlg.data[0]
        specific_run=subjDlg.data[1]
        screen=subjDlg.data[2]
        if (not subj_id == False):
            if len(specific_run) == 1: #if user enters an ONLY run - run only the specified run
                run = int(specific_run);
                print 'Playing Round %s' %int(specific_run)
            else:
                print 'Please specify which round of the sampling game you would like to run. \n Consult the participant sheet for the counterbalance order.'
        else:
            print 'Please enter subject ID. Consult the particiant sheet for the correct ID'
            sys.exit()
    else:
        print 'Please enter study details.'
        sys.exit()

### logging ###
#directories
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = 'logs/{}/{}_ebdm_run_{}.csv'
sampling_file = csv.writer(open('%s/%s_ebdm_samplingdata_run_%s.csv' % (subjdir, subj_id, run),"w"),delimiter=',')
sampling_file.writerow(['Trial', 'Resp', 'LR', 'Outcome', 'RT','respOnset'])
imgdir = '%s/stim' % (expdir)

logging.LogFile('%s/%s_ebdm_run_%s.log' % (subjdir, subj_id, specific_run), level=logging.DEBUG, filemode='w')
logging.setDefaultClock(globalClock)

### windows ###
#setup window
if screen == 'y':
    useFullScreen=True
    useDualScreen=0 #change to yes for actual study
if screen == 'n':
    useFullScreen=False
    useDualScreen=0
if (screen != 'y') and (screen != 'n'):
    print 'Please specify how you want to present this task. Please enter y (yes) or n (no).'

win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen,
    allowGUI=False, screen=useDualScreen, color='black', winType='pyglet') #set screen to 1 for dual monitor

rectWidth = .275    #adjust these accordingly for the monitor you need to use, pulled from DBDM
aspectRatio = (16*rectWidth)/9 #define your monitor to be the same as TUBRIC

#basics
fixation = visual.TextStim(win, text="+", height=2)
readyScreen = visual.TextStim(win, text="Ready? \n\nPlease remember to keep your head still!", height=1.5)
waiting = visual.TextStim(win, text="Waiting for scanner...", height=1.5)
pressSpace = visual.TextStim(win, text='Press SPACE to continue.', color='white', height=1, alignHoriz='center', alignVert='center')
think = visual.TextStim(win, text="THINK", height=.1, units = 'norm', alignHoriz='center', alignVert='center')
decide = visual.TextStim(win, text="DECIDE", height=.1, units = 'norm', alignHoriz='center', alignVert='center')

#boxes
box1 = visual.Rect(win, width=rectWidth*2, height=aspectRatio*2, lineWidth=3.5, lineColor='white', fillColor=None, pos=(-.65+rectWidth/2, .15-aspectRatio/2), units='norm')
box2 = visual.Rect(win, width=rectWidth*2, height=aspectRatio*2, lineWidth=3.5, lineColor='white', fillColor=None, pos=(.35+rectWidth/2, .15-aspectRatio/2), units='norm')

#outcomes
out1 = visual.TextStim(win, units='norm', pos=(-.65+rectWidth/2, .15-aspectRatio/2), height=.2, alignHoriz='center', alignVert='center') #same pos as box1
out2 = visual.TextStim(win, units='norm', pos=(.35+rectWidth/2, .15-aspectRatio/2), height=.2, alignHoriz='center', alignVert='center') #same pos as box2

#select
press1 = visual.TextStim(win, text='Press 1', units='norm', pos=(-.65+rectWidth/2, .15-aspectRatio*2), height=.1, alignHoriz='center', alignVert='center')
press2 = visual.TextStim(win, text='Press 2', units='norm', pos=(.35+rectWidth/2, .15-aspectRatio*2), height=.1, alignHoriz='center', alignVert='center')

#task instructions
instruct1 = visual.ImageStim(win, image=('%s/ebdm1R.jpeg' % imgdir), units='norm')
instruct2 = visual.ImageStim(win, image=('%s/ebdm2R.jpeg' % imgdir), units='norm')
instruct3 = visual.ImageStim(win, image=('%s/question.jpeg' % imgdir), units='norm')
keyPress = visual.ImageStim(win, image=('%s/keyboard.jpeg' % imgdir), units='norm')

### stimuli ###
#read in experiment spreadsheet
trial_data = [r for r in csv.DictReader(open('stim/fMRIProblemSet_20190114.csv', 'rU'))]

#randomize trial data
random.seed(int(subj_id[-3:])) #this allows us to replicate it if you have to run it a second time/it breaks in the middle
random.shuffle(trial_data)

trial_data_1 = trial_data[:18]
trial_data_2 = trial_data[18:]

#parse the randomized trial order
trials_run1 = data.TrialHandler(trial_data_1[:1], 1, method="sequential")
trials_run2 = data.TrialHandler(trial_data_2[:], 1, method="sequential")

#randomize the ITI and samplingDurs
for i in [ITI_1, ITI_2, sampling_dur1, sampling_dur2]:
    random.seed(int(subj_id[-3:]))
    random.shuffle(i)

### main task ###
#reset globalClock for beginning of task
globalClock.reset()

# main task loop
def do_run (run, trials):

    #present instructions
    #if fMRI, wait for scanner trigger
    instruct1.draw()
    win.flip()
    logging.data('** START RUN %s **' % specific_run)
    event.waitKeys(keyList=('space'))
    
    instruct2.draw()
    win.flip()
    event.waitKeys(keyList=('space'))

    keyPress.draw()
    win.flip()
    event.waitKeys(keyList=('space'))

    instruct3.draw()
    win.flip()
    event.waitKeys(keyList=('space'))


    if run == 1:
        ITI = ITI_1
        sampling_durList = sampling_dur1

    if run == 2:
        ITI = ITI_2
        sampling_durList = sampling_dur2

    for trial in trials:
        #add trial logic: show stimuli, get resp, add data to 'trial'

        idx = trials.thisIndex
        sampling_dur = sampling_durList[idx]
        ITItime=ITI[idx]
        
        core.checkPygletDuringWait = False


        ### RANDOMIZATION
        #also it should be noted that in the fmriProblemSet_20180802 file I was dumb and the OUTCOME and PROBABILITIES have different naming conventions SMH. They are re-streamlined here.
        #as of 20190114 I have renamed the PROBABILITIES naming conventions so that they match with the OUTCOME.
        prob1_1 = float(trial['P1_1']) #probability1 for option1
        prob2_1 = float(trial['P2_1']) #probability2 for option1
        prob1_2 = float(trial['P1_2']) #probability1 for option2
        prob2_2 = float(trial['P2_2']) #probability2 for option2

        if '-' not in trial['O1_1'] and trial['O1_1'] != '0': #O1_1
            O1_1 = '+%s' % (trial['O1_1'])
        else:
            O1_1 = trial['O1_1']
        if '-' not in trial['O1_2'] and trial['O1_2'] != '0': #O1_2
            O1_2 = '+%s' % (trial['O1_2'])
        else:
            O1_2 = trial['O1_2']
        if '-' not in trial['O2_1'] and trial['O2_1'] != '0': #O2_1
            O2_1 = '+%s' % (trial['O2_1'])
        else:
            O2_1 = trial['O2_1']
        if '-' not in trial['O2_2'] and trial['O2_2'] != '0': #O2_2
            O2_2 = '+%s' % (trial['O2_2'])
        else:
            O2_2 = trial['O2_2']

        Prob1 = {
            'p': [prob1_1, prob2_1],
            'out': [O1_1, O2_1]
            }
        Prob2 = {
            'p': [prob1_2, prob2_2],
            'out': [O1_2, O2_2]
            }


        sampling_RT_list = []
        sampling_resp_list = []
        sampling_lr_list= []
        sampling_outcome_list = []
        sampling_respOnset_list = []
        samplingCount = 0
        safeCount = 0
        riskyCount = 0
        switchCount = 0

        leftRight = random.randint(0,1) #if 0, P1 is on the left, P2 is on the right

        trialStartTime = globalClock.getTime()
        trials.addData('trialStartTime', trialStartTime)
        logging.data('Trial Onset - ProblemType: %s, ProblemNumber: %s, leftRight: %s, samplingDur: %s, assignedITI: %s' % (trial['ProbType'], trial['ProbNumber'], leftRight, sampling_dur, ITItime))

        timer.reset()

        #https://github.com/alishir/IGT_net/blob/master/igt_psychtoolbox/igt_mri.m
        logging.data('Sampling Onset')
        while timer.getTime() < sampling_dur:
            samplingOnset = timer.getTime()
            #SET PROBABILITIES FOR EACH SUBTRIAL
            draw1 = np_choice(a=Prob1['out'], size=1, p=Prob1['p'])
            draw2 = np_choice(a=Prob2['out'], size=1, p=Prob2['p'])

            box1.draw()
            box2.draw()
            press1.draw()
            press2.draw()
            win.flip()

            if DEBUG:
                resp_val = random.randint(1,2)
                rt_onset = globalClock.getTime()
                logging.data('DEBUG MODE Sampled Response: %s' % resp_val)
                core.wait(.5)

            else:
                resp = event.getKeys(keyList = responseKeys, timeStamped=globalClock)
                resp_val = None
                prev_resp = None
                #prev_rt = None
                if len(resp) > 0:
                    resp_val = int(resp[0][0])
                    rt_onset = resp[0][1]

                    sampling_respOnset_list.append(rt_onset)

                    if samplingCount == 0: #and idx == 0:
                        sampling_RT_list.append(rt_onset-trialStartTime)
                    else:
                        sampling_RT_list.append(rt_onset-prev_rt)

                if samplingCount != 0: #won't have a previous response for the first sample
                    prev_resp = sampling_resp_list[-1]
                    prev_rt = sampling_respOnset_list[-1]

                #for adding in SwitchCount later
                #save prev_response
                #if resp_val != prev_resp:
                    #switchCount += 1
                    #make new response replace previous response


            if resp_val == 1:
                samplingCount += 1
                #logic to decide which outcome to display
                if leftRight == 0: #if 0, P1 is on the left, P2 is on the right
                    out1.setText(draw1[0])
                    response = 1
                else: #if 1, P1 is on the right, P2 is on the left
                    out1.setText(draw2[0])
                    response = 2

                if response == int(trial['SafeOption']):
                    safeCount += 1
                else:
                    riskyCount += 1

                if prev_resp and response != prev_resp: #won't have a previous response for the first sample
                    switchCount += 1

                box1.draw()
                box2.draw()
                press1.draw()
                press2.draw()
                out1.draw()
                win.flip()
                core.wait(feedback_dur)


                logging.data('Sampled Response: %s, Outcome Shown: %s' % (response, draw1[0]))

                sampling_resp_list.append(response)
                sampling_lr_list.append(leftRight)
                sampling_outcome_list.append(draw1[0])



            if resp_val == 2:
                samplingCount += 1
                if leftRight == 0:
                    out2.setText(draw2[0])
                    response = 2
                else:
                    out2.setText(draw1[0])
                    response = 1

                if response == int(trial['SafeOption']):
                    safeCount += 1
                else:
                    riskyCount += 1

                if prev_resp and response != prev_resp: #won't have a previous response for the first sample
                    switchCount += 1

                box1.draw()
                box2.draw()
                press1.draw()
                press2.draw()
                out2.draw()
                win.flip()
                core.wait(feedback_dur)
                

                logging.data('Sampled Response: %s, Outcome Shown: %s' % (response, draw2[0]))
                sampling_resp_list.append(response)
                sampling_lr_list.append(leftRight)
                sampling_outcome_list.append(draw2[0])
                
            event.clearEvents()


            if timer.getTime() >= sampling_dur-.5  :
                logging.data('** broke sampling loop (<.5s left in trial) **')
                break

        for idx in range(samplingCount):
            sampling_file.writerow([
                trials.thisIndex+1,
                sampling_resp_list[idx],
                sampling_lr_list[idx],
                sampling_outcome_list[idx],
                sampling_RT_list[idx],
                sampling_respOnset_list[idx]])

        samplingEndTime = globalClock.getTime()
        sampling_pad = sampling_dur-timer.getTime()
        trials.addData('samplingCount_total', samplingCount) #jk #I starting samplingCount at 1 to use it as an index for correctly calculating response time. We subtract that here to log it accurately.
        trials.addData('samplingCount_risky', riskyCount)
        trials.addData('samplingCount_safe', safeCount)
        trials.addData('switchCount', switchCount)
        trials.addData('samplingDur_assigned', sampling_dur)
        trials.addData('samplingDur_total', samplingEndTime-trialStartTime)
        trials.addData('samplingEndTime', samplingEndTime)

        timer.reset()
        box1.setLineColor('white')
        box2.setLineColor('white')
        thinkOnset = globalClock.getTime()
        logging.data('samplingCount: %s' % samplingCount)
        logging.data('Think Onset')
        trials.addData('thinkOnset', thinkOnset)

        while timer.getTime() < think_dur:
            box1.draw()
            box2.draw()
            think.draw()
            win.flip()

        box1.draw()
        box2.draw()
        press1.draw()
        press2.draw()
        decide.draw()
        win.flip()

        timer.reset()
        event.clearEvents()
        answer = 0
        response = []
        decide_onset = globalClock.getTime()
        logging.data('Decide Onset')
        trials.addData('decideOnset', decide_onset)
        timer.reset()

        while timer.getTime() < decision_dur:

            if DEBUG:
                resp = [1]
                resp_val = random.randint(1,2)
                logging.data('DEBUG MODE Decision Response: %s' % resp_val)
                core.wait(.5)

            else:
                resp = event.getKeys(keyList = responseKeys)


            if len(resp) > 0:
                resp_onset = globalClock.getTime()
                rt = resp_onset-decide_onset
                answer=1

                if not DEBUG:
                    resp_val = int(resp[0])
                    logging.data('Decision Button Press: %s' % resp)

                if resp_val == 1:
                    box1.setLineColor('red')
                    if leftRight == 0:
                        response = 1 #response is 1 for P1/option1 and 2 for P2/option2 always
                    else:
                        response = 2
                if resp_val == 2:
                    box2.setLineColor('red')
                    if leftRight == 0:
                        response = 2 #response is 1 for P1/option1 and 2 for P2/option2 always
                    else:
                        response = 1

                if response == int(trial['SafeOption']):
                    safeChoice = 0 #safeChoice is 0 if the safe choice was chosen, 1 if the risky option was chosen
                else:
                    safeChoice = 1

                logging.data('Decision Response: %s' % response)
                box1.draw()
                box2.draw()
                press1.draw()
                press2.draw()
                win.flip()
                core.wait(feedback_dur)
                decide_pad = decision_dur-rt-.3
                decideDur_total = resp_onset-trialStartTime+.3
                break


        if answer == 0:
            response = 'NA'
            resp_val = 'NA'
            resp_onset = 'NA'
            rt = 'NA'
            decide_pad = 'NA'
            safeChoice = 'NA'
            decideDur_total = decision_dur



        trials.addData('leftRight', leftRight)
        trials.addData('resp', response)
        trials.addData('safeChoice', safeChoice) #0 if safe, 1 if risky
        trials.addData('resp_onset', resp_onset)
        trials.addData('rt', rt)
        trials.addData('decideDur_total', decideDur_total)

        #reset box colors, reset outcomes
        box1.setLineColor('white')
        box2.setLineColor('white')
        out1.setText()
        out2.setText()


        timer.reset()

        #ITI
        ITI_onset=globalClock.getTime()
        logging.data('ITI Onset')

        if answer == 0:
            totalITI = ITItime+sampling_pad
        else:
            totalITI = ITItime+decide_pad+sampling_pad
        while timer.getTime() < totalITI:
            fixation.draw()
            win.flip()

        trials.addData('assignedITI', ITItime)
        trials.addData('sampling_pad', sampling_pad)
        trials.addData('decide_pad', decide_pad)
        trials.addData('totalITI', totalITI)
        trials.addData('ITI_onset', ITI_onset)
        trialEndTime = globalClock.getTime()
        trials.addData('TrialEndTime', trialEndTime)
        logging.data('Trial End Time - totalITI: %s' % totalITI)

        timer.reset()
        event.clearEvents()

    trials.saveAsWideText(fileName=log_file.format(subj_id, subj_id, run), delim=',', appendFile=True)
    logging.data('*****END RUN %s*****' % specific_run)

#### just do specific run if needed
if len(specific_run)==1:
    if run == 1:
        do_run(1, trials_run1)
    elif run == 2:
        do_run(2, trials_run2)
#    else: 'Run index is not permissible.'
#else:
#    for run_idx, trials in enumerate([trials_run1, trials_run2],1):
#        do_run(run_idx, trials)
