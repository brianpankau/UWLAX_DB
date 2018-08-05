# -*- coding: utf-8 -*-

# Author: Brian Pankau
# Class: DS710 Summer 2017
# Assignment: Python 7


# import libraries
import string
import os
import sys
import binascii
import unicodedata
import pandas as pd
import numpy as np
from pandas import Series, DataFrame


# set working directory
os.chdir('C:/_DS710/Temp07')

# set debug options (1=TRUE)
debug = 1

# Problem 1a: Word Length
# ---------------------------------------------------------------------
# Write a function called word_length_list() which takes a string and 
# returns a list with the length of each word in the string. 
# For each word, count the number of English, alphanumeric characters. 
# Words are defined as text separated by spaces. 
# Your function should ignore punctuation. 
# For example, word_length_list("Haven't you eaten 8 oranges today?") 
# should return [6,3,5,1,7,5]. 
# Call or create other functions as necessary to organize your work.


# define a function to remove the standard punctuation marks from a string
# input:  a string with punctuation marks
# output: a string with punctuation marks removed
def rmPunctuation(s):
        rmPunctuation_table = str.maketrans("", "", string.punctuation)
    return s.translate(rmPunctuation_table)

    
# define a function to count the number of characters per word in a word list
# note:   string oriented, not list oriented
# input:  a string of character_words delimited by a whitespace
# output: a list of integers, each integer represents the number of characters in a word
def word_length_list(s):
    # rm punctuation characters
    s1 = rmPunctuation(s)
    
    # convert string into a list by splitting on a whitespace character
    list_str = s1.split(" ")
    
    if (debug):
        print("input string converted into a list = ", list_str)
        print("")
    
    # create a list of lengths of the words in the list
    char_count_word_list = []
    for l in list_str:
        char_count_word_list.append(len(l))
        
    return char_count_word_list


# test Problem 1a functions
inputStr = "Haven't you eaten 8 oranges today?"
if (debug):
    print("input string = ", inputStr)
    print("")
    print("input string w/o punctuation = ", rmPunctuation(inputStr))
    print("")
    print("character count per word in input string w/o punctuation = ", word_length_list(rmPunctuation(inputStr)))
    print("")


# Problem 1b: A Mourner
# ---------------------------------------------------------------------
# Use your function word_length_list() from 1(a) to find the length 
# of each word in "A Mourner". (Note that your output should end 
# in . . ., 3, 1, 7].)


# define a function to remove carriage returns from a string
# input:  a string with CRs
# output: a sring without CRs
def rmCarriageReturns(s):
    split_list = s.splitlines()
    # if CR were present then reverse the list and exclude ''
    if (len(split_list) > 1):
        split_list.reverse()
        s1 = split_list.pop()
        for e in split_list:
            if (e != ''):
                s1 = s1 + " " + e
        return s1
    else:
        s1 = split_list[0]
        return s1

# test Problem 1b functions
inputStr = "The general Sympathy and Concern for the Murder of the \
Lad by the base and infamous Richardson on the 22d Instant, \
will be sufficient Reason for your Notifying the Public that he will \
be buried from his Father’s House in Frogg Lane, opposite Liberty-Tree, \
on Monday next, when all the Friends of Liberty may have an Opportunity \
of paying their last Respects to the Remains of this little Hero and \
first Martyr to the noble Cause--Whose manly Spirit (after this Accident \
happened) appear’d in his discreet Answers to his Doctor, his Thanks to \
the Clergymen who prayed with him, and Parents, and while he underwent \
the greatest Distress of bodily Pain; and with which he met the King of \
Terrors. These Things, together with the several heroic Pieces found in \
his Pocket, particularly Wolfe’s Summit of human Glory, gives Reason to \
think he had a martial Genius, and would have made a clever Man.\
\r\n\
A Mourner."


# Problem 1c: Pride and Prejudice
# ---------------------------------------------------------------------
# reads input file character by character
# input:  a file name
# output: a text string that contains the contents of the input file
# import libraries

# import libraries
import string
import os
import sys
import binascii
import unicodedata
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

# set working directory
os.chdir('C:/_DS710/Temp07')

def rmPunctuationStr(s):
    rmPunctuation_table = str.maketrans("", "", string.punctuation)
    return s.translate(rmPunctuation_table)


