#!usr/bin/env/python
# File called by CloneFolderTree.py. A suite of utilities for html implementation

import os
from os.path import join as jn
from shutil import copyfile
import pandas as pd

# path to the html and css templates
templatesPath = jn(os.getcwd(),'html_templates')

# Get the excel file contained in the master folder and turn it into a df
excelPath = [x for x in os.listdir(os.getcwd()) if "SPPDATA" in x][0]
dfSPP = pd.read_excel(excelPath)
dfSPP = dfSPP.fillna('')
dfSPP = dfSPP.astype(str)


def editHTML (pathToPopulate, cssPath, isSpecies = False):
    # Consume a subdataframe with given species and return a string with its
    # description
    def createDescription(species):
        Des = ''
        Des += "<b>Species Code: </b>" + (species["MSP_CODE"].values[0]) + ". "
        Des += "<b>Locality: </b>" + (species["LOCALITY"]).values[0] + ". "
        Des += "<b>Species ID: </b>" + (species["ID AUTHOR"]).values[0] + ". "
        Des += "<b>Specimens: Female, </b>" + (species["FEMNUM"]).values[0] + ", Male " + (species["MALNUM"].values[0]) + ". "
        Des += "<b>Species ID: </b>" + (species["SPPIMAUT"]).values[0] + ". "
        Des += "For nomenclatural changes on this taxon ID reffer to its Unique Record Number in The World Spider Catalog {}.".format(species["WSP_NUM"].values[0])
        
        return(Des)

    # Consume a dataframe and name of species, then find its full name with authorship
    def findName(df, spp_name):
        subdf = df[df["SPECIES"] == spp_name]
        author_sp = subdf["SP_AUTHOR"].values[0]
        # If author cell is longer than at leats one character, it means there's information in it
        if len(author_sp) > 1:
            return("<em>{}</em> {}".format(spp_name, author_sp))
        else:
            return("<em>{}</em>".format(spp_name))

    # Consume a dataframe and the name of a taxon, then retrieves a string with its taxonomic level
    def findHighTax(df, taxName):
        taxongroup_name = ''
        df_cols = [col for col in df.columns]
        for col in df_cols:
            # If the query matches at least one element in this column, we return its taxonomic rank
            if len(df[df[col] == taxName]) != 0:
                return (col.title())
            if col == "SPECIES":
                for indx, rows in df.iterrows():
                    # if the word on the left of a species name matches the query, then it's a genus
                    if rows[col].split(' ')[0] == taxName:
                        return ("Genus")
        return("Undetermined taxonomic rank")

    def taxonPopList(path):
        getLowerRanks = [p for p in os.listdir(path) if not p.endswith('.html')]
        popList = ''
        for lowertaxon in getLowerRanks:
            popList += '<li><a href="{}">{}</a></li>'.format(jn(pathToPopulate,lowertaxon, "{}.html".format(lowertaxon)),lowertaxon)
            popList += '\n'
        return(popList)
        



    # Select and assign a template to edit base on taxon type (species or otherwise)
    if isSpecies:
        targetHtml = jn(pathToPopulate,'{}.html'.format(pathToPopulate.split('\\')[-1]))
        copyfile(jn(templatesPath,'speciestemplate.html'),targetHtml)
    else:
        targetHtml = jn(pathToPopulate,'{}.html'.format(pathToPopulate.split('\\')[-1]))
        copyfile(jn(templatesPath,'template.html'),targetHtml)

    # ********Getting information for editing species html**********

    if (isSpecies):
        # Get species name from the path
        species_name = pathToPopulate.rsplit("\\",2)[1:]
        species_name = " ".join(species_name)
        complete_spName = findName(dfSPP, species_name)
        
        # Get description from excel table
        speciesDescription = dfSPP[dfSPP["SPECIES"] == species_name]
        descriptionString = createDescription(speciesDescription)

        # Get the images from .txt file
        txtFile = [x for x in os.listdir(pathToPopulate) if x.endswith(".txt")][0]
        # Open the txt file with the absolute path to the species' images
        with open(jn(pathToPopulate, txtFile), 'r') as imagesForSP:
            # Extract the paths of male and female images based on the 11th character
            imagesForSP = imagesForSP.readlines()
            imagesForSP = [img.replace('\n','') for img in imagesForSP]
            femaleImages = [f for f in imagesForSP if f.split('\\')[-1][10] == "f"]
            maleImages = [m for m in imagesForSP if m.split('\\')[-1][10] == "m"]
            textimgSet = ["Female: ", "Male: "]
            totalImages = [femaleImages, maleImages]
            speciesImages = ''
            for indxSet, imgSet in enumerate(totalImages):
                if len(imgSet) !=0:
                    speciesImages += "<br><b>{}</b> <br>".format(textimgSet[indxSet])
                    for image in imgSet:
                        speciesImages += '<img src="{}" alt="{}"> \n'.format(image, image.split('\\')[-1])
        # *******Creating the html file********************************
        # 
        newHTML = ''
        with open(targetHtml,"r") as htmlToEdit:
            htmlToEdit = htmlToEdit.read()

            # configuration tags are identifiers in template.html
            configTags = ['[speciesName]','[speciesDescription]','[speciesImages]']
            for tag in configTags:
                if tag == configTags[0]:
                    htmlToEdit = htmlToEdit.replace(tag, complete_spName)
                if tag == configTags[1]:
                    htmlToEdit = htmlToEdit.replace(tag, descriptionString)
                if tag == configTags[2]:
                    htmlToEdit = htmlToEdit.replace(tag, speciesImages)
            # Also edit the css path
            htmlToEdit = htmlToEdit.replace("[csspath]", cssPath)
            newHTML = htmlToEdit
        with open(targetHtml,'w', encoding='utf-8') as writeHtmlFile:
            writeHtmlFile.write(newHTML)
        # print(newHTML)
    else:
        taxonHighName = pathToPopulate.split('\\')[-1] #the taxon's name
        taxonSearch = findHighTax(dfSPP, taxonHighName) #the taxon's rank
        # The actual html will show the taxon level that is immediately lower to that which we found,
        # so it's necessary to change the returned value with reference to a list
        taxonomic_ranks = ["Phyllum", "Class", "Order", "Family", "Genus", "Morphospecies"]
        for indx, vals in enumerate(taxonomic_ranks):
            try:
                if (vals == taxonSearch):
                    taxonSearch = taxonomic_ranks[indx+1] + " of " + taxonHighName
                    break
                            
            except:
                print("It seems the taxon {} is not in your excel spreadsheet.".format(taxonHighName))
                break
        
        # If the name of the taxon is just the root, then look into chlidren folders to see what they are.
        # The higher rank will be assigned in this case
        if taxonHighName == "HTML_SpeciesTree":
            newPath = jn(pathToPopulate)
            getChildFolder = [x for x in os.listdir(newPath) if not x.endswith(".html")][0]
            taxonSearch = findHighTax(dfSPP, getChildFolder) + " search:"
        popList = taxonPopList(pathToPopulate) # Get a list of taxa that are nested within this level

        #********Edit the template.html***************************************
        newHTMLHigh = ''
        with open(targetHtml, "r", encoding='utf-8') as editHtmlTaxon:
            editHtmlTaxon = editHtmlTaxon.read()
            configTags = ["[TaxonName]", "[TaxonSearch]", "[PopList]"]
            for tag in configTags:
                if tag == configTags[0]:
                    editHtmlTaxon = editHtmlTaxon.replace(tag,taxonHighName)
                if tag == configTags[1]:
                    taxonSearch = taxonSearch.replace("Genus", "Genera")
                    editHtmlTaxon = editHtmlTaxon.replace(tag,taxonSearch)
                if tag == configTags[2]:
                    editHtmlTaxon = editHtmlTaxon.replace(tag,popList)
            # Also edit the css path
            editHtmlTaxon = editHtmlTaxon.replace("[csspath]", cssPath)
            newHTMLHigh = editHtmlTaxon
        with open(targetHtml, 'w', encoding='utf-8') as writeHtmlTaxon:
            writeHtmlTaxon.write(newHTMLHigh)

# editHTML (r"D:\Garcilazo\Javascript_NodeJS\FAPOWebpage\02_Editing_Dynamic\PYTHON_Version\HTML_SpeciesTree")