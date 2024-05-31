# Arkema 2024 Project
This repo contains the work for the Arkema 2024 project. The project focused on using images of paints on wood to predict the ratings of the wood over several modes of failure.

## Separating Sections
We were given images of racks which contained several panels. Our first task was to segment the racks into individual panels.
To do this we created the segmenter (under `segmenter.py`) which performs human-assisted segmentation. Due to the slight variations in color, a human is required to make sure the panels are separated.

This application shows images of racks and the user must click the top left and bottom right of the panel to save it as an image. The dependencies required for this application are under `segment_requirements.txt`.

## Classification Models
The next task was to use the newly-acquired panel images to predict ratings for seven modes of failure including:
* Erosion
* Checking
* Cracking
* Flaking
* Peeling
* Chalking
* Mildew/Algae

All information related to training the models is in the python notebook `model_training.ipynb`. This notebook contains all of the models applied to this dataset and the results of the models. The dependencies required for this notebook are under `requirements.txt`.
The command to install the proper version of pytorch is below.
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Extra File Information
* The JavaScript file, `excel_table2csv.js`, is the file used to convert Arkema's labels from an excel document into a csv format. This is necessary to keep the label format consistent and accurate (no human error from retyping values). 
