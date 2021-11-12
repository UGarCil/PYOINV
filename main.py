#!usr/bin/env/python
# Pyoinv 2.0: Create a webpage for standardized faunistic inventories
# File created on August 18th by Uriel Garcilazo. Comments as UGC
# The program receives a path representing the master folder from which images of species have been taken.
# Images are assumed to have been named following a standardized protocol

import os
from os.path import join as jn
import pandas as pd
from populateHtmls import populateHtmls
from CloneDirectories import clonedirectories
import logging
import evalError as eE

logging.basicConfig(filename="log.txt", level=logging.INFO,
    format='%(asctime)s; %(levelname)s; %(message)s')

# Find the path to the images' folder
currPath = os.getcwd()
pathImages = jn(currPath, "Images")

logging.info(f"{'#'*10}Starting Pyoinv{'#'*10}")

try:
    assert(os.path.isdir("Images")), "The folder images is mispelled or it doesn't exist"
except AssertionError as err:
    logging.critical("The folder images doesn't exist in the same folder as main.py. If it's there, verify it doesn't have extra letters, and first letter is uppercase. Please correct and run again")
    raise err

# path to master html folder and the html/css templates
os.mkdir("HTML_files") if "HTML_files" not in os.listdir(currPath) else print("There seems to be an HTML_files folder already. Some data loss could occur")
masterHtmlPath = jn(currPath, "HTML_files")
rootHtmlTemplates = jn(currPath, "html_templates")









# Evaluate if a Summary.txt file already exists
nameSummaryFile = "Summary_images_processed.txt"
if nameSummaryFile not in os.listdir(currPath):
    with open(jn(currPath, nameSummaryFile), "w") as file:
        file.write("Image_name\tSpecies\tStructure_and_view\timage_dir\n")
    logging.info(f"File '{nameSummaryFile}' created..")
else:
    with open(jn(currPath, nameSummaryFile), "a") as file:
        file.write((f"{'#####'}\t" *4) + "\n")
    logging.info(f"File '{nameSummaryFile}' created..")


# Variables naming the excel files
tax_df_Name = "SPPDATA_EX.xlsx"
struct_df_Name = "structureNomenclature.xlsx"



# Load excel table with taxonomic information on species
taxonomic_df = pd.read_excel(jn(currPath, tax_df_Name), engine='openpyxl')
taxonomic_df = taxonomic_df.astype(str)
taxonomic_df = taxonomic_df.fillna('')
# Load dataframes with information on the name and view of the different structures
views_df = pd.read_excel(jn(currPath, struct_df_Name), sheet_name="views", engine='openpyxl')
struct_df = pd.read_excel(jn(currPath, struct_df_Name), sheet_name="structures", engine='openpyxl')




def extractImagesList(path):
    # Consume Path with images of species and return a String with absolute path for those images, separated by newline 
    _String = ''
    for root, folder, files in os.walk(pathImages):
        for file in files:
            for format in ['.jpg', '.jpeg', '.tiff', ".png", ".gif"]:
                if file.lower().endswith(format):
                    _String += (jn(root,file))+ "\n"
            # _String += (jn(".\Images",folder, file))+ "\n" if file.endswith('.jpg')  else None
    return(_String)


