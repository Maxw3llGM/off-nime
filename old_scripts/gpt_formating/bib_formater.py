from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
import os
from dotenv import load_dotenv
import json
import pickle
import pandas as pd
import bibtexparser as bp
from bibtexparser.library import Library
from bibtexparser.splitter import Splitter
from fuzzywuzzy import fuzz

load_dotenv()
API_KEY = os.getenv("GPT_API")

origina_data : pd.DataFrame = pd.read_pickle("ISIDM/sorted_references.pkl")
origina_data = origina_data.reset_index()
original_names = origina_data['references'].map(lambda x : x.split(",")[0].split('.')[0].split(' ')[0])
# print(origina_data['references'].map(lambda x : x.split(",")[0]))
# print(type(original_names))
bib_database = bp.parse_file("scripts/gpt_formating/gpt_bibtexts.bib")
print(len(bib_database.blocks), ' | ', len(bib_database.entries), ' | ', len(bib_database.failed_blocks))
# print(type(bib_database))
gpt_names =[]
# print(bib_database.failed_blocks)
# for x in bib_database.failed_blocks[13:]:
#     # print(x.error)
#     print(x.ignore_error_block)
#     print(bib_database.entries_dict[x.ignore_error_block.key])

def last_name_extraction(entry):
    last_name = ''
    if entry.key == 'Rockmore1998':
        last_name = entry["title"].split(',')[0].split(' ')[0]
    else:
        try:
            last_name = entry['author'].split(',')[0].split('.')[0].split(' ')[0]
        except KeyError:
            last_name = entry["editor"].split(',')[0].split('.')[0]
    return last_name
def process_bib_entries(bib_database):
    gpt_names = []
    for index, x in zip(range(0, len(bib_database.entries)), bib_database.entries):
        gpt_names.append(last_name_extraction(x))
    return gpt_names

def compare_names(gpt_names_pd, original_names):
    for i in range(0, max(gpt_names_pd.size, original_names.size)):
        try:
            if i >= gpt_names_pd.size:
                y_gpt = " "
            else:
                y_gpt = gpt_names_pd['Names'][i]
            
            if i >= original_names.size:
                y_original = " "
            else:
                y_original = original_names[i]
        except KeyError:
            print(i, ":", original_names[97])
            raise

        print(y_original, ":", y_gpt)

def find_missing_references(oData, bData):
    missing_refs = []
    bool_ref = 0
    for original_ref in oData:
        original_name = original_ref.split(",")[0].split('.')[0].split(' ')[0].lower()
        
        # if bool_ref == 0:
        #     missing_refs.append(original_ref)
    return missing_refs

gpt_names = process_bib_entries(bib_database)
gpt_names_pd = pd.DataFrame({'Names':gpt_names})

gpt_name = ''
original_name = ''
print("ORIGINAL COLUMN : GPT COLUMN")
compare_names(gpt_names_pd, original_names)

missing_refs = find_missing_references(origina_data['references'],bib_database.entries)
print(len(missing_refs))


# while (not original_names_t.empty):
#     if (not gpt_names):
#         gpt_name = 'Empty'
#     else:
#         gpt_name = gpt_names.pop(0)
#         original_name = original_names.drop(0)
#     print(original_name, " : ",gpt_name)


# print(len(bib_database.entries))
# for x in bib_database.failed_blocks:
#     print(x)