#!usr/bin/env/python
# *****Called by main.py*****
# This script consumes a pandas dataframe and creates a tree of nested folders
# following the classification indicated by the order in the columns of the
# dataframe, where the leftmost index value [0] represents the higher level
# of classification

import pandas as pd
import os
from os.path import join as jn
from html_utils import editHTML

def nestingFolders(df, original_path, cssPath):
    # This will create the folders
    def makeFolder(path, name):
        os.mkdir(jn(path,name))

    # This will create a unique list of values for the column number col_num
    def getUniqueValues(col_num, df):
        # Extract uniqeu values and get rid of empty values
        listUniqueValues = df[col_num].unique()
        listUniqueValues = [x for x in listUniqueValues if x != '']
        return(listUniqueValues)

    


    # Implement the recursion. rec_num represents the current column
    # maximum represents the maximum value in the index (i.e. max. num. cols)
    # df = dataframe
    # current_path will represent an accumulator and a pivot to make a new folder
    def recursion(df, rec_num, maximum, current_path):
        # This local function is within the scope of the main recursion function. It exports a .txt file with a list
        # showing the location of the images following its absolute path
        def XportImageList(xportPath, xportMaxNum, xportNew_df):
            with open(jn(xportPath,'{}.txt'.format(xportPath.split("\\", -2)[-1])), "w") as img_file:
                temp_string = ''
                for indx, vals in xportNew_df.iterrows():
                    temp_string += "{}\n".format(vals[xportMaxNum])
                img_file.write(temp_string)


        new_df = df
        origPath = current_path
        for i in getUniqueValues(rec_num, new_df):
            if(rec_num < maximum):
                makeFolder(current_path, i)
                editHTML(current_path, cssPath)
                current_path += '\\' + i
                new_df = df[df[rec_num] == i]
                recursion(new_df, rec_num+1, maximum, current_path)
            # If the column we're at is the maximum, it means this is the image names
            elif (rec_num == maximum): 
                XportImageList(current_path, maximum, new_df)
                editHTML(current_path, cssPath, True)
                

            else:
                return None
            current_path = origPath
                


    # Call the recursion to produce a tree of folders with the same structure as the master fodler containing the images
    # We don't consider the last column because those are the images names
    recursion(df, 0, len(df.columns)-1, original_path)
