import os
from os.path import join as jn
from PIL import Image
import shutil
import logging
# Clone all images in a folder, changing the resolution of images
# Consume a directory path and new directory name, produce a new directory tree

# logging.basicConfig(filename="Log.txt", level=logging.INFO,
#     format='%(levelname)s;%(asctime)s;%(message)s')

currPath = os.getcwd()
nameNewDir = "Thumbnails"
pathToClone = jn(currPath, "Images")

def clonedirectories(PathcloneFrom, nameDir):
    def isImage(fileName):
    # Look at the extension of the file, and if it looks like an image, give it back
        imgFormats = [".jpg",".png",".jpeg",".tiff"]
        for ext in imgFormats:
            if ext in fileName: return True
        return False
    # Make an exact copy of the high res images first
    thumbsFolder = jn(currPath, nameNewDir)
    try:
        shutil.copytree(PathcloneFrom, thumbsFolder)
    except:
        logging.warning("The folder {} already exists. Some data loss could occur".format(nameDir))
    # then, lower the resolution of the new images using pillow
    listImagesNewFolder = ""
    for root, folder, files in os.walk(thumbsFolder):
        imagesList = [jn(root,file) for file in files if isImage(file)]
        listImagesNewFolder += "\n".join(imagesList) + '\n'
    listImagesNewFolder = listImagesNewFolder.strip()

    for imagePath in listImagesNewFolder.split('\n')[:-1]:
        try:
            imageFile = Image.open(imagePath)
            # Change the images to a medium resolution
            imageFile.save(imagePath,quality=50)
        except:
            None if imagePath == "" else print("An error ocurred trying to change the resolution of {}".format(imagePath))


# clonedirectories(pathToClone, nameNewDir)