def read_input(inputFN):
    # exclude appostrophe (right, left, regular), dash
    exclusionChars = {chr(8220), chr(8221), chr(34), chr(95)}
    tx_str = ""
    with open(inputFN, 'r') as f_in:
        for line in f_in:
            if (len(line) > 1):
                for ch in line:
                    # exclude quotation marks
                    if (ch in exclusionChars):
                        pass
                    # if character is a dash (or hyphen-like), replace with a space
                    elif (ch == chr(45)):
                        tx_str = tx_str + chr(32)
                    else:
                        tx_str = tx_str + ch
        tx_str = tx_str + chr(32)
    return tx_str


# splits a text string into a word list by whitespace
# input:  a text string containing words delimited by whitespace
# output: a list of words
def splitTextIntoWordList(txStr):
    aWordList = txStr.split(chr(32))

    # remove any blank words that were generated due to hypen/space subsitution
    bWordList = []
    for word in aWordList:
        if (word != ''):
            bWordList.append(word)
    
    return bWordList


# removes soft carriage returns that may be embedded in a word
# - joins incompleted sentences that are separated by soft CRs
# - recognize when a new sentence begins after a CR
# input:  a list of words that may contain embedded CRs
# output: a list of words with the embedded CRs resolved
def rmSoftCRs(iList):
    wList = []
    for word in iList:
        # the word does not have a CR
        if (word.find(chr(10)) < 0):
            wList.append(word)
        # the word has an embedded CR
        else:
            # partition the word into before & after CR
            t = word.partition(chr(10))
            
            # if the before word is blank and the after word is Titled then it is the start of a new sentence
            if ((len(t[0]) == 0) and (t[2].istitle())):
                wList.append(word)
            # the word represents an incomplete sentence, remove the CR & append before & after words
            else:
                wList.append(t[0])
                wList.append(t[2])
    return wList

# checks to see if an exclusion string is a substring in a word
# - needed to use find to handle cases where a CR is preappended
#   to the exclusion word
# input:  a word/phrase
# output: a Boolean (True = exclusion word found)
def checkForExclusion(phrase):
    returnValue = False
    # handle cases were exclusion string is the string in the phrase
    exclusionWords = ["Mr.", "Mrs.", "Dr.", "Fr.", "Jr.", "St.", "Esq.", "ect."]
    if ([elem for elem in exclusionWords if elem == phrase]): # first code attempt
      returnValue = True
    # handle cases were exclusion string is a substring in the phrase
    else:
        # check for exclusion substring
        if (phrase.find("Mr.") > 0):
            returnValue = True
        elif (phrase.find("Mrs.") > 0):
            returnValue = True
        elif (phrase.find("Dr.") > 0):
            returnValue = True
        elif (phrase.find("Fr.") > 0):
            returnValue = True
        elif (phrase.find("Jr.") > 0):
            returnValue = True
        else:
            if (phrase.find("St.") > 0):
                returnValue = True
    return returnValue

        
# construct new sentences from embedded sentences
# - differentiate abbreviations from end of sentences
# input:  a list of words
# output: a list of words with embedded sentences resolved
def resolveEmbeddedSentences(embeddedWordList):
    nonEmbeddedWordList = []
    i = -1
    for word in embeddedWordList:
        i = i + 1
        # if the word is in the exclusion list, then do not process it as an end of sentence delimiter
        if (checkForExclusion(word)):
            nonEmbeddedWordList.append(word)
        # determine if there is an end of sentence delimiter in the word
        else:
            # if the word has a period
            if (word.find(chr(46)) > 0):
                # if there is a CR
                if (word.find(chr(10)) > 0):
                    # if there is a CR after the period, just append the word
                    if ((word.rfind(chr(10))) > word.find(chr(46))):
                        nonEmbeddedWordList.append(word)
                    # if there is no CR following the period, append a CR to the word & append
                    else:
                        delimitedWord = word + chr(10)
                        nonEmbeddedWordList.append(delimitedWord)
                # the word does not have a CR
                else:
                    delimitedWord = word + chr(10)
                    nonEmbeddedWordList.append(delimitedWord)
            # the word has an exclamation point
            elif (word.find(chr(33)) > 0):
                # if there is a CR after the exclamation point, just append the word
                if ((word.rfind(chr(10))) > word.find(chr(33))):
                    nonEmbeddedWordList.append(word)
                # if there is no CR following the period, append a CR to the word & append
                else:
                    delimitedWord = word + chr(10)
                    nonEmbeddedWordList.append(delimitedWord)
            # the word has an question mark
            elif (word.find(chr(63)) > 0):
                # if there is a CR after the question mark, just append the word
                if ((word.rfind(chr(10))) > word.find(chr(63))):
                    nonEmbeddedWordList.append(word)
                # if there is no CR following the period, append a CR to the word & append
                else:
                    delimitedWord = word + chr(10)
                    nonEmbeddedWordList.append(delimitedWord)
            # the word was not an embedded sentence, just append the word
            else:
                nonEmbeddedWordList.append(word)
    return nonEmbeddedWordList


