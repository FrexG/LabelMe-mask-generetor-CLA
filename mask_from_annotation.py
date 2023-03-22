import os
import glob
import json
import numpy as np
import cv2 as cv
import pandas as pd
import argparse
from tqdm import tqdm
"""
Author: Fraol Gelana
Date : Nov,2022
==============================================================|
To run this applications, execute                             | 
**** python mask_from_annotation.py --source folder_path **** | 
==============================================================|
"""

def make_shapes(path):
    """
    Creates binary masks and corresponding csv labels for json annotations 
    generated by labelme app.
    -------------------------
        Parameters
            `path`: relative path of the folder containing the annotation for 
                    individual videos 
    """
    label_color_dict = {
                        "leaf_rust":(0,0,255),
                        "leaf_spot":(56,89,120),
                        "leaf_miner":(255,0,0),
                        "free_feeder":(100,0,200),
                        "leaf_skeletonizer":(0,190,256)
                        }

    if os.path.exists(path):
        save_dir = os.path.join(path,"masks")
        
        try:
            os.mkdir(save_dir)
        except Exception as e:
            print(e)

        images = []
        masks = []

        json_files = glob.glob(path+"/*.json") # find all .json files in the current directory
        
        # read the contents of each json file
        for file in tqdm(json_files):
            with open(file) as f:
                data = json.load(f)
                image_path = os.path.join(path,data["imagePath"])

                im = cv.imread(image_path)
                mask = np.zeros((im.shape[0],im.shape[1],3))

                for shape in data["shapes"]: # Draw polly for each pollygon in the annotation
                    fill_color = label_color_dict[shape["label"]]
                    mask = cv.fillPoly(mask,np.array([shape["points"]],np.int32),color=fill_color)
                    
                images.append(data['imagePath'])

                mask_filename = f"{data['imagePath'].split('.')[0]}_mask.jpg"
                masks.append(os.path.join("masks",mask_filename))

                cv.imwrite(os.path.join(save_dir,f"{data['imagePath'].split('.')[0]}_mask.jpg"),mask) # save mask to file

            if len(masks) > 0:
                df = pd.DataFrame({'images_names':images,'mask_names':masks})
                df.to_csv(f'{path}/annotations.csv')
    else:
        raise(FileNotFoundError)


# Create the parser object
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--source',type=str,required=True) 
# source (path of the directory containing the annotations)
# Parse the argument
args = parser.parse_args()

make_shapes(args.source)

