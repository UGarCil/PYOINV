#!usr/bin/env/python
# Program created on Aug 13th 2021 by Uriel Garcilazo as part of BIOINV2.2 from Alvarez-Padilla lab. The script consumes input from three sources:
# - A text .txt file with the location of images 
# - An excel file with information on the taxonomy of a group of species
# - The structure of folders
# 
# It outputs an html with an inventory of the spiders
# 

import os
from os.path import join as jn 
import pandas as pd
from CloneFolderTree import nestingFolders
from Extract_images import getImages as getIMG

# Use the 2 vector matrix made in Extrac_images.py as a dataframe, with empty cells read as empty strings
df = pd.DataFrame(getIMG())
df = df.fillna('')
df = df.astype(str)


#If the file has been created before, chances are there's already information
# created for the inventories. beenHereBefore is a check point
beenHereBefore = False #If it stays False, then we're running this for the first time

# A ternary operator: make sure the folder we're trying to make doesn't already exist, then make it.
# If it does exist, set the var. beenHereBefore = True to update the checkpoint
beenHereBefore = True if "HTML_SpeciesTree" in (os.listdir(os.getcwd())) else os.mkdir(jn(os.getcwd(),"HTML_SpeciesTree"))
path = jn(os.getcwd(),"HTML_SpeciesTree") #root folder for recursively create htmls
cssPath = jn(os.getcwd(), "html_templates", "styles.css") #html path is dynamic, CSS path is not

# If we just created the folder with HTMLs, then we can start creating the folders for each of the species
# in our dataframe recursively, assigning them to their respective folders (e.g. species to their genus)
if not beenHereBefore:
    nestingFolders(df, path, cssPath)
else:
    print("There might be some data in the HTML species folder already. Erase the folder before continuing")



