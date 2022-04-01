""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains all the functions to give a feedback to the user.
"""
import matplotlib.pyplot as plt

def show_results(images_name, images, body_parts, body_parts_pos, body_parts_temps):
    """
    @Description: Show the images used and the body parts detected in a new window and 
                    print their corresponding temperatures in the terminal.
    @Inputs:
        images_name: The name of the images used in order.
        images: The list of images used by openpifpaf,
        body_parts: The body parts used in order.
        body_parts_pos: The list of positions of each body_part of each human in each image.
                        This variable indices are: [image][human][body_part].
        body_parts_temps: The list of temperatures of each body_part of each human in each image.
                        This variable indices are: [image][human][body_part].
    """
    for im in range(len(images)):
        print("In image", images_name[im])
        plt.imshow(images[im])

        for human in range(len(body_parts_temps[im])):
            for body_part in range(len(body_parts)):
                number = human*len(body_parts) + body_part
                if body_parts_pos[im][human][body_part] == [0,0]:
                    print("The ", body_parts[body_part], number,
                        "is not detected in this image.")
                    continue
                cur_pos = [body_parts_pos[im][human][body_part][1], body_parts_pos[im][human][body_part][0]]
                plt.scatter(cur_pos[0], cur_pos[1], s=4, c='blue')
                plt.text(cur_pos[0], cur_pos[1], str(number))
                print("The temperature of the ", body_parts[body_part], number,
                        "is", body_parts_temps[im][human][body_part], "(in blue).")

        plt.show()