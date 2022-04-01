""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions that use openPifPaf functionnalities.
"""
import openpifpaf
from files_convertion import convert_in_panda_array

def get_PifPAf_prediction(images, model):
    """
    @Inputs:
        images: List of images to predict human position.
        model: Name of the neural network model to use with openPifPaf.
    @Outputs:
        predictions_df: List of predictions done per images in panda data frames.
    """
    predictor = openpifpaf.Predictor(checkpoint=model)
    predictions = []
    gt_anns = []
    image_meta = []
    for i in range(len(images)):
        res1, res2, res3 = predictor.pil_image(images[i])
        predictions.append(res1)
        gt_anns.append(res2)
        image_meta.append(res3)
    
    predictions_df = convert_in_panda_array(predictions)
    return predictions_df