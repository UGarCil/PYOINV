# This module was create on 11/11/2021
# It produces a log in file while running the different images and trying to match with their respective
# elements in the taxonomic table. Any mismatch will be taken as an Exception and added to the log file


import logging
import os
from os.path import join as jn



logFileName = "CriticalErrors.txt"
filePath = jn(os.getcwd(), logFileName)


def findInDf(image, stng, trgt_df, colName, sheet_name, file_name):
    img_name = image.split("/")[-1]
    with open(jn(os.getcwd(),logFileName), "a") as logFile:
        if stng not in trgt_df[colName].unique():
            logFile.write("{}: {} wasn't found in column {} of sheet {} in file {} \t{}\n".format(img_name, stng, colName, sheet_name, file_name,image))
            

def eval_imgLenght(img_list):
    imageNames = [x.split('/')[-1] for x in img_list]
    _String = "{} The length in the name of these files doesn't match the first 22 characters + underscore symbol expected by Pioinv {} \n".format(("#"*10), ("#"*10))
    with open(jn(os.getcwd(),logFileName), "a") as logFile:
        for indx, img in enumerate(imageNames):
            img_len = len(img.split("_")[0])
            if img_len != 22:
                _String += "{}\t{}\n".format(img, img_list[indx])
        if len(_String.strip().split("\n"))  != 1: #if there's anything in the _String other than "#####" then there's at least one mistake
            _String += "{}\n\n".format("#"*50)
            logFile.write(_String)


# Log into the CriticalErrors.txt if there are any issues when running the initial assessment
def eval(img_list, tax_Tuple, struc_Tuple, view_Tuple):
    taxonomic_df, tx_df_sheet, tx_df_name = tax_Tuple
    struct_df, st_df_sheet, st_df_name = struc_Tuple
    views_df, vw_df_sheet, vw_df_name = view_Tuple
    
    logging.info("Searching for errors in the dataset..")



    if os.path.exists(filePath):
        logging.info("Creating new log file: CriticalErrors.txt")
        os.remove(filePath)
    open(filePath, "w").close()

    eval_imgLenght(img_list)

    for img in img_list:
        imageName = img.split("/")[-1]
        # Following variables have same name as the columns they represent
        # Example: INVTUXV212fcepidTXV058_400X_E2B.jpg
        invSpCode = imageName[0:10] #Ex. INVTUXV212 
        findInDf(img, invSpCode, taxonomic_df, "MSP_CODE", tx_df_sheet, tx_df_name)
        # sexCo = imageName[10] #Ex. f for female
        # metCo = imageName[11] #Ex. c or p for SEM or photo
        parCo = imageName[12:15] #Ex. epi for epigynum
        findInDf(img, parCo, struct_df, "AcrStr", st_df_sheet, st_df_name)
        vieCo = imageName[15] #Ex. d for dorsal view
        findInDf(img, vieCo, views_df, "AcrView", vw_df_sheet, vw_df_name)
        vouCo = imageName[16:22] #Ex. TXV058 for photovoucher
        findInDf(img, vouCo, taxonomic_df, "VOUCOD", tx_df_sheet, tx_df_name)
        # magCo = imageName.split('_')[1] #Ex. 400X for magnification
        # micCo = imageName.split('_')[2].split('.')[0] #Ex. _E2B for microscope model
        # ftyCo = imageName.split('.')[1] #Ex. .jpg for image extension
    with open(jn(os.getcwd(), logFileName), "r") as file:
        file = file.readlines()
        if len(file) == 0:
            logging.info("No errors found in the dataset (hooray!)")
            return (True)
            
        else:
            logging.critical("Critical errors found in the name of the images. Open CriticalErrors.txt and fix them before running Pyoinv again")
            return(False)