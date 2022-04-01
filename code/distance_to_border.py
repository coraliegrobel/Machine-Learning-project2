""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains the functions to get the minimum distance from a point 
    to the border of the image.
"""
def min_distance_to_border(point, image_size):
    """
    @Inputs:
        point: The point that we want to calculate the minimum distance to the border.
        image_size: The size of the image.
    @Outputs:
        min_distance_to_border
    """
    return min(point[0], image_size[0]-point[0], point[1], image_size[1]-point[1])