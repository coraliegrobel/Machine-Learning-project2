""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions to get and/or transform the data 
    that we would like to use.
"""
import glob
from os import path
from PIL import Image
import pandas as pd
import numpy as np
import csv
from os import path

def get_files_name(path_to_files):
    """
    @Description: Get the names of all the files of the predefined format at 
        the wanted path, whitout the format extension.
    @Inputs:
        path_to_files: String of the path to the files. (ex:Images/*.jpg)
    @Outputs:
        names: List of the names of all files satisfying "path_to_files".
    """
    names = []
    for file in glob.glob(path_to_files):
        names.append(path.splitext(path.basename(file))[0])
    return names

def get_jpg(path_to_jpg, images_name):
    """
    @Inputs:
        path_to_jpg: The path to the directory containing the jpg images.
        images_name: The name of all images to use.
    @Outputs:
       List of the jpg images.
    """
    return [Image.open(path.join(path_to_jpg, file+".jpg")) for file in images_name]
    
def get_csv(path_to_csv, images_name):
    """
    @Inputs:
        path_to_csv: The path to the directory containing the csv files.
        images_name: The name of all images to use.
    @Outputs:
       thermal_matrices: List of the csv thermal matrices in numpy format.
    """
    reader = []
    data = []
    for file in images_name:
        with open(path.join(path_to_csv, file + ".csv"), 'r') as file_opened:
            reader = csv.reader(file_opened)
            data.append(list(reader))

    thermal_matrices = []
    for i in range(len(data)):
        thermal_matrices.append(np.array(data[i][6:], dtype='float'))
    return thermal_matrices

def convert_in_panda_array(predictions):
    """
    @Inputs:
        predictions: The list of predictions done by openPifPaf.
    @Outputs:
       predictions_df: The list of predictions done by openPifPaf in a pandas format.
    """
    predictions_df = []
    for i in range(len(predictions)):
        cur_predictions_df = []
        for j in range(len(predictions[i])):
            cur_predictions_df.append(pd.DataFrame(predictions[i][j].data))
        predictions_df.append(cur_predictions_df)
    
    for i in range(len(predictions)):
        for j in range(len(predictions[i])):
            predictions_df[i][j].rename(columns={0: 'x', 1: 'y', 2: 'proba'}, inplace=True)
    return predictions_df

def matrix_normalisation(thermal_matrices, min_temp, max_temp):
    """
    @Definition:
        It transform the matrixes so that each value smaller than min_temp are 0,
        each value bigger than max_temp are 255 and stretch linearly the rest between 0 and 255.
    @Inputs:
        thermal_matrices: The list of thermal matrices.
        min_temp: The temperature that will be matched to 0.
        max_temp: The temperature that will be matched to 255.
    @Outputs:
       grayscal_matrices: The list of thermal matrices stretched between 0 and 255.
    """
    grayscal_matrices = []
    for mat in thermal_matrices:
        new_mat = np.round((mat-min_temp)*(255/(max_temp-min_temp)))
        new_mat = np.where(new_mat < 0, 0, new_mat)
        new_mat = np.where(new_mat > 255, 255, new_mat)
        grayscal_matrices.append(new_mat)
    return grayscal_matrices

def matrix_stretching(thermal_matrices):
    """
    @Inputs:
        thermal_matrices: The list of thermal matrices.
    @Outputs:
       grayscal_matrices: The list of thermal matrices stretched between 0 and 255.
    """
    grayscal_matrices = []
    for mat in thermal_matrices:
        min_T = np.min(np.min(mat))
        max_T = np.max(np.max(mat))
        grayscal_matrices.append(np.round((mat-min_T)*(255/(max_T-min_T))))
    return grayscal_matrices

def transform_thermal_matrices_to_images(thermal_matrices, using_normalisation = True, 
                                            min_temp = 20, max_temp = 40):
    """
    @Inputs:
        thermal_matrices: The list of thermal matrices.
        using_normalisation: [Boolean]: Determine if we want to use the matrix stretching 
                                        with normalisation.
        min_temp: The minimum temperature that will use for normalisation.
        max_temp: The maximum temperature that will use for normalisation.
    @Outputs:
       grayscale_images: The list of grayscale images.
    """
    if using_normalisation:
        grayscal_matrices = matrix_normalisation(thermal_matrices, min_temp, max_temp)
    else:
        grayscal_matrices = matrix_stretching(thermal_matrices)

    grayscale_images = []
    for mat in grayscal_matrices:
        grayscale_image = Image.fromarray(mat)
        if grayscale_image.mode != 'RGB':
            grayscale_image = grayscale_image.convert('RGB')
        grayscale_images.append(grayscale_image)
    return grayscale_images