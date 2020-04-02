import language_check
import pandas as pd

tool = language_check.LanguageTool('en-US')

clickbait = pd.read_csv('datasets/clickbaits.csv')  # Load the dataset containing potential clickbait words
clickbait = list(clickbait['Word'])  # Convert it into list
clickbait = set([x.lower() for x in clickbait])  # Convert it into a set

rel = pd.read_csv('datasets/religions.csv')  # Load the dataset containing Religious words
rel = list(rel['Religion'])  # Convert it into list
rel = set([x.lower() for x in rel])  # Convert it into a set

#DEFINITION OF HAS_RELIG():
def has_relig(list):
    '''Returns x>1 if the keyword list contains any religion entity.'''
    try:
        kws = set(list)
        kws = set([x.lower() for x in kws])
        length = len(rel.intersection(kws))
        return length

    except:
        print("Error encountered!")

#DEFINTION OF HAS_BAIT():
def has_bait(string):
    '''Returns x>1 if the title contains any clickbait entity.'''
    try:
        words_in_text = set(string.split())
        int_len = len(clickbait.intersection(words_in_text))
        return int_len

    except:
        print("Error encountered!")

#DEFINTION OF GET_LENGTH():
def get_length(string):
    '''Returns the length of a string.'''
    try:
        string = string.split()
        return len(string)

    except:
        print("Error encountered!")

#DEFINITION OF GET_ENG_MISTAKES():
def get_eng_mistakes(string):
    try:
        mistakes = tool.check(string)
        return len(mistakes)
    except:
        print("Error in ",string)
