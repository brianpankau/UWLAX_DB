# -*- coding: utf-8 -*-

# Author: Brian Pankau
# Class: DS710 Summer 2017
# Assignment: Python 11


# -----------------------------------------------------------------------------------------------------    
# Problem 1(a)
# Create a pandas DataFrame object with the following entries for each review:
# •Product ID
# •Number of people who voted this review helpful
# •Total number of people who rated this review
# •Rating of the product
# •Text of the review

# For the second and third of these, 
# the information will be given in the file as 1/5, 
# which would correspond to 1 vote for helpful out of 5 people who rated the review.


# Description: Read foods.txt input file and creates a table in foods_out.txt
#   that represents the input data as a tab delimited table that will be used
#   to create a data frame df.
#   The intermediate file foods_parsed.txt is generated in order to handle
#   embedded carriage returns within each field with each text block.

# Control Flow:
# convert unknown encoding into ascii => parse_input_fn -> parse_output_fn
# parse input file an replace any embeddeed CR with a space => parse_input_fn -> parse_output_fn
# construct a list of lists from the fields within each text block => process_input_fn -> list_of_lists
# write the table header to the output file => header -> process_output_fn
# process the list_of_lists, extract values from key:value pairs, generate each row of the output table => list_of_lists -> key:value -> value -> process_output_fn
# create dataframe from table in file


# set debug status, 0=OFF, 1=ON
debug = 0

# import libraries
import string
import codecs
import sys
import binascii
import unicodedata
import os
import time
import pandas as pd
import numpy as np
from pandas import Series, DataFrame


# set file names
if (debug) :
    # 100 input text blocks
    parse_input_fn0    = "foods100.txt"
    parse_output_fn0   = "foods100_parsed_0.txt"
    parse_input_fn1    = "foods100_parsed_0.txt"
    parse_output_fn1   = "foods100_parsed.txt"
    process_input_fn   = "foods100_parsed.txt"
    process_output_fn  = "foods100_out.txt"
    process_output_csv  = "foods100.csv"
else :
    # Actual data file for run-for-record
   parse_input_fn0    = "foods.txt"
   parse_output_fn0   = "foods_parsed_0.txt"
   parse_input_fn1    = "foods_parsed_0.txt"
   parse_output_fn1   = "foods_parsed.txt"
   process_input_fn   = "foods_parsed.txt"
   process_output_fn  = "foods_out.txt"
   process_output_csv  = "foods.csv"

    
# set working directory
os.chdir('C:\_DS710\Temp11')


# convert unknown encoding into ascii, remove non-printable characters, multiple spaces
f2 = open(parse_output_fn0, 'w', encoding='utf-8', errors="ignore")
with open(parse_input_fn0, 'r', encoding="utf-8", errors="ignore") as f1:
    for aline in iter(f1.readline, ""):
        # replace all multiple spaces with a single space
        aline_str = aline.replace(chr(9), chr(20))
        aline_str1 = aline_str.replace("  ", chr(20))
        aline_str2 = aline_str1.replace(chr(34), chr(39))
        #strip special characters from salaries
        printable = set(string.printable)
        aline_str3 = '' .join(filter(lambda x: x in string.printable, aline_str2))
        # write the processed line to a file
        f2.write(aline_str3)
f2.close()
f1.close()


# parse input file an replace any embeddeed CR with a space
f_out_parse = open(parse_output_fn1, 'w', encoding='utf-8', errors="surrogateescape")
with open(parse_input_fn1, "r", encoding='utf-8', errors="surrogateescape") as f_in_parse:
    # process each field in the input text block
    for parse_line in f_in_parse :
        # input line is only a CR, issue CR to terminate text block
        if ((len(parse_line) == 1) & (parse_line[0:1] == "\n")):
            f_out_parse.write("\n")
        # input line is a product field of text block
        elif (parse_line[0:8] == "product/") :
            f_out_parse.write("\n")
            f_out_parse.write(parse_line[0:len(parse_line)-1])
        # input line is a review field of text block
        elif (parse_line[0:7] == "review/") :
            f_out_parse.write("\n")
            f_out_parse.write(parse_line[0:len(parse_line)-1])
        # input line represents a continuation of the previous input field
        else :
            f_out_parse.write(parse_line[0:len(parse_line)-1])
f_out_parse.write("\n\n")
f_out_parse.close()

# construct a list of lists from the fields within each text block
list_of_lists = []
with open(process_input_fn, "r", encoding='utf-8', errors="ignore") as f_in:
    # read the blank line at the beginning of the parsed file that was generated
    empty_line = f_in.readline()
    if (debug) :
        print("EMPTY LINE", empty_line)

    linecount = 1
    line_list = []
    for line in f_in:
        if (debug) :
            print("****", linecount, line)

        if (linecount % 9 != 0):
            if (debug) :
                print(linecount, "IF BEFORE", line_list)
            line_list.append(line)
            if (debug) :
                print(linecount, "IF AFTER", line_list)
            linecount = linecount + 1
        else:
            if (debug) :
                print(linecount, "ELSE BEFORE", line_list)

            list_of_lists.append(line_list)

            if (debug) :
                print(linecount, "ELSE AFTER", line_list)

            line_list = []
            linecount = 1

