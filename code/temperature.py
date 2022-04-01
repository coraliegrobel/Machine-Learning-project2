""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions to get the temperature of a position in an image.
"""
def get_temperatures(thermal_matrices, body_parts_pos):
    """
    @Inputs:
        thermal_matrices: The dictionnary linking the string of the body parts
            to the index of the body part in the prediction list made by openPifPaf.
        body_parts_pos: The list of positions of each body_part of each human in each image.
            This variable indices are: [image][human][body_part].
    @Outputs:
        body_parts_temps: The list of temperatures of each body_part of each human in each image.
            This variable indices are: [image][human][body_part].
    """
    body_parts_temps = []
    for image in range(len(thermal_matrices)):
        human_temps = []
        for human in range(len(body_parts_pos[image])):
            body_temps = []
            for body_part_pos in range(len(body_parts_pos[image][human])):
                body_temps.append(
                    thermal_matrices[image][body_parts_pos[image][human][body_part_pos][0]]
                    [body_parts_pos[image][human][body_part_pos][1]]
                )
            human_temps.append(body_temps)
        body_parts_temps.append(human_temps)
    return body_parts_temps