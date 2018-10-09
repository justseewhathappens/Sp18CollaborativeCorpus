#written by Jennie Wolfgang and Erica Brozovsky for E 396L, Spring 2018
#libraries
import re
import json
import os
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import io

#Functions written for each calculation
#they are stored in the file "text_mining_calculations.py", and just need to be in the same directory
from text_mining_calculations import get_ttr
from text_mining_calculations import get_nouniness
from text_mining_calculations import get_mean_word_len
from text_mining_calculations import get_mean_sentence_len
from text_mining_calculations import get_np_info
from text_mining_calculations import get_sub_conj

#define global variable for paths and data files
folder_path = 'C:/data/'
jsonFileName = 'coha_text_mining_results'
col_names = ['word','lemma','POS']
null_character_replacement = ' '

#custom function to read in txt files with null chars and unescaped "
def get_data_from_file(file_location):
    #Open Files
    with open(file_location, 'r') as f:
        str1 = f.read()

    ##uncomment if the first line is determined to be bogus
    index = 0
    for i in range(0,len(str1)):
       if(str1[i] == '\n'):
           index = i
           break
    str1 = str1[index:]
    
    #Replace end of lines with tabs for proper delimiting
    str1 = str1.replace('\n','\t')

    #Remove the impossible case of \t\t
    str1 = str1.replace('\t\t','\t')

    #Strip out the beginning and ending whitespaces, tabs, and new lines that'll mess you up
    #Then split on tabs
    strsplit = str1.strip().split('\t')

    #Create numpy array and reshape it into len(strsplit)/3 rows and 3 columns
    a = np.array(strsplit).reshape(int(len(strsplit)/3),3)

    data_frame = pd.DataFrame(data=a, columns=col_names)
    return data_frame

def main():
    #start by loading all data from the folder of txt files
    #declare a dataframe to build the data into
    doc_results_combined = pd.DataFrame()
    
    all_files = os.listdir(folder_path)
    #wrap the iterator in tqdm for a progress bar
    all_files = tqdm(all_files)
    
    #iterate through all files in the folder
    for file_name in all_files:
        
        doc_info = re.split(r'_', file_name)
        doc_genre = doc_info[0]
        doc_year = doc_info[1]
        doc_id = doc_info[2][:-4]
        #print(f'genre: {doc_genre} \r year: {doc_year} \r id: {doc_id}')

        #Get file txt data, put into data frame
        full_file_location = folder_path + file_name
        #get the file contents, without nulls
        doc_text = get_data_from_file(full_file_location)
        
        #Calculate data of interest and build row to add to all results
        #first genre, year, and id
        doc_data = [[doc_genre,doc_year,doc_id,0,0,0,0,0,0,0]]
        resultColumns = ['genre','year','id','ttr','nouniness','mean_word_len','mean_sentence_len','mean_np_len', 'max_np_len', 'sub_conj']
        doc_results = pd.DataFrame(data=doc_data, columns = resultColumns)
        #print(doc_results)
        
        #function calls imported above on doc text data frame
        doc_results['ttr'] = get_ttr(doc_text)
        doc_results['nouniness'] = get_nouniness(doc_text)
        doc_results['mean_word_len'] = get_mean_word_len(doc_text)
        doc_results['mean_sentence_len'] = get_mean_sentence_len(doc_text)
        doc_results['mean_np_len'], doc_results['max_np_len'] = get_np_info(doc_text)
        doc_results['sub_conj'] = get_sub_conj(doc_text)

        #Append all data for this doc to the entire list
        doc_results_combined = doc_results_combined.append(doc_results, ignore_index= True)
        
    #Dump combined data to json file for easy loading into next script
    doc_results_combined_json = doc_results_combined.to_dict('index')
    #Create a unique file name using date and time so the file won't overwrite another
    jsonFileNameNow = jsonFileName + time.strftime("%d%b%H%M%S", time.localtime())
    with open("{}.json".format(jsonFileNameNow), 'w') as outfile:
        json.dump(doc_results_combined_json, outfile, sort_keys = True, indent = 4)


if __name__ == '__main__': main()
