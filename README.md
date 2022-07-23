# Leaf-Segmentation-Tool

This script is essentially a polygonal cropping tool, but was made with the intended use of generating leaf level segmentation masks by hand. 

## Getting Started

Navigate to the repository directory and run the following command, 
```
 pip install -r requirements.txt
```
This will install the necessary dependancies. Note that we are using an older version of 
open-cv, I have found it to be more compatible with the cv2.imshow() function. 

Now you should be able to run the main script with, 
```
python MainScript.py 
```

From here a file dialog window will appear, simply select the directory which contains the images you want to crop. For an example select the 'Example' folder. 

The script will display the an image to the screen, now use the cursor to click points around the leaf you wish to crop (in a counterclockwise or clockwise direction), and once you are satisfies with a crop press the space bar to save the mask. Repeat until you have cropped all the leafs you wish to use. Then press the esc key to display the next image. 