# define search strings
key_0 = "product/productId: "
key_1 = "review/userId: "
key_2 = "review/profileName: "
key_3 = "review/helpfulness: "
key_4 = "review/score: "
key_5 = "review/time: "
key_6 = "review/summary: "
key_7 = "review/text: "

# define labels for output header
label_rowid = "Rowid"
label_0 = "ProductId"
label_1 = "UserId"
label_2 = "Name"
label_3 = "Helpfulness"
label_4 = "Score"
label_5 = "Time"
label_6 = "Summary"
label_7 = "Text"

label_0_len = "ProductId_len"
label_1_len = "UserId_len"
label_2_len = "Name_len"
label_3_len = "Helpfulness_len"
label_4_len = "Score_len"
label_5_len = "Time_len"
label_6_len = "Summary_len"
label_7_len = "Text_len"

head_str = chr(34)
mid_str = chr(34) + chr(9) + chr(34)
tail_str = chr(34) + chr(10)

# open the output file
f_out = open(process_output_fn, 'w', encoding='utf-8', errors="ignore")

# write the table header to the output file
if (debug) :
    header_str = head_str + label_rowid + mid_str + label_0 + mid_str + label_1 + mid_str + label_2 + mid_str + label_3 + mid_str + label_4 + mid_str + label_5 + mid_str + label_6 + mid_str + label_7 + tail_str
else :
    header_str = head_str + label_0 + mid_str + label_1 + mid_str + label_2 + mid_str + label_3 + mid_str + label_4 + mid_str + label_5 + mid_str + label_6 + mid_str + label_7 + tail_str
#    header_str = head_str + \
#        label_rowid + mid_str + \
#        label_0 + mid_str + label_0_len + mid_str + \
#        label_1 + mid_str + label_1_len + mid_str + \
#        label_2 + mid_str + label_2_len + mid_str + \
#        label_3 + mid_str + label_3_len + mid_str + \
#        label_4 + mid_str + label_4_len + mid_str + \
#        label_5 + mid_str + label_5_len + mid_str + \
#        label_6 + mid_str + label_6_len + mid_str + \
#        label_7 + mid_str + label_7_len + tail_str

# ouput the table header
f_out.write(header_str)

# process the list_of_lists, extract values from key:value pairs, generate each row of the output table
rowid = 1
for a_list in list_of_lists :
    if (debug) :
        f_out.write(str(len(list_of_lists)))
        f_out.write("\n")

    if (debug) :
        f_out.write(str(len(a_list)))
        f_out.write("\n")

    # extract the value from the key : value pair and remove the trailing CR
    value_0 = a_list[0][len(key_0) : len(a_list[0]) - 1]
    value_1 = a_list[1][len(key_1) : len(a_list[1]) - 1]
    value_2 = a_list[2][len(key_2) : len(a_list[2]) - 1]
    value_3 = a_list[3][len(key_3) : len(a_list[3]) - 1]
    value_4 = a_list[4][len(key_4) : len(a_list[4]) - 1]
    value_5 = a_list[5][len(key_5) : len(a_list[5]) - 1]
    value_6 = a_list[6][len(key_6) : len(a_list[6]) - 1]
    value_7 = a_list[7][len(key_7) : len(a_list[7]) - 1]

    if (debug) :
        output_str = head_str + \
            str(rowid) + mid_str + \
            value_0 + mid_str + \
            value_1 + mid_str + \
            value_2 + mid_str + \
            value_3 + mid_str + \
            value_4 + mid_str + \
            value_5 + mid_str + \
            value_6 + mid_str + \
            value_7 + tail_str
    else :
        output_str = head_str + value_0 + mid_str + value_1 + mid_str + \
            value_2 + mid_str + value_3 + mid_str + value_4 + mid_str + \
            value_5 + mid_str + value_6 + mid_str + value_7 + tail_str
#        output_str = head_str + \
#            str(rowid) + mid_str + \
#            value_0 + mid_str + str(len(value_0)) + mid_str + \
#            value_1 + mid_str + str(len(value_1)) + mid_str + \
#            value_2 + mid_str + str(len(value_2)) + mid_str + \
#            value_3 + mid_str + str(len(value_3)) + mid_str + \
#            value_4 + mid_str + str(len(value_4)) + mid_str + \
#            value_5 + mid_str + str(len(value_5)) + mid_str + \
#            value_6 + mid_str + str(len(value_6)) + mid_str + \
#            value_7 + mid_str + str(len(value_7)) + tail_str

    # write the row to the table
    f_out.write(output_str)
    rowid = rowid + 1

    # close the file containing the table
