#!usr/bin/env/python3
# Iterate over the taxonomic ranks, represented as columns from a dataframe, to create html files

# The table that the user gives as SPPDATA should include all of the taxonomic levels that follow
# the highest rank found

import os
from os.path import join as jn
import pandas as pd
from shutil import copyfile
import logging
import random as rn

currPath = os.getcwd()
# test_df = pd.read_excel("Esquema.xlsx")
# test_df = test_df.fillna('')
# test_df = test_df.astype(str)

# rootTemplates = jn(currPath, "html_templates")
# masterHtmlPath = jn(currPath, "HTML_files")

def populateHtmls(df, rootHtmlTemplates, masterHtmlPath):
# Create a series of html files for each taxonomic level to the level of species
    # Assert the existence of the folder containing the html templates
    try:
        assert(os.path.isdir(rootHtmlTemplates)),"The folder html_templates doesn't exist"
    except AssertionError as err:
        logging.critical("The folder containing the html and css templates should always be named html_templates. Please fix before proceeding..")
        raise err


    # Create two additional folders, one for Menus and one for species htmls
    menusPath = jn(masterHtmlPath,"Menus")
    speciesHtmlPath = jn(masterHtmlPath,'Species')
    os.mkdir(menusPath) if not os.path.isdir(menusPath) else print("A folder named Menus already exists in your HTML folder. Some data loss could occur.")#, logging.warning("A folder named Menus already exists in your HTML folder. Some data loss could occur..")
    os.mkdir(speciesHtmlPath) if not os.path.isdir(speciesHtmlPath) else print("A folder named Species already exists in your HTML folder. Some data loss could occur.")#, logging.warning("A folder named Species already exists in your HTML folder. Some data loss could occur..")    

    # Path for html/css templates
    speciesTemplate = jn(rootHtmlTemplates, "speciesTemplate.html")
    TaxRankTemplate = jn(rootHtmlTemplates, "template.html")
    cssTemplate = jn(rootHtmlTemplates, "styles.css")

    # Assert the existence of each of the files above
    for eachpath in [speciesTemplate, TaxRankTemplate, cssTemplate]:
        try:
            assert(os.path.isfile(eachpath)), "The file {} is mispelled or it doesn't exist in the folder html_templates".format(eachpath.split('/')[-1])
        except AssertionError as err:
            logging.critical("The file {} is mispelled or it doesn't exist in the folder html_templates.".format(eachpath.split('/')[-1]))
            raise err

    # Taxonomic rank names below match column names from Esquema
    taxonomic_Ranks = ["CLASS","ORDER", "FAMILY", "SPECIES"]
    _String = ''

    def evaluateHighestRank(columns_df):
        #identify the highest rank available in a df's columns
        for indx, rank in enumerate(taxonomic_Ranks):
            if rank in columns_df: return (indx)

    def editHTML(pathToPopulate, isSpecies, taxonName, currentTaxLevel, tax_df):
    # Edit the html to the parameters needed for that particular taxonomic level
        def getChildTaxonList(columnName, tax_df, isIndex=False):
        # redact a string in html format that summarizes the families included in the dataframe
            _String_gctl = ''
            # Get  list with unique records for the taxonomic level of interest
            uniqueRecords = tax_df[columnName].unique()
            # And add each element into the list
            for name in uniqueRecords:
                if isIndex:
                    if taxonomic_Ranks[indxHighRank] == "SPECIES": #if the inventory only contains species, refer to the species elements directly
                        _String_gctl += '<li><a target= "wel" href="{}"><i>{}</i></a></li>\n'.format("./HTML_files/Species/{}.html".format(name),name)
                    else:
                        _String_gctl += '<li><a target= "invs" href="{}">{}</a></li>\n'.format("./HTML_files/Menus/{}.html".format(name),name)
                else:
                    if columnName == "SPECIES":
                        _String_gctl += '<li><a target= "wel" href="{}"><i>{}</i></a></li>\n'.format("../Species/{}.html".format(name),name)
                    else:
                        _String_gctl += '<li><a target= "invs" href="{}">{}</a></li>\n'.format("../Menus/{}.html".format(name),name)
            return(_String_gctl)

        def fillDescription (taxname):
        # Consumes a string with the name of a species and uses df (free var.) and return species description
            # Because names in Esquema are repeated based on number of images for each voucher, we take one of such images,
            # doesn't matter which one, to populate the empty string
            taxrow = df[df["SPECIES"] == taxname].head(1)
            Des = ''
            Des += "<b>Species Code: </b>" + (taxrow["InvSP_CODE"].values[0]) + ". "
            Des += "<b>Locality for photographed specimens: </b>" + (taxrow["LOCDATA"]).values[0] + ". "
            Des += "<b>Specimens:</b> Female, " + (taxrow["FEMSPE"]).values[0] + ", Male " + (taxrow["MALSPE"].values[0]) + ". "
            Des += "<b>Species ID: </b>" + (taxrow["DET"]).values[0] + ". "
            Des += "<b>Images author: </b>" + (taxrow["IMGAUT"]).values[0] + ". " 
            Des += "<b>Taxonomic notes: </b>" + (taxrow["TAXNOT"]).values[0] + ". " if (taxrow["TAXNOT"]).values[0] !="0" else ""
            Des += "For taxon name changes use this code {} in The World Spider Catalog. ".format(taxrow["WSC"].values[0])
            
            return(Des)
        
        def displayImages(taxname):
        # Consumes a string with species name and uses free variable dataframe (df) to get list of photos for given species,
        # Returns string, formatted as html to display the images in the html template
            def determineSex(s):
            # Retrieve the full text of the specimen's sex
                if s == "f":
                    fullSex = "Female specimens:"
                elif s == "m":
                    fullSex = "Male specimens:"
                elif s.lower() == "j":
                    fullSex = "Juvenile specimens"
                else:
                    fullSex = "Sex undetermined"
                return (fullSex)
            def thereIsSex(s, l_df):
            # Consume string with male or female, search through dataframe and return boolean on presence/absence of at least 1 image with that sex in index 10
                for indx, rows in l_df.iterrows():
                    if rows["IMAGENAME"][10] == s: return True
                return False

            def trimAbsPath(pathString):
            # Consume a string representing full path to an image and turns it into relative path using the folder Images as master folder 
                # We start with the assumption that we're located in the Species folder, then we need to go up two directories, then enter images
                relativePath = '../../Images/' + pathString.split('Images')[1][1:]
                return(relativePath)
            def generateUniqueImg():
                return 'newwindow{}'.format(''.join([str(rn.randint(0,9)) for x in range(4)]))

            def anchorTagBuilder(img_path, img_name, img_structureAndView):
                if os.path.exists(img_path):
                    with open(jn(currPath, "Summary_images_processed.txt"), "a") as summaryFile:
                        summaryFile.write(f"{img_name}\t{taxname}\t{img_structureAndView}\t{trimAbsPath(img_path)}\n")
                    anchorTag = ''
                    newWindowHtml = "window.open('{}', '{}', 'width=500, height=400'); return false;".format(trimAbsPath(img_path), generateUniqueImg())
                    anchorTag += '<a href="{}" onclick=\"{}\" target="_blank">\n<img src="{}" alt="{}"> \n<h4 class="myh4">{}</h4>\n</a>\n'.format(
                                                                                                                            trimAbsPath(img_path), 
                                                                                                                            newWindowHtml,
                                                                                                                            trimAbsPath(img_path).replace("/Images/","/Thumbnails/"),
                                                                                                                            img_name, img_structureAndView)
                    return(anchorTag)
                else:
                    logging.info(f"The image {img_path} doesn't exist. Was it erased?")
                    return ("")
            
            _String = ''
            

            listImages = df[df["SPECIES"] == taxname] # Get a list of all pictures for a given species
            orderShow = ["habd", "habl", "habv", "prs", "epiv", "epid", "epi", "palv", "palp", "pal"]
            blackList = [] #empty list to check out images that have been processed already
            
            #iterate over the images three times, prioritizing females, then males, then juveniles
            for sex in ["f", "m", 'j']:
                if thereIsSex(sex, listImages):
                    fullSex = determineSex(sex)
                    _String += "<h3>{}</h3>\n".format(fullSex)
                else:
                    logging.info(f"No images were found with the sex tag {sex} and species {taxname}. If photovouchers exist their sex couldn't be included. Valid tags are f (female), m (male), j (juvenile), u (unknown)")
                for item in orderShow:
                    for indx, img in listImages.iterrows():
                        if img["IMAGENAME"][10] == sex:
                            if len(item)==4:
                                if img["IMAGENAME"][12:16] == item:
                                    if img["IMAGENAME"] not in blackList:
                                        blackList.append(img["IMAGENAME"])
                                        #html instructions to request file to open in new window. _Strign got really long and it was hard to keep track of the quotes
                                        imageToAdd = anchorTagBuilder(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])
                                        _String += imageToAdd
                                        
                                        logging.info("Adding {} to {}.html".format(img["IMAGENAME"],taxname))
                                
                            else:
                                if img["IMAGENAME"][12:15] == item:
                                    if img["IMAGENAME"] not in blackList:
                                        blackList.append(img["IMAGENAME"])
                                        # _String += '<a href="{}" target="blank">\n<img src="{}" alt="{}"> \n<h4 class="myh4">{}</h4>\n</a>\n'.format(trimAbsPath(img["HR_OLD_ADDS"]), trimAbsPath(img["HR_OLD_ADDS"]).replace("/Images/","/Thumbnails/"), img["IMAGENAME"], img["LEGOR"])
                                        _String += anchorTagBuilder(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])
                                        logging.info("Adding {} to {}.html".format(img["IMAGENAME"],taxname))
                # Once the main designation of the images in the html of the species have been set up, we can place anything else (i.e., legs, spinnerets, etc.)
                for indx, img in listImages.iterrows():
                    if img["IMAGENAME"] not in blackList and img["IMAGENAME"][10] == sex:
                        blackList.append(img["IMAGENAME"])
                        _String += anchorTagBuilder(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])
                        # _String += '<a href="{}" target="blank">\n<img src="{}" alt="{}"> \n<h4 class="myh4">{}</h4>\n</a>\n'.format(trimAbsPath(img["HR_OLD_ADDS"]), trimAbsPath(img["HR_OLD_ADDS"]).replace("/Images/","/Thumbnails/"), img["IMAGENAME"], img["LEGOR"])                                                                                                                            img["IMAGENAME"], img["LEGOR"])
                        logging.info("Adding {} to {}.html".format(img["IMAGENAME"],taxname))

            return(_String)

            



        # Open the newly created html into python to change the tags
        with open(pathToPopulate, "r") as file_read:
            file_read = file_read.read()
        
        if not isSpecies:
            configTags = ["[csspath]","[TaxonName]","[TaxonSearch]","[PopList]"]
            for indx, tag in enumerate(configTags):
                if indx == 0: #The csspath tag
                    if pathToPopulate == inventoryHomeName:
                        file_read = file_read.replace(tag, "./html_templates/styles.css")
                    else:
                        file_read = file_read.replace(tag, "../../html_templates/styles.css")
                elif indx == 1: #The Taxon name tag
                    file_read = file_read.replace(tag, taxonName)
                elif indx ==2: #The Search title in the body
                    file_read = file_read.replace(tag, "{} search".format(currentTaxLevel))
                else: #The list of child taxonomic nodes
                    # Get a unique list of that taxonomic level in the df
                    if 'fams_menu.html' in pathToPopulate:
                    # If the word index is contained in the file to populate, it means is the home html
                        file_read = file_read.replace(tag, getChildTaxonList(currentTaxLevel, tax_df, True))
                    else:
                        file_read = file_read.replace(tag, getChildTaxonList(currentTaxLevel, tax_df))
        else:
            configTags = ["[csspath]","[speciesName]", "[backHome]", "[speciesDescription]","[speciesImages]"]
            for indx, tag in enumerate(configTags):
                if indx == 0: #The csspath tag
                    file_read = file_read.replace(tag, "../../html_templates/styles.css" )
                elif indx == 1: #The Taxon name tag
                    if len(taxonName) > 1: #taxon name was passed as a tuple. If there's a second value, it means there's autorship information
                        file_read = file_read.replace(tag, "<em>{}</em> {}".format(taxonName[0], taxonName[1]))
                    else: #otherwise, there's probably a number representing morphospecies that shouldn't be in italics
                        file_read = file_read.replace(tag, "<em>{}</em> {}".format(taxonName[0].split(' ')[0], taxonName[0].split(' ')[1]))
                elif indx ==2: #Back Home link
                    file_read = file_read.replace(tag, '<div class="regreso"><a target= "_blank" href="..\..\index.html"><font color="blue" size="3"> Back to inventory home</font></a></div>'.format(chosenNameInv, "Inventory website"))
                elif indx ==3: #The Search title in the body
                    file_read = file_read.replace(tag, fillDescription(taxonName[0]))
                else: #The list of child taxonomic nodes
                    # Get a unique list of that taxonomic level in the df
                    file_read = file_read.replace(tag, displayImages(taxonName[0]))

        with open(pathToPopulate, "w", encoding='utf-8') as file_write:
            file_write.write(file_read)    

    def recursion(taxRank, r_df):
    # Iterate over the dataframe, extracting information on the children nodes
    # of each search, creating an html webpage for each
        thisTaxonRank = taxonomic_Ranks[taxRank]
        childrenTaxa = r_df[thisTaxonRank].unique()
        logging.info("Creating menu html file: {}".format(thisTaxonRank))
        if thisTaxonRank != "SPECIES":
            for item in childrenTaxa:
                targetHtml = jn(menusPath, '{}.html'.format(item))
                copyfile(TaxRankTemplate, targetHtml)
                subr_df = r_df[r_df[thisTaxonRank] == item]
                editHTML(targetHtml, False, item, taxonomic_Ranks[taxRank+1], subr_df)
                recursion(taxRank+1, subr_df)
        else: #It must be a list of the species images
            for species in childrenTaxa:                
                targetHtml = jn(speciesHtmlPath, '{}.html'.format(species))
                isSpecies = True

                #pass species+author when possible using a list
                authorThisSpecies = r_df[r_df[thisTaxonRank] == species]["SPAUTH"].values[0]
                if authorThisSpecies != "0":
                    speciesAuth = [species, authorThisSpecies]
                else:
                    speciesAuth = [species]
                copyfile(speciesTemplate, targetHtml)
                editHTML(targetHtml, isSpecies, speciesAuth, thisTaxonRank, r_df)
              

    # what is the highest taxonomic rank in the Inventory? Compare columns in df with the taxonomic ranks
    columnsIn_df = [x.upper() for x in df.columns]
    indxHighRank = evaluateHighestRank(columnsIn_df)

            
    # First create the main inventory page
    chosenNameInv = "fams_menu"
    inventoryHomeName = jn(currPath, '{}.html'.format(chosenNameInv))
    copyfile(TaxRankTemplate, inventoryHomeName)
    editHTML(inventoryHomeName, False, "Family search:", taxonomic_Ranks[indxHighRank], df)


    # Create a new txt log file and delete the previous one if exists
    logFile = jn(currPath, "Summary_images_processed.txt")
    os.remove(logFile) if os.path.exists(logFile) else None
    open(logFile, "w").close()
    # Then, create htmls recursively starting at the highest taxonomic rank
    recursion(indxHighRank, df)
        

            
# populateHtmls (test_df, rootTemplates, masterHtmlPath)

    
