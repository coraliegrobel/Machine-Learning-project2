""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions to get the position of a body part in an image.
"""

from pifpaf import get_PifPAf_prediction
from show_results import *
from distance_to_border import *
from position import *
import pandas as pd
import numpy as np
import glob
import csv
import matplotlib.pyplot as plt
import time

def load_folder_csv(folder):
    """
    @Input:
        folder: The path to the directory containing the csv files.
    @Outputs:
       data: List of the csv thermal matrices in numpy format.
    """
    reader = []
    data = []
    files = folder + '/*.csv'
    for file in glob.glob(files):
        with open(file, 'r') as file_opened:
            reader = csv.reader(file_opened)
            data.append(np.array(list(reader), dtype='float'))
            
    print(len(data))
    return data

def plot_image(positions, label_per_people, image, body_part):
    """
    @Input:
        positions: Positions of the body part of interest predicted by Openpifpaf
        label_per_people: Positions of the body part of interest labeled
    """
    fig = plt.figure(figsize=(5, 7))
    plt.imshow(image[0])
    for k in range(len(body_part)):
        plt.scatter(positions[0][0][k][1], positions[0][0][k][0],s=4, c='blue')
        plt.scatter(positions[0][1][k][1], positions[0][1][k][0],s=4, c='green')
        plt.scatter(label_per_people[0].iloc[k].X, label_per_people[0].iloc[k].Y, s = 4, c='red')
        plt.scatter(label_per_people[1].iloc[k].X, label_per_people[1].iloc[k].Y, s = 4, c='yellow')
    plt.axis('off')
    plt.legend(["predicted 1", "predicted 2", "label 1", "label 2"], loc ="lower right")
    plt.show()

def labeled_people(label):
    '''
    @Definition : For an image label, returns a dictionnary with a data frame per people of the image
    @Input:
        label : label of an image with all people
    @Output:
        label_per_people : dictionnary with data frame of label per people
    '''
    peoples = int(len(label)/8)
    label_per_people = {}
    label_per_people[0] = label.iloc[0:8]
    start = 8
    stop = start + 8
    if peoples > 1 :
        for people in range(1,peoples) :
            label_per_people[people] = label.iloc[start:stop]
            start = stop
            stop = stop + 8
    return label_per_people

def calculate_mean_euclidean(body_parts, positions, model, label, image_size):
    '''
    @Definition : For all body parts of interest, returns the euclidean distance between the labeled position of the body 
    part and the predicted position by open pifpaf. Return also the mean euclidan distance of this model
    on this image.
    
    @Inputs:
        body_parts : np.array of body parts of interest
        positions : position of body parts of interest predicted by openpipaf
        model : model of openpifpaf to predict
        label : positions of body parts of interest labeled 
        max_pixel_x : size of image in x
        max_pixel_y : size of image in y

    @Outputs:
        mean : mean euclidean distance over all body parts of interest
        euclidean : data frame of eclidian distance per body part
    '''
    euclidean = pd.DataFrame()
    for body_part in range(len(body_parts)):
        euclidean.at[body_parts[body_part], model] = np.sqrt(np.power(label.iloc[body_part].X - positions[body_part][1],2) + \
                np.power(label.iloc[body_part].Y - positions[body_part][0],2))

        if euclidean.iloc[body_part][model] > 100 :
            # it means the point is missing
            euclidean.at[body_parts[body_part], model] = min_distance_to_border(label.iloc[body_part], image_size)
    mean = euclidean.mean(axis= 0, skipna = True).values[0]

    return mean, euclidean

def evaluation(all_models, body_part, images, label, body_part_to_index_dictionnary):
    '''
    @Definition : Evaluation of all models by calculating the euclidean distance for each body part and 
    the number of missing point for each model.    
    @Inputs:
        all_models : all models of openpifpaf that we want to evaluate
        body_part : np.array of body parts of interest
        images : all the images on which we want to evaluate our model
        label : all coordinates of the labeled points
        body_part_to_index_dictionnary :
    @Outputs:
        percentage_detected : mean percentage of people detected
        all_euclideans : mean euclidean distance per model per body part
        all_euclideans_weighted : mean weighted euclidean distance per model per body part
        people_detected_per_model : 
    '''
    all_euclideans = pd.DataFrame(index = body_part)
    all_euclideans_weighted = pd.DataFrame(index = body_part)
    percentage_detected = pd.DataFrame(index = body_part)
    people_detected_per_model = pd.DataFrame(index = ['false positive', 'false negative'])
    time_ = pd.DataFrame()
    for model in all_models :
        people_detected = pd.DataFrame(index = ['openpifpaf_detection', 'real_number', 'difference'])
        euclidean_per_model = pd.DataFrame(index = body_part)
        euclidean_per_model_weighted = pd.DataFrame(index = body_part)
        missing_point_per_model = pd.DataFrame(index = body_part)

        a= time.time()
        predictions_df = get_PifPAf_prediction(images, model)
        b = time.time()
        time_.at['time', model] = (b-a)/len(predictions_df)

        positions = []
        positions = get_body_parts_position(body_part_to_index_dictionnary, body_part, predictions_df)
        number_people = 0
        for image in range(len(predictions_df)) :
            label_per_people = labeled_people(label[image])
            number_people += len(label_per_people)
            for people in range(len(label_per_people)):
                mean = []
                euclidean = {}
                for human in range(len(predictions_df[image])):
                    temp_mean, euclidean[human] = calculate_mean_euclidean(body_part, positions[image][human], model, label_per_people[people],
                    images[image].size)
                    mean.append(temp_mean)
                if len(mean) == 0:
                    df = pd.DataFrame(index = body_part)
                    df[model] = df.apply(lambda x :  float('Nan'))
                    euclidean_per_model['image' + str(image) + '_model_' + str(model) + '_people_' + str(people)] = df[model]
                else:
                    index = np.where(mean == np.amin(mean))
                    euclidean_per_model_weighted['image' + str(image) + '_model_' + str(model) + '_people_' + str(people)]\
                        = euclidean[index[0][0]][model]
                    euclidean[index[0][0]][model] = euclidean[index[0][0]][model].apply(lambda x : float('Nan') if x > 100 else x)
                    euclidean_per_model['image' + str(image) + '_model_' + str(model) + '_people_' + str(people)] = euclidean[index[0][0]][model]
                    missing_point_per_model['image' + str(image) + '_model_' + str(model) + '_people_' + str(people)] = \
                        euclidean_per_model['image' + str(image) + '_model_' + str(model) + '_people_' + str(people)]\
                            .apply(lambda x : np.isnan(x).sum())

            people_detected.at['openpifpaf_detection', 'image' + str(image) + '_model_' + str(model)] = len(euclidean)
            people_detected.at['real_number', 'image' + str(image) + '_model_' + str(model)] = len(label_per_people)
            people_detected.at['difference', 'image' + str(image) + '_model_' + str(model)] = len(euclidean) - len(label_per_people)
        percentage_detected[model] = 100 - (missing_point_per_model.sum(axis = 1) / number_people * 100)
        sum_pos = pd.DataFrame(people_detected[people_detected>0].sum(1))
        sum_neg = pd.DataFrame(people_detected[people_detected<0].sum(1))
        people_detected_per_model.at['false positive', model] = sum_pos.iloc[2].values[0]
        people_detected_per_model.at['false negative', model] = sum_neg.iloc[2].values[0]
        all_euclideans_weighted[model] = euclidean_per_model_weighted.mean(axis = 1)
        all_euclideans[model] = euclidean_per_model.mean(axis = 1, skipna = True)
    people_detected_per_model.at['Number total of people'] = number_people
        
    return percentage_detected, all_euclideans, all_euclideans_weighted, people_detected_per_model, time_