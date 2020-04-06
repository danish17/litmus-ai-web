"""Copyright 2020 Danish Shakeel

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""

import pandas as pd
import pickle

tool = pickle.load(open("models/language_tool.cls","rb"))

clickbait = pd.read_csv('datasets/clickbaits.csv')  # Load the dataset containing potential clickbait words
clickbait = list(clickbait['Word'])  # Convert it into list
clickbait = set([x.lower() for x in clickbait])  # Convert it into a set

rel = pd.read_csv('datasets/religions.csv')  # Load the dataset containing Religious words
rel = list(rel['Religion'])  # Convert it into list
rel = set([x.lower() for x in rel])  # Convert it into a set


# DEFINITION OF HAS_RELIG():
def has_relig(rel_list):
    """Returns x>1 if the keyword list contains any religion entity."""
    try:
        kws = set(rel_list)
        kws = set([x.lower() for x in kws])
        length = len(rel.intersection(kws))
        return length

    except:
        print("Error encountered!")


# DEFINTION OF HAS_BAIT():
def has_bait(string):
    """Returns x>1 if the title contains any clickbait entity."""
    try:
        words_in_text = set(string.split())
        int_len = len(clickbait.intersection(words_in_text))
        return int_len

    except:
        print("Error encountered!")


# DEFINTION OF GET_LENGTH():
def get_length(string):
    """Returns the length of a string."""
    try:
        string = string.split()
        return len(string)

    except:
        print("Error encountered!")


# DEFINITION OF GET_ENG_MISTAKES():
def get_eng_mistakes(string):
    try:
        mistakes = tool.check(string)
        return len(mistakes)

    except:
        print("Error in ", string)
