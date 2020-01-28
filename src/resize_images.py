
import glob
import os
import shutil
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from PIL import Image


def make_image_thumbnail(filename):
    """
    Resize image for CNN

    INPUT
        filename: str, required; string of image to be processed
    
    OUTPUT
        Resized image, saved to directory
        String of filename with directory
    """
    # The thumbnail will be named "<original_filename>_thumbnail.jpg"
    base_filename, file_extension = os.path.splitext(filename)
    thumbnail_filename = f"{base_filename}{file_extension}"
    
    thumbnail_filename = thumbnail_filename.replace("train", "train_resized")

    # Create and save thumbnail image
    image = Image.open(filename)
    image.thumbnail(size=(256, 256))
    image.save(f"{thumbnail_filename}", "jpeg")

    return thumbnail_filename

def process_images():
    """
    Create a pool of processes to resize images.
    One process created per CPU
    """

    with ProcessPoolExecutor() as executor:
        
        # Get a list of files to process
        image_files = glob.glob("../data/train/*.jpeg")

        # Process the list of files, but split the work across the process pool to use all CPUs
        zip(image_files, executor.map(make_image_thumbnail, image_files))

def move_images(df):
    """
    Move images to folder with labels
    """

    [os.mkdir(f"../data/train_resized/{val}") for val in list(range(0,5))]



if __name__ == '__main__':
    process_images()

    # df_labels = pd.read_csv("../data/trainLabels.csv")

    # dict_images = dict(zip(df_labels.image, df_labels.level))  
