import os
import glob
import json
import cv2
import numpy as np
import argparse
from tqdm import tqdm

def generated_symptoms(path:str):
    label_color_dict = {
                        "leaf_rust":(0,0,255),
                        "leaf_spot":(56,89,120),
                        "leaf_miner":(255,0,0),
                        "free_feeder":(100,0,200),
                        "leaf_skeletonizer":(0,190,256)
                        }
    # Create a directory for each key in label_color_dict
    for key in label_color_dict.keys():
        new_dir = os.path.join(path,key)
        if not os.path.exists(new_dir):
            print(f"Creating dir {new_dir}")
            try:
                os.mkdir(new_dir)
            except Exception as e:
                print(e)
    
    json_files = glob.glob(path+"/*.json")
    progress_bar = tqdm(json_files)
    for j,file in enumerate(progress_bar):
            with open(file) as f:
                data = json.load(f)
                image_path = os.path.join(path,data["imagePath"])
                progress_bar.set_postfix(file = image_path)
                im = cv2.imread(image_path)
                for i,shape in enumerate(tqdm(data["shapes"])):
                    label = shape["label"]
                    # Define the polly
                    pollygone_array = np.array([shape["points"]],np.int32)
                    # get the bounding box
                    x,y,w,h = cv2.boundingRect(pollygone_array)
                    # crop the symptom from the rgb image
                    symptom = im[y:y+h,x:x+w]
                    # save symptom image to the corresponding symptom folder
                    save_name = os.path.join(path,label)+f"/{data['imagePath'].split('.')[0]}_{label}.jpg"
                    progress_bar.update()
                    cv2.imwrite(save_name,symptom)

parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--source',type=str,required=True) 
# source (path of the directory containing the annotations)
# Parse the argument
args = parser.parse_args()

generated_symptoms(args.source)

