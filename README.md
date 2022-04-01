# Machine learning for flir temperature extraction
Thermal imaging is based upon the study of emitted infrared radiation. The output of thermal camera typically represent an array of the temperature measured at each pixel. In this study, we will use different machine learning models to detect specific parts of the human body, such as the nose and wrists and extract the temperature at these points.
With this information we would be able to adjust in real time the air conditioning of a room or building, such that the persons in it neither feel too cold or too warm at any time.
For the body parts recognition, we used machine learning algorithms that were trained and rely on RGB images for their prediction.
We adapted our temperature array to a grayscale image to make them readable to our models. We compared the different algorithms on RGB and grayscale images to find the best possible model for our study.
We found that both image type could give satisfying results when matched with an appropriate model.
<object data="https://github.com/CS-433/ml-project-2-ccd_ml_part2/blob/main/Machine_learning_for_flir_temperature_extraction.pdf" type="application/pdf" width="700px" height="700px">
<embed src="https://github.com/CS-433/ml-project-2-ccd_ml_part2/blob/main/Machine_learning_for_flir_temperature_extraction.pdf">

<p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/CS-433/ml-project-2-ccd_ml_part2/blob/main/Machine_learning_for_flir_temperature_extraction.pdf">Download PDF</a>.</p>
</embed>
</object>

## Installation

1.You can download the code to run the models from the github repository [Github](https://github.com/CS-433/ml-project-2-ccd_ml_part2)

Clone the repository:

```bash
git clone https://github.com/CS-433/ml-project-2-ccd_ml_part2
```
```bash
pip install -r /path/to/requirements.txt
```
## How to run the program

To run the program, go in the project repository (in the folder code) and run for example the following command :

```bash
cd code
python body_parts_temperature.py -s -g -n --model shufflenetv2k30 --body_parts forehead left-cheek right-wrist
```

### What will happen

It will get all the images in the exemple_image folder. Then convert the images in normalised grayscale images and finally send them to Openpifpaf using the model shufflenetv2k30 to detect the forehead, the left-cheek and the right-wrist.

### How to use it with your own images

1. Add the csv and images files in the *data* folder. (The images need to be in jpg and the csv files structure need to be respected. (cf. example_data/examples_csv for examples)).
2. Use the argument -csv <csv_path> and -p <images_path> to give the paths to the program.
(-s make the algorithm show the results.)
```bash
cd code
python body_parts_temperature.py -csv <csv_path> -p <images_path> -s ...
```

### How to use it with a live stream

This part of the code is an example of what it could be if we were using the thermal camera as a live stream.
But here we are using the webcam of the computer and sending the first color channel as temperatur.
```bash
cd code
python live_stream.py
```
Click on the live_stream window and prerss q to stop it.

https://user-images.githubusercontent.com/44364136/147221726-c4c3b943-1929-4004-bb58-c62bf6850c7c.mp4

## Methods and parameters

You can use the following command to have informations about the algorithm and its parameters :

```bash
cd code
python body_parts_temperature.py -h
```
![view](/git_images/help_file.png)

## Code content

You can find more detail about the code in the folder [*code*](https://github.com/CS-433/ml-project-2-ccd_ml_part2/tree/main/code).
It contains a jupyter notebook [main_final.ipynb](https://github.com/CS-433/ml-project-2-ccd_ml_part2/blob/main/code/main_final.ipynb) where you can follow the flow of our reasoning and the different ideas we had during this project. You will also be able to observe all the plots and tables that we used to compare the different methods and models.
It also contains .py files that contains different functions that are either used in the notebook or in our main program, [body_parts_temperature.py](https://github.com/CS-433/ml-project-2-ccd_ml_part2/blob/main/code/body_parts_temperature.py).