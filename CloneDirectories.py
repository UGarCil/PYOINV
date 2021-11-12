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

def clonedirectories(PathcloneFrom, nameDir):
    # Remove the existing Thumbnails directory if exists
    if os.path.exists(nameDir):
        logging.warning("Removing existing Thumbnails folder")
        shutil.rmtree(jn(currPath, "Thumbnails"))
    
    def isImage(fileName):
    # Look at the extension of the file, and if it looks like an image, give it back
        imgFormats = [".jpg",".png",".jpeg",".tiff"]
        for ext in imgFormats:
            if ext in fileName: return True
        return False

    # Make an exact copy of the folder tree that contains the images of our species
    logging.info("Cloning 'Images' folder to create Thumbnails folder..")
    
    thumbsFolder = jn(currPath, nameDir)
    try:
        def ignore_files(dir, files):
            return [f for f in files if os.path.isfile(os.path.join(dir, f))]
        shutil.copytree(PathcloneFrom, thumbsFolder, ignore= ignore_files)

    except:
        logging.critical("The folder {} couldn't be overwritten. Please make sure no other applications are using any of the folder's contents".format(nameDir))
    # then, lower the resolution of the new images using pillow
    listImagesNewFolder = ""

    for root, folder, files in os.walk(PathcloneFrom):
        imagesList = [jn(root,file) for file in files if isImage(file)]
        listImagesNewFolder += "\n".join(imagesList) + '\n'
    listImagesNewFolder = listImagesNewFolder.strip()
    totalNumImages = listImagesNewFolder.split('\n')
    logging.info("Pyoinv detected {} image files that will be converted into thumbnails".format(len(totalNumImages)))
    print("Pyoinv detected {} image files that will be converted into thumbnails. This might take a couple of minutes..".format(len(totalNumImages)))


    for indx, imagePath in enumerate(totalNumImages):
        try:
            # Notify the user in the screen about on the process of making thumbnails
            if indx % (int(len(totalNumImages)/10)) == 0:
                print("{:.2f}% of thumbnails completed".format((indx / len(totalNumImages))*100))
            if indx+1 == len(totalNumImages):
                print("{:.2f}% of thumbnails completed".format(((indx+1) / len(totalNumImages))*100))

            imageFile = Image.open(imagePath)
            # Change the images to a medium resolution
            possibleExts = [imagePath.replace(f"{x}Images{x}", f"{x}Thumbnails{x}") for x in ["/", "\\"]]
            for ext in possibleExts:
                if os.path.exists(ext):
                    imageFile.save(imagePath.replace("Images","Thumbnails"),quality=50)
        except:
            None if imagePath == "" else print("An error ocurred trying to change the resolution of {}".format(imagePath))
            logging.info("An error ocurred when trying to change the resolution of {}".format(imagePath)) if imagePath != "" else None

# if we're calling the module directly then call the function right away
if __name__ == "__main__":
    nameNewDir = "Thumbnails"
    pathToClone = jn(currPath, "Images")
    clonedirectories(pathToClone, nameNewDir)




