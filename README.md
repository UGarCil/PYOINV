# PYOINV v2.0
Based on BIOINV 2.2 (Alvarez-Padilla et. al., 2020) to automate the production of standardized faunistic inventories on the web.

To run the program you will need to following libraries installed along with a python version 3.0x or above:
- pandas
- PIL (pillow)

Installation:
We strongly recommend using anaconda to run Pyioinv, as the package installing is much simpler. Download anaconda for your OS and add it to the PATH, in the system variables. Once it's installed, you can install pillow and pandas with the following commands:

```
conda install -c anaconda pillow
conda install -c anaconda pandas
```

## We recommend however that you install both programs in one go while creating a new environment:

```
conda create --name Pyoinv pandas pillow
```

Then, to activate your new environment, simply type:

```
conda activate Pyoinv
```

## Clone and run the repository

Go to Code > Download ZIP and extract the folder in your chosen folder

Access the Pyoinv folder from the terminal and edit the SPPDATA_Ex.xlsx with your taxonomic database, and replace the contents of the "Images" folder with the contents in your own directory tree (I recommend you simply erasing the Images folder already in Pyoinv, changing the name of the folder containing your own images to "Images" and then place it in the Pyoinv directory). You might also need to change the contents of the table "structureNomenclature.xlsx" if you have images of structures that are not already in the table.

Once you're done editing your data, run the following command from the terminal (while still in your environment)

```
python main.py
```

If everything is in place the program will finish running and you'll have a new "HTML_files" folder containing your inventory in htmls, and also an index.html file located in the master folder with the home directory.

We included a log file system. Please make sure not to change the names of the excel file's columns, position in the master folder or the file's name. The log file might be useful to retrieve some critical errors that you may encounter. You can find it in the master folder, named as "Log.txt"

## Some major changes in the structure of the pipeline:
Starting September 13th, Pyoinv changed the way the Eschema.xlsx file is created. The program does the following:
1. Create a clone of the tree directory "Images". The new folder is called Thumbnails and contains a low resolution image of each of your species' views. This step was implemented to maximize computational resources when loading the page.

2. Create a "Esquema". A esquema is an excel table that summarizes the relationship between each of your species images and their taxonomic information in your inventory. The program uses two sub tables:
- SPPDATA.xlsx: contains the taxonomic information of each species
- structureNomenclature.xlsx: contains the names of the structures and their views, and needed to translate the extracted acronyms in the species images' names into english.

3. Create htmls: the index.html is created providing a list of the taxa with the highest taxonomic range (usually Family), then it creates an html tree ending in the least inclusive taxon that is species. The species htmls incorporate the images from the thumbnails, with hyperlinks to their original, high res versions.



## Putting my inventory on the web
Transfer all the items inside the master folder into your hosting provider cpanel's File manager (inside your public_html)

##We hope you enjoy Pyoinv! Please let us know if you run into any problems by sending an email to fap at ciencias.unam.mx