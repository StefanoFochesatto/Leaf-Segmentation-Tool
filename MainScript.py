#!/usr/bin/env python3
#################### Dependencies #################### 
# For Data Management
import numpy as np
# For Directory Management
import os 
# For Image Processing
import cv2  
import copy

## For Directory dialog windows
import tkinter
from tkinter import filedialog
from tkinter import messagebox
root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

MaskCoordinatesList = []
MaskCoordinates = []


def click_event(event, x, y, flags, params):
	global MaskCoordinates
	
    # Listening for Left Click
	if event == cv2.EVENT_LBUTTONDOWN:

        # Print and Append Coordinates
		#print(x, ' ', y)
		MaskCoordinates.append((x, y))

        # Display Coordinates 
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(imgCopy,'+', (x,y), font, .2, (255,164,0))
		cv2.imshow('image', imgCopy)

	# Listening for Right Click	
	if event==cv2.EVENT_RBUTTONDOWN:

        # Print and Append Coordinates
		#print(x, ' ', y)
		MaskCoordinates.append((x, y))

		# Display Coordinates 
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(imgCopy,'+', (x,y), font, .2, (255,164,0))
		cv2.imshow('image', imgCopy)


# Driver function for MaskCoordinates array generation
# This function will display the input image and defines all the 
# logic for interacting with the script. 
def generateMasks(imgCopy):
    cv2.namedWindow('HerbariumImage', cv2.WINDOW_AUTOSIZE)
    cv2.startWindowThread()
    # Displaying the image
    cv2.imshow('image', imgCopy)

    # Running MouseClick Callback
    cv2.setMouseCallback('image', click_event)

    
    while True:
        k = cv2.waitKeyEx(0) & 0xFF
        print(k)

        # Pressing the space bar key appends MaskCoordinate to MaskCoordinatesList, to be cropped out later on. 
        if k == 32:
            global MaskCoordinates
            global MaskCoordinatesList
            MaskCoordinatesList.append(MaskCoordinates)
            MaskCoordinates = []
        # Exiting when a esc key is pressed, so next step in parent for loop can display the next image
        if k == 27:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break



def ImageProcess(img, filename, SavePath):

    for i in range(len(MaskCoordinatesList)):

        if len(MaskCoordinatesList[i]) == 0:
            return
        else:
            pts = np.array(MaskCoordinatesList[i])
            
            ## Cropping the bounding rectangle
            rect = cv2.boundingRect(pts)
            x,y,w,h = rect
            cropped = img[y:y+h, x:x+w].copy()

            ## Generating the Mask
            pts = pts - pts.min(axis=0)
            mask = np.zeros(cropped.shape[:2], np.uint8)
            cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

            ## Removing everything outside the Mask with bitwise operation
            dst = cv2.bitwise_and(cropped, cropped, mask=mask)

            ## Saving the image to the save file path
            SaveFileName = filename[:-4] + '_' + str(int(i)) + '.jpg'
            print(SaveFileName)
            os.chdir(SavePath) # We have to set the path every time since cv2 can't handle relative paths without it.
            cv2.imwrite(SaveFileName, dst)


def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir


#################### Main Script ####################
if __name__ == "__main__":

    ## Directory Management
    path = search_for_file_path()
    os.chdir(path) #Change the working directory to the TimeLapse directory
    SegmentationMaskList = [] #Pull the current list of files in TimeLapse directory
    for file in os.listdir(path):
        if file.endswith(".jpg") and not file.startswith('.'): 
            SegmentationMaskList.append(file)
    
    SavePath = os.path.join(path, 'LeafSegmentation')
    os.mkdir(SavePath)

    ## MainLoop Iterating through all images in a directory. 
    for i in SegmentationMaskList:
            os.chdir(path) # Change the working directory to the TimeLapse directory
            # Read in image with segmentation mask
            img = cv2.imread(i)
            # Pass a copy to generate the masks (removes indicators from final segmentation)
            imgCopy = img.copy()
            generateMasks(imgCopy)
            # Pass original to image processing
            ImageProcess(img, i, SavePath)
            MaskCoordinatesList = []
            