# split a string of sentences into a lists of sentences by CR
# input:  a string of words representing sentences delimited by CRs
# output: a list of sentences with each sentence a list of words
def convertSentencesToLists(aStringOfSentences):
    listsOfSentences = []
    aSentence = []
    for word in aStringOfSentences:
        # the word does not have a CR
        if (word.find(chr(10)) < 0):
            aSentence.append(word)
        # the word has an embedded CR
        else:
            after_word = word
            while (after_word.find(chr(10)) > 0):
                # partition the phrase into before & after CR
                t = after_word.partition(chr(10))
            
                # append the before to the current sentence
                before_word = t[0]
                aSentence.append(before_word)
            
                # append the current sentence to the document
                listsOfSentences.append(aSentence)
            
                # start a new sentence with the after word
                aSentence = []
                after_word = t[2]
            if (after_word != ''):
                aSentence.append(after_word)
    listsOfSentences.append(aSentence)
    return listsOfSentences


# remove the punctuation characters from the sentenceList
# input:  a list of sentence lists with embedded punctuation marks
# output: a list of sentence lists with without punctuation marks
def rmPunctuationFromSentences(sentList):
    cleanedListOfSenences = []
    for s in sentList:
        cleanedSentence = []
        for w in s:
          cleanedSentence.append(rmPunctuationStr(w))
        cleanedListOfSenences.append(cleanedSentence)
    return cleanedListOfSenences


# calculate the word length for each word in each sentence
# input:  a list of sentence lists which contain words
# output: a list of integer lists, each integer represents a the character count of a word in a sentence
def sentenceWordLength(cleanedSentenceList):
    wordLengthPerSentenceList = []
    for sent in cleanedSentenceList:
        sentenceWordLen = []
        # for each word in a sentence, count the number of characters in the word
        for w in sent:
            sentenceWordLen.append(len(w))
    
        # append the word lengths per sentence to the list of sentences
        wordLengthPerSentenceList.append(sentenceWordLen)
    return wordLengthPerSentenceList


# calculate the sum value of the integers in a list
# input:  a list of integers
# output: an integer representing the sum of the integers in a list
def sumIntegerList(integerList):
    sumValue = 0
    for i in integerList:
        sumValue = sumValue + i
    return sumValue


# calculated sentence statistics
# for each sentence:
# - count the number of words
# - calculate the sum of the length of the words
# - calculate the mean lenght of the words
# input:  a list of integer lists, each integer represents a the character count of a word in a sentence
# output: a list of integer lists, each list represents the total word length, the word count, and the mean word length
def calculateSentenceStats(intLists):
    sentenceStatList = []
    for iSent in intLists:
        # initialize statistic variables
        sentenceStat = []
        totalCharCount = 0
        wordCount = 0
        meanCharCount = 0
        
        # calculate statistic variables
        totalCharCount = sumIntegerList(iSent)
        wordCount = len(iSent)
        if (wordCount > 0):
            meanCharCount = totalCharCount/wordCount
        
        # create a list for the sentence's statistics
        sentenceStat.append(totalCharCount)
        sentenceStat.append(wordCount)
        sentenceStat.append(meanCharCount)
        
        # append the sentence's statistics list to the list of sentence statistics
        sentenceStatList.append(sentenceStat)
    return sentenceStatList

    
# create a dataframe to hold the sentence statistics
# input:  list of sentence statistics: the total word length, the word count, and the mean word length
#         list of sentences with punctuation removed
# output: the dataframe
def createDF(sentStatList, listOfCleanedSents):
    # create a blank dataframe
    aDF = pd.DataFrame()
    
    # create a series for the total word length values
    totalWordLengthList = []
    for s in sentStatList:
        totalWordLengthList.append(s[0])
    aDF['totalWordLength'] = totalWordLengthList
    
    # create a series for the word count values
    wordCountList = []
    for s in sentStatList:
        wordCountList.append(s[1])
    aDF['wordCount'] = wordCountList
    
    # create a series for the mean word length values
    meanWordLengthList = []
    for s in sentStatList:
        meanWordLengthList.append(s[2])
    aDF['meanWordLength'] = meanWordLengthList
    
    # create a series for the cleaned sentences
    cleanSentList = []
    for cSent in listOfCleanedSents:
        cleanSentList.append(cSent)
    aDF['cleanSentenceList'] = cleanSentList
    
    return(aDF)


