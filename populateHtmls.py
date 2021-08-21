#!usr/bin/env/python3
# Iterate over the taxonomic ranks, represented as columns from a dataframe, to create html files

# The table that the user gives as SPPDATA should include all of the taxonomic levels that follow
# the highest rank found

import os
from os.path import join as jn
import pandas as pd
from shutil import copyfile
import logging

# currPath = os.getcwd()
# test_df = pd.read_excel("Esquema.xlsx")
# test_df = test_df.fillna('')
# test_df = test_df.astype(str)

# rootTemplates = jn(currPath, "html_templates")
# masterHtmlPath = jn(currPath, "HTML_files")

def populateHtmls(df, rootHtmlTemplates, masterHtmlPath):
# Create a series of html files for each taxonomic level to the level of species

    # Path for html/css templates
    speciesTemplate = jn(rootHtmlTemplates, "speciesTemplate.html")
    TaxRankTemplate = jn(rootHtmlTemplates, "template.html")
    cssTemplate = jn(rootHtmlTemplates, "styles.css")

    # Taxonomic rank names below match column names from Esquema
    taxonomic_Ranks = ["CLASS","ORDER", "FAMILY", "GENUS", "SPECIES"]
    _String = ''

    def evaluateHighestRank(columns_df):
        #identify the highest rank available in a df's columns
        for indx, rank in enumerate(taxonomic_Ranks):
            if rank in columns_df: return (indx)

    def editHTML(pathToPopulate, isSpecies, taxonName, currentTaxLevel, tax_df):
    # Edit the html to the parameters needed for that particular taxonomic level
        def getChildTaxonList(columnName, tax_df):
        # redact a string in html format that summarizes the families included in the dataframe
            _String_gctl = ''
            # Get  list with unique records for the taxonomic level of interest
            uniqueRecords = tax_df[columnName].unique()
            # And add each element into the list
            for name in uniqueRecords:
                _String_gctl += '<li><a href="{}">{}</a></li>\n'.format("{}.html".format(name),name)
            return(_String_gctl)

        def fillDescription (taxname):
        # Consumes a string with the name of a species and uses df (free var.) and return species description
            # Because names in Esquema are repeated based on number of images for each voucher, we take one of such images,
            # doesn't matter which one, to populate the empty string
            taxrow = df[df["SPECIES"] == taxname].head(1)
            
            
            
            Des = ''
            Des += "<b>Species Code: </b>" + (taxrow["VOUCO2"].values[0]) + ". "
            Des += "<b>Locality: </b>" + (taxrow["LOCDATA"]).values[0] + ". "
            Des += "<b>Species ID: </b>" + (taxrow["DET"]).values[0] + ". "
            Des += "<b>Specimens:</b> Female, " + (taxrow["FEMSPE"]).values[0] + ", Male " + (taxrow["MALSPE"].values[0]) + ". "
            Des += "<b>Images author: </b>" + (taxrow["IMGAUT"]).values[0] + ". "
            Des += "For nomenclatural changes on this taxon ID reffer to its Unique Record Number in The World Spider Catalog {}.".format(taxrow["WSC"].values[0])
            
            return(Des)
        
        def displayImages(taxname):
        # Consumes a string with species name and uses free variable dataframe (df) to get list of photos for given species,
        # Returns string, formatted as html to display the images in the html template
            def determineSex(s):
            # Retrieve the full text of the specimen's sex
                if s == "f":
                    fullSex = "Female:"
                elif s == "m":
                    fullSex = "Male"
                else:
                    fullSex = "Juvenile/undetermined"
                return (fullSex)
            def thereIsSex(s, l_df):
            # Consume string with male or female, search through dataframe and return boolean on presence/absence of at least 1 image with that sex in index 10
                for indx, rows in l_df.iterrows():
                    if rows["IMAGENAME"][10] == s: return True
                return False



            _String = ''
            # Get a list of all pictures for a given species
            listImages = df[df["SPECIES"] == taxname]
            orderShow = ["habd", "habl", "habv", "prs", "epiv", "epid", "epi", "palv", "palp", "pal"]
            blackList = []
            for sex in ["f", "m", 'j']:
                if thereIsSex(sex, listImages):
                    fullSex = determineSex(sex)
                    _String += "<h2>{}</h2>\n".format(fullSex)
                for item in orderShow:
                    for indx, img in listImages.iterrows():
                        if img["IMAGENAME"][10] == sex:
                            if len(item)==4:
                                if img["IMAGENAME"][12:16] == item:
                                    if img["IMAGENAME"] not in blackList:
                                        print(img["IMAGENAME"])
                                        blackList.append(img["IMAGENAME"])
                                        _String += '<img src="{}" alt="{}"> \n<h3 class="myh3">{}</h3>\n'.format(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])

                                
                            else:
                                if img["IMAGENAME"][12:15] == item:
                                    if img["IMAGENAME"] not in blackList:
                                        blackList.append(img["IMAGENAME"])
                                        _String += '<img src="{}" alt="{}"> \n<h3 class="myh3">{}</h3>\n'.format(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])
                for indx, img in listImages.iterrows():
                    if img["IMAGENAME"] not in blackList and img["IMAGENAME"][10] == sex:
                        blackList.append(img["IMAGENAME"])
                        _String += '<img src="{}" alt="{}"> \n<h3 class="myh3">{}</h3>\n'.format(img["HR_OLD_ADDS"], img["IMAGENAME"], img["LEGOR"])

            return(_String)

            



        # Open the newly created html into python to change the tags
        with open(pathToPopulate, "r") as file_read:
            file_read = file_read.read()
        
        if not isSpecies:
            configTags = ["[csspath]","[TaxonName]","[TaxonSearch]","[PopList]"]
            for indx, tag in enumerate(configTags):
                if indx == 0: #The csspath tag
                    file_read = file_read.replace(tag, cssTemplate)
                elif indx == 1: #The Taxon name tag
                    file_read = file_read.replace(tag, taxonName)
                elif indx ==2: #The Search title in the body
                    file_read = file_read.replace(tag, "{} search".format(currentTaxLevel))
                else: #The list of child taxonomic nodes
                    # Get a unique list of that taxonomic level in the df
                    file_read = file_read.replace(tag, getChildTaxonList(currentTaxLevel, tax_df))
        else:
            configTags = ["[csspath]","[speciesName]", "[backHome]", "[speciesDescription]","[speciesImages]"]
            for indx, tag in enumerate(configTags):
                if indx == 0: #The csspath tag
                    file_read = file_read.replace(tag, cssTemplate)
                elif indx == 1: #The Taxon name tag
                    file_read = file_read.replace(tag, "<em>{}</em>".format(taxonName))
                elif indx ==2: #Back Home link
                    file_read = file_read.replace(tag, '<h2><a href="{}.html">{}</a></h2>\n'.format(chosenNameInv, "Inventory website"))
                elif indx ==3: #The Search title in the body
                    file_read = file_read.replace(tag, fillDescription(taxonName))
                else: #The list of child taxonomic nodes
                    # Get a unique list of that taxonomic level in the df
                    file_read = file_read.replace(tag, displayImages(taxonName))

        with open(pathToPopulate, "w", encoding='utf-8') as file_write:
            file_write.write(file_read)    

    def recursion(taxRank, r_df):
    # Iterate over the dataframe, extracting information on the children nodes
    # of each search, creating an html webpage for each
        # Get the element at the current taxonomic index
        thisTaxonRank = taxonomic_Ranks[taxRank]
        childrenTaxa = r_df[thisTaxonRank].unique()
        if thisTaxonRank != "SPECIES":
            for item in childrenTaxa:
                targetHtml = targetHtml = jn(masterHtmlPath, '{}.html'.format(item))
                copyfile(TaxRankTemplate, targetHtml)
                subr_df = r_df[r_df[thisTaxonRank] == item]
                editHTML(targetHtml, False, item, taxonomic_Ranks[taxRank+1], subr_df)
                recursion(taxRank+1, subr_df)
        else: #It must be a list of the species images
            for species in childrenTaxa:                
                targetHtml = jn(masterHtmlPath, '{}.html'.format(species))
                isSpecies = True
                copyfile(speciesTemplate, targetHtml)
                editHTML(targetHtml, isSpecies, species, thisTaxonRank, r_df)
              

    # what is the highest taxonomic rank in the Inventory? Compare columns in df with the taxonomic ranks
    columnsIn_df = [x.upper() for x in df.columns]
    indxHighRank = evaluateHighestRank(columnsIn_df)

            
    # First create the main inventory page
    chosenNameInv = "HOME-Inventory"
    inventoryHomeName = jn(masterHtmlPath, '{}.html'.format(chosenNameInv))
    copyfile(TaxRankTemplate, inventoryHomeName)
    editHTML(inventoryHomeName, False, chosenNameInv, taxonomic_Ranks[indxHighRank], df)

    # Then, create htmls recursively starting at the highest taxonomic rank
    recursion(indxHighRank, df)
        

            
# populateHtmls (test_df, rootTemplates, masterHtmlPath)

    
