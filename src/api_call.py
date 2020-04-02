import pandas as pd
import numpy as np
import os

from paralleldots import set_api_key,get_api_key,emotion,sentiment,intent,abuse,taxonomy,usage,keywords

# religions = pd.read_csv("dataset/religions.csv")
# religions = list(religions['Religion'])
# religions = [religion.lower() for religion in religions]
# religions = set(religions)
#
# clickbaits = pd.read_csv('dataset/clickbaits.csv')
# clickbaits = list(clickbaits['Word'])
# clickbaits = set(clickbaits)

def get_emotion(string):
    '''Returns emotion and emotion score of a string as a PD Series'''
    try:
        title_emotion = emotion(string)
        title_emotion = (sorted(((title_emotion['emotion']).items()), key=lambda kv: (kv[1], kv[0]), reverse=True))[0]
        emotion_type = title_emotion[0]
        emotion_score = title_emotion[1]
        return pd.Series([emotion_type,emotion_score])

    except:
        print("Error in ", string)

def get_intent(string):
    '''Returns intent and intent score of a string as a PD Series'''
    try:
        title_intent = intent(string)
        title_intent['intent'].pop('feedback')
        title_intent = (sorted(((title_intent['intent']).items()), key=lambda kv: (kv[1], kv[0]), reverse=True))[0]
        intent_type = title_intent[0]
        intent_score = title_intent[1]
        return pd.Series([intent_type, intent_score ])

    except:
        print("Error in ", string)


def get_taxo(string):
    '''Returns taxonomy and confidence score of a string as a PD Series'''
    try:
        text_taxo = taxonomy(string)
        # text_taxo = (sorted(((text_taxo['taxonomy']).items()), key=lambda kv: (kv[1], kv[0]), reverse=True))[0]
        text_tag = text_taxo['taxonomy'][0]['tag']
        text_tag_score =   text_taxo['taxonomy'][0]['confidence_score']
        return pd.Series([text_tag, text_tag_score])

    except:
        print("Error in ", string)

def get_kw(string):
    '''Return all the keywords in a string'''
    try:
        keys = keywords(string)
        keys = keys['keywords']
        key_list = []
        for i in range(len(keys)):
            key_list.append(keys[i]['keyword'])
        return key_list

    except:
        print("Error in ", string)

# def has_relig(list):
#     '''Returns x>1 if the keyword list contains any religion entity'''
#     try:
#         rel = pd.read_csv('dataset/religions.csv')
#         rel = list(rel['Religion'])
#         rel = set([x.lower() for x in rel])
#         kws = set(list)
#         kws = set([x.lower() for x in kws])
#         length = len(rel.intersection(kws))
#         try:
#             del rel
#             del kws
#         return length
#
#     except:
#         print("Error encountered!")
#
# def has_bait(string):
#     '''Returns x>1 if the title contains any clickbait entity'''
#     try:
#         clickbait = pd.read_csv('dataset/clickbaits.csv')
#         clickbait = list(clickbait['Word'])
#         clickbait = set([x.lower() for x in clickbait])
#         words_in_text = set(string.split())
#         len = len(clickbait.intersection(words_in_text))
#         try:
#             del clickbait
#             del words_in_text
#         return len

    # except:
    #     print("Error encountered!")

def get_abuse(string):
    '''Returns abuse and abuse score of a string as a PD Series'''
    try:
        text_abuse = abuse(string)
        text_abuse = (sorted(((text_abuse).items()), key=lambda kv: (kv[1], kv[0]), reverse=True))[0]
        text_abuse_type = text_abuse[0]
        text_abuse_score = text_abuse[1]
        return pd.Series([text_abuse_type,text_abuse_score])

    except:
        print("Error in ", string)

def get_sentiment(string):
    '''Returns sentiment and sentiment score of a string as a PD Series'''
    try:
        sent = sentiment(string)
        sent = (sorted(((sent['sentiment']).items()), key=lambda kv: (kv[1], kv[0]), reverse=True))[0]
        sent_type = sent[0]
        sent_score = sent[1]
        return pd.Series([sent_type,sent_score])
    except:
        print("Error in ",string)