def exportSentenceStatistics(csvFN, bDF):
    bDF.to_csv(csvFN, sep=',', encoding='utf-8', quotechar='"', na_rep='', index=False, index_label=False, \
        columns = ['totalWordLength', 'wordCount', 'meanWordLength', 'cleanSentenceList'], \
        header  = ['totalWordLength', 'wordCount', 'meanWordLength', 'cleanSentenceList'])

        
# debug:  write to file the list of sentences
# input:  output filename, list of sentences
# output: output file of words per sentence
def writeSentenceList(outputFN, sList):
    file = open(outputFN, 'w')
    for sentence in sList:
        for word in sentence:
            file.write(word)
            file.write(" ")
        file.write(chr(10))
    file.close()


# debug:  write to file a list of words
# input:  output filename, list of words
# output: output file of words in the list
def writeWordList(outputFN, wList):
    file = open(outputFN, 'w')
    for word in wList:
        file.write(word)
        file.write(chr(10))
    file.close()


# debug:  find all words with a period
# input:  list of words
# output: list of words
def findAllWordsWithPeriods(wordList):
    wordsWithPeriodsList = []
    for w in wordList:
        if(w.find(chr(46)) > 0):
            wordsWithPeriodsList.append(w)
    return wordsWithPeriodsList
          

# main routine
#def main():
# set the input & output file name
inputFileName  = 'Pride.txt'
outputFileName = 'Pride_Sentences.txt'
debugFileName  = 'debug.csv'
csvFileName    = 'Pride_Sentence_Stats.csv'

# read the input text character by character
textStr = read_input(inputFileName)

# create a word list from the text that was read
wordList = splitTextIntoWordList(textStr)

# remove the soft carriage returns and join the fragmented sentences
removedSoftCrWordList = rmSoftCRs(wordList)

# break apart multiple sentences within a sentence
sentenceWordList = resolveEmbeddedSentences(removedSoftCrWordList)

# create a list of sentences with each sentence representingh a list of words
sentenceList = convertSentencesToLists(sentenceWordList)

# remove the punctuation marks from the list of sentences
listOfCleanedSentences = rmPunctuationFromSentences(sentenceList)

# count the number of characters per word in each sentence
characterWordCountSentenceList = sentenceWordLength(listOfCleanedSentences)

# calculate the statistics for a sentence
sentenceStatisticsList = calculateSentenceStats(characterWordCountSentenceList)

# create a panda containing sentence statistics: the total word length, the word count, and the mean word length
df = createDF(sentenceStatisticsList, listOfCleanedSentences)

# export the dataframe into a .csv file
exportSentenceStatistics(csvFileName, df)

# list the top rows of the dataframe
print(df.head())



# Problem 2a: Introduction: Counting the letter 'e'
# ---------------------------------------------------------------------
# -*- coding: utf-8 -*-

# import libraries
import os
import string

# set working directory
os.chdir('C:/_DS710/Temp07')

# define a function to remove the standard punctuation marks from a string
# note: a space is not a punctuation mark
# input:  a string with punctuation marks
# output: a string with punctuation marks removed
def rmPunctuationString(s):
    rmPunctuation_table = str.maketrans("", "", string.punctuation)
    processed_String =  s.translate(rmPunctuation_table)
    return processed_String


# reads an input file of text and stores into an output file a string of characters that exclude spaces, carriage returns
# input:  a name of a file that contains characters to be read
# output: an output file a string of characters that exclude spaces, carriage returns, and non-printable characters
# note: detect encoding of input file via command line chardetect <iFN>
def readWriteText(inputTX, inEncode, outputTX):
    f2 = open(outputTX, 'w', encoding="utf-8", errors="ignore")
    with open(inputTX, 'r', encoding=inEncode, errors="ignore") as f1:
        # itterate over the lines in the input text
        for iLine1 in iter(f1.readline, ""):
            # remove the punctuation marks
            pLine1 = rmPunctuationString(iLine1)
            
            # process each processed line of input
            if (len(pLine1) > 1):
                # process each character in the processed line
                for ch1 in pLine1:
                    # if the character read is a space or a carriage return, then skip it
                    if ((ch1 == chr(32)) or (ch1 == chr(10))):
                        pass
                    # write the character to the output file
                    else:
                      f2.write(ch1)
    # close all files
    f2.close()
    f1.close()


