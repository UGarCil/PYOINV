# PYOINV v2.0
Based on BIOINV 2.2 (Alvarez-Padilla et. al., 2020) to automate the production of standardized faunistic inventories on the web.

Major changes in the pipeline's structure uses the image folders to find the relationship between image's full path and their species identity.
The program uses two excel files to build a master table (named Esquema):
  - SPPDATA_EX.xlsx: contains the taxonomic information
  - structureNomenclature.xlsx: contains the nomenclature used to standardize views

Because levels of taxonomic classification above genera are not needed in the images folders, the user can simply organize folders at the genus level.

Run the script using main.py. A recent version of python is required (3.0 and above) and the module pandas to be installed. Anaconda is a good way to start.

main.py, like .bat from BIOINV uses information from three sources:

