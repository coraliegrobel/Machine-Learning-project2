""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Links: https://openpifpaf.github.io/intro.html
@Description : Parser used to get the parameter given through the terminal to the python file.
"""
import argparse

description = (
    "The main function of this file will first load the images in the correct format " +
    "to then be able to use openPifPaf to detect body parts in thermal images and " +
    "finaly get the temperature at the previously found positions and return the results."
)

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--path_to_jpg', '-p', dest='path_to_jpg', default='../example_data/example_image/',
                    help='This is the path to the input images.')
parser.add_argument('--path_to_csv', '-csv', dest='path_to_csv', default='../example_data/example_image/',
                    help='This is the path to the input temperature csv files.')
parser.add_argument('--model', dest='model', default='shufflenetv2k30-wholebody',
                    choices=['resnet50', 'shufflenetv2k16-wholebody', 'shufflenetv2k16',
                    'shufflenetv2k16-withdense','shufflenetv2k30-wholebody', 'shufflenetv2k30'],
                    help='This is model used for openpifpaf')
parser.add_argument('--show', '-s', dest='show', default=False, action='store_true',
                    help='Using this parameter show the result.')
parser.add_argument('--grayscale', '-g', dest='grayscale', default=False, action='store_true',
                    help=('Using this parameter will make only use' +
                    ' the temperature csv file.'))
parser.add_argument('--normalisation', '-n', dest='using_normalisation', default=False, action='store_true',
                    help=('Using this parameter combined with the grayscale images will stretch the termal' +
                    ' matrix between min_temp and max_temp.'))
parser.add_argument('--min_temp', '-min_t', dest='min_temp', default=20,
                    help=('This parameter is the minimum temperature that will be used for normalisation.'))
parser.add_argument('--max_temp', '-max_t', dest='max_temp', default=40,
                    help=('This parameter is the maximum temperature that will be used for normalisation.'))
parser.add_argument('--body_parts', nargs='+', dest='body_parts', default="nose",
                    choices=['nose', 'left-eye', 'right-eye', 'left-ear',
                        'right-ear', 'left-shoulder', 'right-shoulder', 
                        'left-elbow', 'right-elbow', 'left-wrist', 'right-wrist',
                        'navel', 'chin', 'forehead', "right-cheek", "left-cheek"], type=str,
                    help='A/some body part/s where to detect the temperature.')

def create_parser():
    return parser.parse_args()