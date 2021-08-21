#!usr/bin/env/python
# Pioinv 2.0: Create a webpage for standardized faunistic inventories
# File created on August 18th by Uriel Garcilazo. Comments as UGC
# The program receives a path representing the master folder from which images of species have been taken.
# Images are assumed to have been named following a standardized protocol

import os
from os.path import join as jn
import pandas as pd
from populateHtmls import populateHtmls
import logging


# Find the path to the images' folder
currPath = os.getcwd()
pathImages = jn(currPath, "Images")

# path to master html folder and the html/css templates
os.mkdir("HTML_files") if "HTML_files" not in os.listdir(currPath) else print("There seems to be an HTML_files folder already. Some data loss could occur")
masterHtmlPath = jn(currPath, "HTML_files")
rootHtmlTemplates = jn(currPath, "html_templates")

# Load excel table with taxonomic information on species
taxonomic_df = pd.read_excel(jn(currPath, "SPPDATA_EX.xlsx"))
taxonomic_df = taxonomic_df.astype(str)
taxonomic_df = taxonomic_df.fillna('')
# Load dataframes with information on the name and view of the different structures
views_df = pd.read_excel(jn(currPath, "structureNomenclature.xlsx"), sheet_name="views")
struct_df = pd.read_excel(jn(currPath, "structureNomenclature.xlsx"), sheet_name="structures")




def extractImagesList(path):
    # Consume Path with images of species and return a String with absolute path for those images, separated by newline 
    _String = ''
    for root, folder, files in os.walk(pathImages):
        for file in files:
            _String += (jn(root,file))+ "\n" if file.endswith('.jpg')  else None
    return(_String)


def populateColumns(imageRow):
    # Consume absolute path of image name and fill in the columns if future excel table
    _String = '{}'.format(imageRow)
    # Extract information based on index and split
    imageRow = imageRow.split('\\')

    # Following variables have same name as the columns they represent
    imageName = imageRow[-1]
    invCo = ""
    invSpCode = imageName[0:10]
    sexCo = imageName[10]
    metCo = imageName[11]
    parCo = imageName[12:15]
    vieCo = imageName[15]
    vouCo = imageName[16:22]
    magCo = imageName.split('_')[1]
    micCo = imageName.split('_')[2].split('.')[0]
    ftyCo = imageName.split('.')[1]

    # To fill the information on the view of the specimen for this particular image (i.e. row)
    # we use the views_df and struct_df dataframes 
    
    imageStructure = struct_df[struct_df["AcrStr"] == parCo]["Structure"].values[0]
    imageStrucView = views_df[views_df["AcrView"] == vieCo]["View"].values[0]

    leGor = "{} {} view".format(imageStructure, imageStrucView)

    # !!!cotBk was originally intended to express the desired order in which the images of different views would appear in the webpage
    # There might be other ways to decide. We'll come back to this variable later, but in the meantime is useful to have it as
    # an empty variable
    cotBk = ''

    # Let's read the SPPDATA dataframe to fill the last variables, which contain taxonomic information

    # We will use the name of the genus + species contained within the images' full path to find our species
    searchQuery = imageRow[-3:-1] #where -3 is the third element from the end of the array to the left, and -1 is the first element in the array, which isn't included but serves as boundary
    # Find the taxonomic information using the searchQuery

    speciesRow = taxonomic_df[taxonomic_df["SPECIES"] == ' '.join(searchQuery)]
    family = speciesRow["FAMILY"].values[0]
    genus = searchQuery[0]
    spp = searchQuery[1]
    sppName = ' '.join(searchQuery)
    wsc_number = speciesRow["WSP_NUM"].values[0]
    spAuth = speciesRow["SP_AUTHOR"].values[0]
    spDistPl = speciesRow["DIST"].values[0]
    vouchCo2 = speciesRow["VOUCOD"].values[0]
    locData = speciesRow["LOCALITY"].values[0]
    det = speciesRow["ID AUTHOR"].values[0]
    femSpe = speciesRow["FEMNUM"].values[0]
    malSpe = speciesRow["MALNUM"].values[0]
    taxNot = speciesRow["TAXON NOTES"].values[0]
    imgAut = speciesRow["SPPIMAUT"].values[0]
    

    


    _String += ("\t{}"*27).format(
        imageName, invCo, invSpCode, sexCo, metCo, parCo, vieCo, vouCo, magCo, micCo, ftyCo, leGor, cotBk,
        family, genus, spp, sppName, wsc_number, spAuth, spDistPl, vouchCo2, locData, det, femSpe, malSpe, taxNot, imgAut
    )
    return(_String.split('\t'))

listImages = extractImagesList(pathImages).split('\n')

# Name of column headers. For additional information look at Ex_Esquema...xlsx
EsHeaders = ["HR_OLD_ADDS", "IMAGENAME", "INVCO", "InvSP_CODE", "SEXCO", "METCO", "PARCO", "VIECO", "VOUCO", "MAGCO", "MICCO", "FTYCO", "LEGOR", "COTBK", "FAMILY", "GENUS", "SPP", "SPECIES", "WSC", "SPAUTH", "SPDISTPL", "VOUCO2", "LOCDATA", "DET", "FEMSPE", "MALSPE", "TAXNOT", "IMGAUT"]

# Make the dataframe of our new Esquema by first processing each of the image paths by adding values for the columns
# specified in EsHeaders, then adding the edited row to a list. Then turn that list into a pandas dataframe
newEsquema = []
[newEsquema.append(populateColumns(row)) for row in listImages if len(row)!=0]
# Turn the new list of lists (i.e. table) into a new array
newEsquema_df = pd.DataFrame(newEsquema, columns=EsHeaders)

# Save new Esquema into an excel file
newEsquema_df.to_excel("Esquema.xlsx")

populateHtmls(newEsquema_df, rootHtmlTemplates, masterHtmlPath)
