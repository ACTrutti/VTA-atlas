
import nibabel
import nighres

#import nighresjava
#from nighres.io import load_volume
#from nighres.io import save_volume
import numpy
import os
import glob
from pathlib import Path
import datetime


# List of subject IDs to be processed, assuming they all come from the Subcortex database (BIDS version)
subjects = []
subjects.sort()

# Alternatively, uncomment to use all of them

# structure(s) of interest
structures = ['vta']
sides = ['l','r']
sessions = ['1','2']


# Raters are scaled by experience level
raters_lvl1 = ['atx','lfx']
# raters_lvl2 = ['mmx','lfx','bix']
# raters_lvl3 = ['jgx','tvr','gwx','lwx','dbx','gpx','vkx','nvb','akx','jrx','dmx','lhx','bos','acm',
#                'jbx','jvd','gbx','jlx','msk','rvb','bkx','roz','vsx','rsz','bbp','mma','rul',
#                'ytt','mjb','vhx']
# raters_lvl4 = ['rtx']

# path for the statistics files (one per structure and hemisphere)
output_path = Path('../VTA_data_BIDS/OverviewFiles')

# send conjunct back to BIDS database?
conj2bids = True

# path for temporary results (will be erased eventually if not changed)
temp_path = Path('../Documents/tmp/manual_delineation_statistics_bids')

verbose = True

today = str(datetime.date.today())


