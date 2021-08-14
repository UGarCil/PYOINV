#!usr/bin/env/python
# This script extracts the information on the images located within a master folder, respecting its relative position
# It outputs an .txt file with the files

import os
from os.path import join as jn

path = os.getcwd()

def getImages():
    finalTable = []
    # This part provides the absolute path directory of all the images contained within their respective folder
    for root, folders, files in os.walk(path):
        imgPaths = ["{}\{}".format(root,file).replace(path,"") for file in files if file.endswith('.jpg')]
        for image in imgPaths:

            # Get rid of the name of the master folder
            firstSplit = image.split('\\',2)[2] + '\n'
            
            # The last element should have the image name only, but we want
            # the absolute path + image name
            # We get rid of the name of the species
            secondSplit = firstSplit.rsplit('\\',1)[0]
            
            # Separate by backslash and turn it into a list
            # to append the absolute path of the image instead
            row = (secondSplit.split('\\'))
            
            # make the full path to the image, add it to the row
            # Add row to main table
            row.append("{}\\{}".format(path,image))
            finalTable.append(row)

            
    # Return list ready to be read as a Dataframe (columns are indexed by number, not names)
    return (finalTable)