# count the number of letters (i.e., non-digits [0..9] in a input file; exclude whitespaces, punctuation marks, digits
# input:  a name of a file that contains characters to be counted
# output: a integer representing the number of letters (non-digit) characters in the file
def count_letters(inFN):
    # exclude carriage return, space, and digit characters
    exclusionChars = {chr(10), chr(32), chr(48), chr(49), chr(50), chr(51), chr(52), chr(52), chr(53), chr(54), chr(55), chr(56), chr(57)}
    
    # initialize the counter
    numberOfLettersInFile = 0
    
    # process the input file    
    with open(inFN, 'r', encoding='utf-8', errors="ignore") as f_in:
        for iLine2 in f_in:
            if (len(iLine2) > 1):
                # remove the punctuation marks
                pLine2 = rmPunctuationString(iLine2)
                
                # count the number of characters in the processed line, exclude digit characters
                for ch2 in pLine2:
                    # exclude digit characters
                    if (ch2 in exclusionChars):
                        pass
                    else:
                        numberOfLettersInFile = numberOfLettersInFile + 1
    # return the number of digits found in the input file
    return numberOfLettersInFile


# count the variants of the letter e in a input file, exclude whitespaces, punctuation marks
# input:  a name ofa file that contains characters to be counted, 
#         the suspected encoding of the input file
#         a boolean flag on whether upper/lower case is to be ignored
#         a boolean flag on whether accent variations is to be ignored
# assumptions: ignore case means that all upper case e variant letters will be added to the lower case letter variant
# output: a integer representing the number of variants of the letter e in the form of a tuple constructed as:
#         (lower_e_normal, lower_e_acute, lower_e_circumflex, lower_e_grave, 
#          upper_e_normal, upper_e_acute, upper_e_circumflex, upper_e_grave)
def count_letter_e(inFN, inEncoding, ignore_case, ignore_accents):
    # define the filename for temporary output
    outFN = 'temp.out'
    
    # initialize count variables for reporting
    lower_e_normal     = 0
    lower_e_acute      = 0
    lower_e_circumflex = 0
    lower_e_grave      = 0
    upper_e_normal     = 0
    upper_e_acute      = 0
    upper_e_circumflex = 0
    upper_e_grave      = 0

    # read all the characters in the input filename and store the characters in a temporary file
    # exclude spaces, carriage returns, and non-printable characters
    # convert the suspected encoding to utf-8
    readWriteText(inFN, inEncoding, outFN)
    
    # count the occurance of the variants of the letter e
    f = open(outFN, 'r', encoding='utf-8', errors="ignore")
    while True:
        aCh = f.read(1)
        if (not aCh):
            break
        else:
            if (aCh == chr(101)):
                lower_e_normal = lower_e_normal + 1
            elif (aCh == chr(233)):
                lower_e_acute = lower_e_acute + 1
            elif (aCh == chr(234)):
                lower_e_circumflex = lower_e_circumflex + 1
            elif (aCh == chr(232)):
                lower_e_grave = lower_e_grave + 1
            elif (aCh == chr(69)):
                upper_e_normal = upper_e_normal + 1
            elif (aCh == chr(201)):
                upper_e_acute = upper_e_acute + 1
            elif (aCh == chr(202)):
                upper_e_circumflex = upper_e_circumflex + 1
            elif (aCh == chr(200)):
                upper_e_grave = upper_e_grave + 1
            else:
                pass
    # close temporary file
    f.close
    
    # process input flags
    if ((ignore_case == True) and (ignore_accents == True)):
        lower_e_normal = lower_e_normal + lower_e_acute + lower_e_circumflex + lower_e_grave + \
                         upper_e_normal + upper_e_acute + upper_e_circumflex + upper_e_grave
        lower_e_acute      = 0
        lower_e_circumflex = 0
        lower_e_grave      = 0
        upper_e_normal     = 0
        upper_e_acute      = 0
        upper_e_circumflex = 0
        upper_e_grave      = 0
    elif ((ignore_case == True) and (ignore_accents == False)):
        lower_e_normal     = lower_e_normal     + upper_e_normal
        lower_e_acute      = lower_e_acute      + upper_e_acute
        lower_e_circumflex = lower_e_circumflex + upper_e_circumflex
        lower_e_grave      = lower_e_grave      + upper_e_grave
        upper_e_normal     = 0
        upper_e_acute      = 0
        upper_e_circumflex = 0
        upper_e_grave      = 0
    else:
        if ((ignore_case == False) and (ignore_accents == True)):
            lower_e_normal     = lower_e_normal + lower_e_acute + lower_e_circumflex + lower_e_grave
            upper_e_normal     = upper_e_normal + upper_e_acute + upper_e_circumflex + upper_e_grave
            lower_e_acute      = 0
            lower_e_circumflex = 0
            lower_e_grave      = 0
            upper_e_acute      = 0
            upper_e_circumflex = 0
            upper_e_grave      = 0
    
    # construct ouput
    lower_e_normal_str     = str(lower_e_normal)
    lower_e_acute_str      = str(lower_e_acute)
    lower_e_circumflex_str = str(lower_e_circumflex)
    lower_e_grave_str      = str(lower_e_grave)
    upper_e_normal_str     = str(upper_e_normal)
    upper_e_acute_str      = str(upper_e_acute)
    upper_e_circumflex_str = str(upper_e_circumflex)
    upper_e_grave_str      = str(upper_e_grave)

    retValue = "(" + lower_e_normal_str + "," + lower_e_acute_str + "," + lower_e_circumflex_str + "," + lower_e_grave_str + ", " + \
                     upper_e_normal_str + "," + upper_e_acute_str + "," + upper_e_circumflex_str + "," + upper_e_grave_str + ")"    
    # return output
    return retValue