f_out.close()

# create dataframe from table in file for further proocessing
if (debug == 1) :
    # create a temp df to remove quotechars & set column names
    df = pd.read_table(process_output_fn, sep='\t', encoding='utf-8', quotechar='"', lineterminator="\n", na_values='NaN', \
        names=['ProductId', 'UserId', 'Name', 'Helpfullness', 'Score', 'Time', 'Summary', 'Text','Help_tuple'],            \
        dtype={'ProductId':str,'UserId':str,'Name':str,'Helpfullness':str,'Score':str,'Time':str,'Summary':str,'Text':str,'Help_tuple':str})
    # debug df
    print(df_tmp)
    print(df_tmp.describe())
else:
    # create a temp df to remove quotechars & set column names
    df = pd.read_table(process_output_fn, sep='\t', encoding='utf-8', quotechar='"', lineterminator="\n", na_values='NaN', header=0, \
        names=['ProductId', 'UserId', 'Name', 'Helpfullness', 'Score', 'Time', 'Summary', 'Text'],            \
        dtype={'ProductId':str,'UserId':str,'Name':str,'Helpfullness':str,'Score':str,'Time':str,'Summary':str,'Text':str})

# convert Helpfullness ratio into integers: calculate number of people who voted helpfull & Total number of people who voted
# - convert ratio string into a 3-part tuple string
# - extract the nominator and denominator & convert to an integer
# - insert converted strings into 2 new columns in dataframe
z = lambda a: a.partition("/")
h_series = Series(df.Helpfullness)
h_tuple = h_series.apply(z)
y = lambda b: int(b[0])
x = lambda c: int(c[2])
h_num_int = Series(h_tuple.apply(y))
h_denum_int = Series(h_tuple.apply(x))
df['Voted_helpful'] = h_num_int
df['Voted_total'] = h_denum_int

# generate results
print(df.columns)
print(df.dtypes)
print(df.ProductId.count())
print(df.describe())


# -----------------------------------------------------------------------------------------------------    
# Problem 1b    
# Add columns to your DataFrame for 
# the length of a review, 
# the number of exclamation points in a review, and 
# the fraction of people who rated a review helpful. 
#
# You should calculate the fraction who rated a review helpful using the two columns you made in 1a, and 
# a ratio of 1 helpful rating out of 5 total ratings should be entered as 0.2, not the string 1/5. 
# If no people voted on whether a problem was helpful, the corresponding entry in your percentage helpful column should be NaN.

# the length of a review Text string
w = lambda d: len(d)
text_series = Series(df.Text)
review_len = text_series.apply(w)
df['Review_length'] = review_len

# count the number of exclamation points in a review
v = lambda e: e.count("!")
exclamation_cnt = text_series.apply(v)
df['Exclamation_count'] = exclamation_cnt

# the fraction of people who rated a review helpful
fraction_series = np.where(df.Voted_total == 0, np.nan, df.Voted_helpful / df.Voted_total)
df['Percentage_helpful'] = fraction_series


# -----------------------------------------------------------------------------------------------------    
# Problem 1(c). Summary statistics.
# How many reviews are in the data set? 
# What is the average length of a review (in characters)? 
# What is the average rating? 
# What is the greatest number of exclamation marks used in a single review? 
# Use the pandas package to answer these questions, then summarize your results in a markdown cell.

print("How many reviews are in the data set? =>", df.shape[0])
print("What is the average length of a review (in characters)? =>", df.Review_length.mean())
print("What is the average rating?  =>", df.Voted_helpful.mean())
print("What is the greatest number of exclamation marks used in a single review? =>", df.Exclamation_count.max())


# -----------------------------------------------------------------------------------------------------    
#Problem 1(d). Export.
# Save your DataFrame as a .csv file suitable for future analysis in R. 
# Your .csv file should not include the review text column, 
# as the presence of commas and quotation marks will make reading the file difficult. 
# You should also convert entries from NaN to the empty string before saving.
df.to_csv(process_output_csv, sep=',', encoding='utf-8', quotechar='"', na_rep='', index=False, index_label=False, \
    columns=['ProductId', 'UserId', 'Name', 'Helpfullness', 'Score', 'Time', \
    'Summary', 'Voted_helpful', 'Voted_total', 'Review_length', \
    'Exclamation_count', 'Percentage_helpful'],
    header=['ProductId', 'UserId', 'Name', 'Helpfullness', 'Score', 'Time', \
    'Summary', 'Voted_helpful', 'Voted_total', 'Review_length', \
    'Exclamation_count', 'Percentage_helpful'])

