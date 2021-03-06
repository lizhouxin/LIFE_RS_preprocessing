# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:10:25 2015

@author: fbeyer
run:
python struct_preproc/run_structural_sample5.py f /scr/kennedy2/liem/subjects_lists/subjects_big_sample5_2_clean_n1184.txt

"""

from structural import create_structural
import sys, os

'''
Meta script to run structural preprocessing
------------------------------------------
Can run in two modes:
python run_structural.py s {subject_id}
python run_structural.py f {text file containing list of subjects}
'''
mode = sys.argv[1]

if mode == 's':
    subjects = [sys.argv[2]]
    print subjects
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

for subject in subjects:
    print 'Running subject ' + subject
    root_dir = '/scr/adenauer1/Franz/LIFE_es'
    working_dir = os.path.join(root_dir, 'wd', subject)
    data_dir = os.path.join(root_dir, 'subjects', subject)
    out_dir = data_dir

    ###########careful
    freesurfer_dir = '/scr/adenauer1/Franz/LIFE_es/FS/'
    # # #


    ##########you have to change this!!
    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    create_structural(subject=subject, working_dir=working_dir, data_dir=data_dir,
                      freesurfer_dir=freesurfer_dir, out_dir=out_dir,
                      standard_brain=standard_brain)
