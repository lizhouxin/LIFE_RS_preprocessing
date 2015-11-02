# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 14:33:51 2015

@author: fbeyer
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:11:28 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.io as nio
from reconall import create_reconall_pipeline
from mgzconvert import create_mgzconvert_pipeline
from ants import create_normalize_pipeline
from brainextract import create_brainextract_pipeline

'''
Main workflow for preprocessing of mp2rage data
===============================================
Uses file structure set up by conversion
'''


def create_structural(subject, working_dir, data_dir, freesurfer_dir, out_dir, standard_brain):
    # main workflow
    struct_preproc = Workflow(name='anat_preproc')
    struct_preproc.base_dir = working_dir
    struct_preproc.config['execution']['crashdump_dir'] = struct_preproc.base_dir + "/crash_files"


    #########-----------------------------------------------------------#######
    # if freesurfer doesn't exists!
    #########-----------------------------------------------------------#######    
    # select files
    # templates={'anat': 'anat/MPRAGE_t1.nii'}
    # selectfiles = Node(nio.SelectFiles(templates, base_directory=data_dir),    name="selectfiles")

    # workflow to run freesurfer reconall
    # reconall=create_reconall_pipeline()
    # reconall.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    # reconall.inputs.inputnode.fs_subject_id=subject



    # workflow to get brain, head and wmseg from freesurfer and convert to nifti
    mgzconvert = create_mgzconvert_pipeline()
    #########-----------------------------------------------------------#######
    # if freesurfer already exists!
    #########-----------------------------------------------------------#######
    mgzconvert.inputs.inputnode.fs_subjects_dir = freesurfer_dir
    mgzconvert.inputs.inputnode.fs_subject_id = subject

    # brain extration function used bet to improve but it wasn't necessary
    # as issue was just caused by dilating the aparc+aseg file!
    # brainextraction=create_brainextract_pipeline()
    # brainextraction.inputs.inputnode.fraction=0.25
    # workflow to normalize anatomy to standard space
    normalize = create_normalize_pipeline()
    normalize.inputs.inputnode.standard = standard_brain

    # sink to store files
    sink = Node(nio.DataSink(base_directory=out_dir,
                             parameterization=False,
                             substitutions=[
                                 # ('outStripped', 'uni_stripped'),
                                 # ('outMasked2', 'uni_masked'),
                                 # ('outSignal2', 'background_mask'),
                                 # ('outOriginal', 'uni_reoriented'),
                                 # ('outMask', 'skullstrip_mask'),
                                 ('transform_Warped', 'T1_brain2mni')]),
                name='sink')

    # connections
    struct_preproc.connect(
        [

            #########-----------------------------------------------------------#######
            # if freesurfer doesn't exist
            #########-----------------------------------------------------------#######
            # (selectfiles, reconall, [('anat', 'inputnode.anat')]),
            # (reconall, mgzconvert,  [('outputnode.fs_subject_id', 'inputnode.fs_subject_id'),
            #                        ('outputnode.fs_subjects_dir', 'inputnode.fs_subjects_dir')]),

            #########-----------------------------------------------------------#######
            # if freesurfer already exists
            #########-----------------------------------------------------------#######

            (mgzconvert, normalize, [('outputnode.anat_brain', 'inputnode.anat')]),
            # (mp2rage, sink, [('outputnode.uni_masked', 'preprocessed.mp2rage.background_masking.@uni_masked'),
            # ('outputnode.background_mask', 'preprocessed.mp2rage.background_masking.@background_mask')
            # ]),
            (mgzconvert, sink, [('outputnode.anat_head', 'preprocessed.mod.anat.@head')]),
            (mgzconvert, sink, [('outputnode.anat_brain', 'preprocessed.mod.anat.@brain')]),
            (mgzconvert, sink, [('outputnode.anat_brain_mask', 'preprocessed.mod.anat.@mask')]),
            (normalize, sink, [('outputnode.anat2std', 'preprocessed.mod.anat.@anat2std'),
                               ('outputnode.anat2std_transforms',
                                'preprocessed.mod.anat.transforms2mni.@anat2std_transforms'),
                               ('outputnode.std2anat_transforms',
                                'preprocessed.mod.anat.transforms2mni.@std2anat_transforms')])
        ])
    # struct_preproc.write_graph(dotfilename='struct_preproc.dot', graph2use='colored', format='pdf', simple_form=True)

    # struct_preproc.run()
    struct_preproc.run(plugin='CondorDAGMan')  #
    #
    # plugin='MultiProc')
    # struct_preproc.run(plugin='MultiProc')
