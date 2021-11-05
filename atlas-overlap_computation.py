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


atlases = ['Pauli', 'Murty']
structures = ['vta', 'pbp', 'snr', 'snc']
sides = ['l','r']



output_path = Path('../analyses/OverviewFiles/thresholded-atlas-overlap')
temp_path = Path('../tmp/manual_delineation_statistics_bids')

reference_atlas_dir = Path('../atlas-vta_mni09b/structures/mni09b/')
verbose = True

today = str(datetime.date.today())

atlas_dir = Path('../vta_atlases/mni09b/unilateral_atlases/thresholded-atlases/')

for atlas in atlases: 
    print(atlas)
    for structure in structures:
        print(structure)
        for side in sides:
            print(side)
            atlas_path = atlas_dir
           # print(atlas_path)
            # find existing atlases
            if verbose: print('looking for atlas: '+'atlas-'+structure+'_hem-'+side+'_'+atlas+'-to-MNI09b_def-img_thr*.nii.gz')
            atlas_list = list(atlas_path.glob('atlas-'+structure+'_hem-'+side+'_'+atlas+'-to-MNI09b_def-img_thr*.nii.gz'))
            if verbose: print(str(len(atlas_list))+' atlases found')
            IMCN_atlas_list = list(reference_atlas_dir.glob('atlas-vta_hem-'+side+'_proba-27_mni09b_thr*.nii.gz'))
            IMCN_atlas = IMCN_atlas_list[0]
            atlas_file = atlas_list[0]
            img1 =  nighres.io.load_volume(str(atlas_file))
            data1 = img1.get_data()
            hdr = img1.get_header()
            aff = img1.get_affine()
            imgres = [x.item() for x in hdr.get_zooms()]
            imgdim = data1.shape       
            data2 = nighres.io.load_volume(str(IMCN_atlas)).get_data()
            # binarize + nifti container
            bin1 = nibabel.Nifti1Image(data1>0, aff, hdr)
            bin2 = nibabel.Nifti1Image(data2>0, aff, hdr)
            bin1_file = temp_path / Path(str(Path(Path(atlas_file).stem).stem)+'_calc-bin.nii.gz')
            nighres.io.save_volume(str(bin1_file), bin1)     
            bin2_file = temp_path / Path(str(Path(Path(IMCN_atlas).stem).stem)+'_calc-bin.nii.gz')
            nighres.io.save_volume(str(bin2_file), bin2)
            # print(atlas_file)
            stats_file = output_path / Path('statistics-vta-atlases-thesholded_overlap_hem-'+side+'_date-'+today+'.csv')
            if verbose: print("compute statistics to: "+str(stats_file))
            nighres.statistics.segmentation_statistics(str(bin1_file), template=str(bin2_file),
            statistics=[ "Voxels", "Volume", 'Volume_difference', 'Dice_overlap', 'Dilated_Dice_overlap', 'Hausdorff_distance'], output_csv=str(stats_file))
                           

