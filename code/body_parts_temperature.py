""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Links: https://openpifpaf.github.io/intro.html
@Description : This file is the core of our algorithms.
    It will use the functions in pifpaf.py, show_results.py and files_convertions.py to first
    load the images in the correct format to then be able to use openPifPaf to detect body parts 
    in thermal images and finaly get the temperature at the previously found positions and 
    return the results.
@Launch: python3.9 body_parts_temperature.py -h
"""
from os import path
import sys

from create_parser import *
from files_convertion import *
from pifpaf import *
from position import *
from temperature import *
from show_results import *

body_part_to_index_dictionnary = {"nose": 0, "left-eye": 1, "right-eye": 2, "left-ear": 3,
                        "right-ear": 4, "left-shoulder": 5, "right-shoulder": 6, 
                        "left-elbow": 7, "right-elbow": 8, "left-wrist": 9, 
                        "right-wrist": 10, "navel": 12, "chin": 30,
                        "forehead": -1, "right-cheek" : -2, "left-cheek" : -3}

def control_path(path_to_folder):
    # control that the path exists
    if not path.exists(path_to_folder):
        sys.exit(path_to_folder + "doesn't exist.")

def main(args, image=[[]], thermal_matrix=[[]]):
    """
    @Inputs:
        args: parser defining the parameters used.
        image: False if nothing is given, otherwise, it should be an image. (comming from live stream?)
        thermal_matrix: Matrix containing the temperatures. (comming from live stream?)
    @Outputs:
        images_name: The name of the images used in order.
        images: The list of images used by openpifpaf,
        thermal_matrices: The list of thermal matrix associated to the images.
        body_parts: The body parts used in order.
        body_parts_pos: The list of positions of each body_part of each human in each image.
            This variable indices are: [image][human][body_part].
        body_parts_temps: The list of temperatures of each body_part of each human in each image.
            This variable indices are: [image][human][body_part].
    """
    
    if isinstance(args.body_parts, str):
        body_parts = []
        body_parts.append(args.body_parts)
    else:
        body_parts = args.body_parts

    model = args.model
    if image!=[[]]:
        images_name = "LIVE"
        images = []
        images.append(image)
        thermal_matrices = []
        thermal_matrices.append(thermal_matrix)
    else:
        print('body_parts :', body_parts)

        control_path(args.path_to_jpg)
        control_path(args.path_to_csv)
        csv_files_name = path.join(args.path_to_csv, "*.csv")
        print('Input csv files path :', args.path_to_csv)

        print('Model :', model)

        if args.using_normalisation:
            print('The normalisation step will be done between:', args.min_temp, 'and', args.max_temp, 'degree celcius.')

        images_name = get_files_name(csv_files_name)
        thermal_matrices = get_csv(args.path_to_csv, images_name)
        if args.grayscale:
            images = transform_thermal_matrices_to_images(thermal_matrices, args.using_normalisation, 
                        args.min_temp, args.max_temp)
        else:
            images = get_jpg(args.path_to_jpg, images_name)

    predictions_df = get_PifPAf_prediction(images, model)

    body_parts_pos = get_body_parts_position(body_part_to_index_dictionnary, body_parts, predictions_df)
    body_parts_temps = get_temperatures(thermal_matrices, body_parts_pos)

    if args.show:
        show_results(images_name, images, body_parts, body_parts_pos, body_parts_temps)

    return images_name, images, thermal_matrices, body_parts, body_parts_pos, body_parts_temps

if __name__ == "__main__":
    args = create_parser()
    main(args)