# ---debug ------------------------------------------------------------
# count the number of digits (0..9) in a input file, exclude whitespaces, exlcude punctuation marks
# input:  a name ofa file that contains characters to be counted
# output: a integer representing the number of digit characters in the file
def count_digits(inFN):
    # only consider digit characters
    inclusionChars = {chr(48), chr(49), chr(50), chr(51), chr(52), chr(52), chr(53), chr(54), chr(55), chr(56), chr(57)}
    
    # initialize the counter
    numberOfDigitsInFile = 0
    
    # process the input file    
    with open(inFN, 'r') as f_in:
        for line in f_in:
            if (len(line) > 1):
                for ch in line:
                    # only include digit characters
                    if (ch in inclusionChars):
                        numberOfDigitsInFile = numberOfDigitsInFile + 1
    # return the number of digits found in the input file
    return numberOfDigitsInFile


# write test output
# input:  iFN, iStr, ignore_case, ignore_accents
# output: formatted results string
def writeTestResult(iFN, inEncodeSuspect, iStr, ignore_case, ignore_accents):
    print(iFN, \
    ": '", iStr, 
    ": Suspected Encoding = ", inEncodeSuspect, \
    "' : ignore_case =", ignore_case, \
    " : ignore_accents =", ignore_accents, \
    " : result =", count_letter_e(iFN, inEncodeSuspect, ignore_case, ignore_accents), \
    " = (e,é,ê,è, E,É,Ê,È)")

    
# ---test -------------------------------------------------------------
# unit tests
print("UNIT TESTS")
print("----------")

print("letter count in 'pride.txt' = ", count_letters('pride.txt'))
print("digit  count in 'pride.txt'  = ", count_digits('pride.txt'))
print("")

print("letter count in l'enlevement.txt = ", count_letters("l'enlevement.txt"))
print("digit  count in l'enlevement.txt = ", count_digits("l'enlevement.txt"))
print("")

writeTestResult('assignment7_test_00.txt', "utf-8", "après tête,général;APRÈS>TÊTE:GÉNÉRAL", True,  True)
writeTestResult('assignment7_test_00.txt', "utf-8", "après tête,général;APRÈS>TÊTE:GÉNÉRAL", True,  False)
writeTestResult('assignment7_test_00.txt', "utf-8", "après tête,général;APRÈS>TÊTE:GÉNÉRAL", False, True)
writeTestResult('assignment7_test_00.txt', "utf-8", "après tête,général;APRÈS>TÊTE:GÉNÉRAL", False, False)


# Problem 2b: Apply Your Code
# ---------------------------------------------------------------------
writeTestResult("Pride.txt", "utf-8", '', True,  True)
writeTestResult("Pride.txt", "utf-8", '', True,  False)
writeTestResult("Pride.txt", "utf-8", '', False, True)
writeTestResult("Pride.txt", "utf-8", '', False, False)
print("")

writeTestResult("l'enlevement.txt", "Windows-1252", '', True,  True)
writeTestResult("l'enlevement.txt", "Windows-1252", '', True,  False)
writeTestResult("l'enlevement.txt", "Windows-1252", '', False, True)
writeTestResult("l'enlevement.txt", "Windows-1252", '', False, False)

