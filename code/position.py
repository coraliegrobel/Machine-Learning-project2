""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions to get the position of a body part in an image.
"""
def get_body_part_pos(body_part_to_index_dictionnary, body_part, prediction_df):
    """
    @Description: This function will calcul the position of a body part that is not part of openPifPaf.
    @Inputs:
        body_part_to_index_dictionnary: The dictionnary linking the string of the body parts
            to the index of the body part in the prediction list made by openPifPaf.
        body_part: A string of a body part that is not detected by openPifPaf.
        prediction_df: Predictions done for a human in an image in panda data frames.
    @Outputs:
        wanted_pos: The position of the body part in the image. If not found, (0,0).
    """
    wanted_pos = [0,0]

    if body_part == 'forehead' or body_part == 'right-cheek' or body_part == 'left-cheek':
        nose_index = body_part_to_index_dictionnary.get("nose")
        nose_pos = prediction_df[nose_index:nose_index+1]
        left_eye_index = body_part_to_index_dictionnary.get("left-eye")
        l_eye_pos = prediction_df[left_eye_index:left_eye_index+1]
        right_eye_index = body_part_to_index_dictionnary.get("right-eye")
        r_eye_pos = prediction_df[right_eye_index:right_eye_index+1]
        middle_eye_pos = [int(round((int(l_eye_pos.y)+int(r_eye_pos.y))/2)), 
                            int(round((int(l_eye_pos.x)+int(r_eye_pos.x))/2))]
        nose_m_eye_distance = [middle_eye_pos[0] - int(nose_pos.y), 
                                middle_eye_pos[1] - int(nose_pos.x)]
        if body_part == 'forehead':
            wanted_pos = [middle_eye_pos[0] + nose_m_eye_distance[0], 
                                    middle_eye_pos[1] + nose_m_eye_distance[1]]
        if body_part == 'right-cheek':
            wanted_pos = [int(r_eye_pos.y) - nose_m_eye_distance[0], 
                                    int(r_eye_pos.x) - nose_m_eye_distance[1]]
        if body_part == 'left-cheek':
            wanted_pos = [int(l_eye_pos.y) - nose_m_eye_distance[0], 
                                    int(l_eye_pos.x) - nose_m_eye_distance[1]]
    return wanted_pos
        
def get_body_parts_position(body_part_to_index_dictionnary, body_parts, predictions_df):
    """
    @Inputs:
        body_part_to_index_dictionnary: The dictionnary linking the string of the body parts
            to the index of the body part in the prediction list made by openPifPaf.
        body_parts: The list of the body parts to found.
        predictions_df: List of predictions done per images in panda data frames.
    @Outputs:
        body_parts_pos: The list of positions of each body_part of each human in each image.
            This variable indices are: [image][human][body_part].
    """
    # Be carefull that the indices of the temperatur matrix and those of the image are inversed : x,y => y,x
    body_parts_pos = []
    for image in range(len(predictions_df)):
        human_pos = []
        for human in range(len(predictions_df[image])):
            body_pos = []
            for body_part in body_parts:
                index = body_part_to_index_dictionnary.get(body_part)
                if index < 0:
                    body_pos.append(get_body_part_pos(
                        body_part_to_index_dictionnary, body_part, predictions_df[image][human],
                    ))
                else:
                    body_pos.append([int(round(predictions_df[image][human][index:index+1].y)),
                        int(round(predictions_df[image][human][index:index+1].x))]
                    )
            human_pos.append(body_pos)
        body_parts_pos.append(human_pos)
    return body_parts_pos