def populateColumns(imageRow):
    # Consume absolute path of image name and fill in the columns if future excel table
    _String = '{}'.format(imageRow)
    # Extract information based on index and split
    imageRow = imageRow.split('/')


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

    # Evaluate whether or not the columns of structures and views contain the structure/view of the image 
    try:
        imageStructure = struct_df[struct_df["AcrStr"] == parCo]["Structure"].values[0]
    except:
        logging.critical("The column AcrStr doesn't contain the structure {}".format(parCo))
        raise ValueError("The column AcrStr doesn't contain the structure {}".format(parCo))
    try:
        imageStrucView = views_df[views_df["AcrView"] == vieCo]["View"].values[0]
    except:
        logging.critical("The column AcrView doesn't contain a view named '{}'".format(vieCo))
        raise ValueError("The column AcrView doesn't contain a view named '{}'".format(vieCo))
    leGor = "{} {} view".format(imageStructure, imageStrucView)

    # !!!cotBk was originally intended to express the desired order in which the images of different views would appear in the webpage
    # There might be other ways to decide. We'll come back to this variable later, but in the meantime is useful to have it as
    # an empty variable
    cotBk = ''

    # Let's read the SPPDATA dataframe to fill the last variables, which contain taxonomic information

    # We will use the name of the genus + species contained within the images' full path to find our species

    # searchQuery = imageRow[-3:-1] #where -3 is the third element from the end of the array to the left, and -1 is the first element in the array, which isn't included but serves as boundary
    # # Find the taxonomic information using the searchQuery
    try:
        searchQuery = taxonomic_df[taxonomic_df["MSP_CODE"] == imageName[0:10]]["SPECIES"].values[0]
    except:
        logging.critical("The voucher {} couldn't be found in your SPPDATA.xlsx. Please fix the issue and run the program again".format(imageName[0:10]))

    # searchQuery = imageRow[-3:-1] #where -3 is the third element from the end of the array to the left, and -1 is the first element in the array, which isn't included but serves as boundary
    # Find the taxonomic information using the searchQuery

    speciesRow = taxonomic_df[taxonomic_df["SPECIES"] == searchQuery]
    family = speciesRow["FAMILY"].values[0]
    genus = searchQuery.split(' ')[0]
    spp = searchQuery.split(' ')[1]
    sppName = searchQuery
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



logging.info("Retrieving images list..")
listImages = extractImagesList(pathImages).strip().replace('\\','/').split('\n')
logging.info("A list of images has been retrieved from the 'Images' folder")

# Name of column headers. For additional information look at Ex_Esquema...xlsx
EsHeaders = ["HR_OLD_ADDS", "IMAGENAME", "INVCO", "InvSP_CODE", "SEXCO", "METCO", "PARCO", "VIECO", "VOUCO", "MAGCO", "MICCO", "FTYCO", "LEGOR", "COTBK", "FAMILY", "GENUS", "SPP", "SPECIES", "WSC", "SPAUTH", "SPDISTPL", "VOUCO2", "LOCDATA", "DET", "FEMSPE", "MALSPE", "TAXNOT", "IMGAUT"]


# At this point, call the evalError module. If no error are detected, then proceed. Otherwise ask user to fix issues
if eE.eval(listImages, (taxonomic_df, "SPECIES DATA", tax_df_Name), (struct_df, "structures", struct_df_Name), (views_df, "views", struct_df_Name)):
    # Evaluate whether or not the folder Thumbnails already exists. If yes, ask user if overwrite, otherwise do nothing
    if "Thumbnails" not in os.listdir(currPath):
        clonedirectories(pathImages, "Thumbnails")
    else:
        userAnswer = input("There seems to be a Thumbnails folder already. Would you like to erase and rewrite its contents? It may take a while for large datasets [y/n]").lower()
        if userAnswer == "y":
            # Create a low resolution copy of the directory tree that contains the high resolution images
            clonedirectories(pathImages,"Thumbnails")
            logging.info("The new directory Thumbnails has been successfully created")
        else:
            logging.info("User decided not to create a new Thumbnails folder")


    # Make the dataframe of our new Esquema by first processing each of the image paths by adding values for the columns
    # specified in EsHeaders, then adding the edited row to a list. Then turn that list into a pandas dataframe
    newEsquema = []
    [newEsquema.append(populateColumns(row)) for row in listImages if len(row)!=0]
    # Turn the new list of lists (i.e. table) into a new array
    newEsquema_df = pd.DataFrame(newEsquema, columns=EsHeaders)

    # Save new Esquema into an excel file
    newEsquema_df.to_excel("Esquema.xlsx", engine='openpyxl')

    logging.info("File Eschema.xlsx successfully created")

    populateHtmls(newEsquema_df, rootHtmlTemplates, masterHtmlPath)

    print('''
    {}
    Thank you for using PYOINV. The program has finished running. You can find additional information on how your data was processed in the log.txt file located in the same folder as main.py.
    If you have any questions. You can find a summary of the image files processed in the folder {} feel free to contact the Alvarez-Padilla lab at fap@ciencias.unam.mx. Press enter to exit the program.
    {} 
    '''.format(("="*200),nameSummaryFile,("="*200)))
    logging.info("Pyoinv has finished running")
    input()
else:
    print("At least one critical error was found while trying to match images with their tags. Look at CriticalErrors.txt and fix issues. Then run Pyoinv again")
    input()