bidsdir = Path('../VTA_data_BIDS/')
#print(bidsdir)
for subject in subjects:
    for structure in structures:
     #   print(structure)
        for side in sides:
      #      print(side)
            for ses in sessions:
       #         print(ses)
                # data path
                subject = str(subject).zfill(3)
                print(subject)
                #mask_path =  bidsdir/('sub-'+subject)/('ses-'+ses)/'derivatives'/structure/'manual_masks'
                mask_path =  bidsdir/structure/('sub-'+subject)/'manual_masks'

      #          print(mask_path)
                # find existing masks
                if verbose: print('looking for masks: '+'sub-'+subject+'_mask-'+structure+'_hem-'+side+'*.nii.gz')
                masks = list(mask_path.glob('sub-'+subject+'_mask-'+structure+'_hem-'+side+'*.nii.gz'))
                if verbose: print(str(len(masks))+' masks found')

               
               # masks = os.listdir(mask_path)
                

               # if verbose: print(str(len(masks))+' masks found')
            
                # check for sufficient number (2):
                if len(masks)>1:
            
                    # check for most experienced first rater
                    found1 = False
                    mask1 = None
                    rater1 = None
                    for rater in raters_lvl1:
                        if not found1:
                            mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                            if len(mask)==1:
                                found1 = True
                                mask1 = mask[0]
                                rater1 = rater
                    if not found1:
                        for rater in raters_lvl2:
                            if not found1:
                                mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                if len(mask)==1:
                                    found1 = True
                                    mask1 = mask[0]
                                    rater1 = rater
                        if not found1:
                            for rater in raters_lvl3:
                                if not found1:
                                    mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                    if len(mask)==1:
                                        found1 = True
                                        mask1 = mask[0]
                                        rater1 = rater
                            if not found1:
                                for rater in raters_lvl4:
                                    if not found1:
                                        mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                        if len(mask)==1:
                                            found1 = True
                                            mask1 = mask[0]
                                            rater1 = rater
            
                    if found1:
                        if verbose: print('first rater: '+rater1)
                        if verbose: print('first rater mask: '+str(mask1))
                
                        # check for most experienced second rater:
                        # if more than one in same category then 
                        # choose the one with highest Dice (explicit bias toward experience)
                        found2 = False
                        mask2 = None
                        rater2 = None
                        bestDice = 0.0
                        for rater in raters_lvl1:
                            if rater is not rater1:
                                #print('rater: '+rater+', rater 1: '+rater1)
                                mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                if len(mask)==1:
                                    trial2 = mask[0]
                                    # compute Dice
                                    data1 = nighres.io.load_volume(str(mask1)).get_data()
                                    data2 = nighres.io.load_volume(str(trial2)).get_data()
                                    Dice = 2*numpy.sum( (data1>0)*(data2>0) )/(numpy.sum(data1>0)+numpy.sum(data2>0))
                                    #print('Dice: '+str(Dice))
                                    if Dice>bestDice:
                                        bestDice = Dice
                                        mask2 = trial2
                                        rater2 = rater
                                        found2 = True
                        if not found2:
                            for rater in raters_lvl2:
                                if rater is not rater1:
                                    #print('lvl2: rater: '+rater+', rater 1: '+rater1)
                                    mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                    if len(mask)==1:
                                        trial2 = mask[0]
                                        # compute Dice
                                        data1 = nighres.io.load_volume(str(mask1)).get_data()
                                        data2 = nighres.io.load_volume(str(trial2)).get_data()
                                        Dice = 2*numpy.sum( (data1>0)*(data2>0) )/(numpy.sum(data1>0)+numpy.sum(data2>0))
                                        #print('Dice: '+str(Dice))
                                        if Dice>bestDice:
                                            bestDice = Dice
                                            mask2 = trial2
                                            rater2 = rater
                                            found2 = True
                        if not found2:
                            for rater in raters_lvl3:
                                if rater is not rater1:
                                    #print('lvl3: rater: '+rater+', rater 1: '+rater1)
                                    mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                    if len(mask)==1:
                                        trial2 = mask[0]
                                        # compute Dice
                                        data1 = nighres.io.load_volume(str(mask1)).get_data()
                                        data2 = nighres.io.load_volume(str(trial2)).get_data()
                                        Dice = 2*numpy.sum( (data1>0)*(data2>0) )/(numpy.sum(data1>0)+numpy.sum(data2>0))
                                        #print('Dice: '+str(Dice))
                                        if Dice>bestDice:
                                            bestDice = Dice
                                            mask2 = trial2
                                            rater2 = rater
                                            found2 = True
                        if not found2:
                            for rater in raters_lvl4:
                                if rater is not rater1:
                                    mask = list(mask_path.glob('sub-'+subject+'*_mask-'+structure+'_hem-'+side+'_rat-'+rater+'.nii.gz'))
                                    if len(mask)==1:
                                        trial2 = mask[0]
                                        # compute Dice
                                        data1 = nighres.io.load_volume(str(mask1)).get_data()
                                        data2 = nighres.io.load_volume(str(trial2)).get_data()
                                        Dice = 2*numpy.sum( (data1>0)*(data2>0) )/(numpy.sum(data1>0)+numpy.sum(data2>0))
                                        if Dice>bestDice:
                                            bestDice = Dice
                                            mask2 = trial2
                                            rater2 = rater
                                            found2 = True
                                         
                
                        if found2:
                            if verbose: print('second rater: '+rater2)
                            if verbose: print('second rater mask: '+str(mask2))
                            if verbose: print('Dice coefficient: '+str(Dice))
                
                            # load data
                            img1 =  nighres.io.load_volume(str(mask1))
                            data1 = img1.get_data()
                            hdr = img1.get_header()
                            aff = img1.get_affine()
                            imgres = [x.item() for x in hdr.get_zooms()]
                            imgdim = data1.shape
                
                            data2 = nighres.io.load_volume(str(mask2)).get_data()
                        
                            # binarize + nifti container
                            bin1 = nibabel.Nifti1Image(data1>0, aff, hdr)
                            bin2 = nibabel.Nifti1Image(data2>0, aff, hdr)
                        
                            # conjunction + nifti container
                            conj = nibabel.Nifti1Image((data1>0)*(data2>0), aff, hdr)
                         
                            # create output dir if needed
                            output_path.mkdir(exist_ok=True)
                            temp_path.mkdir(exist_ok=True)
                        
                            # save the binarized images with proper names etc
                            bin1_file = temp_path / Path(str(Path(Path(mask1).stem).stem)+'_calc-bin.nii.gz')
                            nighres.io.save_volume(str(bin1_file), bin1)
                 
                            bin2_file = temp_path / Path(str(Path(Path(mask2).stem).stem)+'_calc-bin.nii.gz')
                            nighres.io.save_volume(str(bin2_file), bin2)
                
                            # merge both rater names, keep everything else    
                            conj_file = temp_path / Path(str(Path(Path(mask1).stem).stem)+rater2+'_calc-conj.nii.gz')
                            nighres.io.save_volume(str(conj_file), conj)
                
                            # send the result back into database?
                            if conj2bids:
                                conj_dir = bidsdir/structure/('sub-'+subject)/'derivatives'/'conjunct_masks'
                                conj_dir.mkdir(exist_ok=True)
                                conj_db_file =  conj_dir / Path(str(Path(Path(mask1).stem).stem)+rater2+'_calc-conj.nii.gz')
                                if verbose: print('copy conjunct to: '+str(conj_db_file))
                                nighres.io.save_volume(str(conj_db_file), conj)
                
                            stats_file = output_path / Path('statistics-conj_mask-'+structure+'_hem-'+side+'_date-'+today+'.csv')
                            if verbose: print("compute statistics to: "+str(stats_file))
                            nighres.statistics.segmentation_statistics(str(bin1_file), template=str(bin2_file),
                                               statistics=[ "Voxels", "Volume", 'Volume_difference', "Center_of_mass",'Dice_overlap', 'Dilated_Dice_overlap', 'Hausdorff_distance'], output_csv=str(stats_file))
                           