import pickle
import pandas as pd
import numpy as np
import language_check
from paralleldots import set_api_key
from src import nlp_custom
from src import api_call
from src import custom_encoder
from tensorflow.keras import models

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tool = language_check.LanguageTool('en-US')

clickbait = pd.read_csv('datasets/clickbaits.csv')  # Load the dataset containing potential clickbait words
clickbait = list(clickbait['Word'])  # Convert it into list
clickbait = set([x.lower() for x in clickbait])  # Convert it into a set

rel = pd.read_csv('datasets/religions.csv')  # Load the dataset containing Religious words
rel = list(rel['Religion'])  # Convert it into list
rel = set([x.lower() for x in rel])  # Convert it into a set

def cook(data):
    #data['decomposed_sum'] =
    data["decomposed_sum_sq"] = (data["title_emotion_score"]+data["text_emotion_score"]+data["title_intent_score"]+data["text_taxo_score"]+data["title_sentiment_score"])**2
    # new_df = \
    data.keys()

    cooked_data = [data["title_emotion"],
                   data['text_emotion'],
                   data["title_intent"],
                   data['text_taxo'],
                   data['has_rel'],
                   data['has_bait'],
                   data['title_sentiment'],
                   data['title_w_count'],
                   data['body_w_count'],
                   data['decomposed_sum_sq'],
                   data['title_errors'],
                   data['text_errors']]

    return cooked_data

def parallel_ensemble(cooked_data):

    cooked_data = np.array(cooked_data)

    model1 = pickle.load(open("models/rf.mdl","rb"))
    vote_1 = model1.predict(cooked_data.reshape(1,-1))[0]

    model2 = pickle.load(open("models/nbayes.mdl","rb"))
    vote_2 = model2.predict(cooked_data.reshape(1,-1))[0]

    model3 = pickle.load(open("models/log_reg.mdl","rb"))
    vote_3 = model3.predict(cooked_data.reshape(1,-1))[0]

    del model1,model2,model3

    cooked_data = np.append(cooked_data,[vote_1,vote_2,vote_3])

    return cooked_data

def dense_model(to_feed):
    brain = models.load_model("models/ann.h5")
    score = brain.predict(to_feed.reshape(1,-1))
    to_feed = np.append(to_feed,score)
    return to_feed

def hybrid_ensemble(data):
    cooked_data = cook(data)
    to_feed = parallel_ensemble(cooked_data)
    prediction = dense_model(to_feed)

    return prediction

def encode(data):
    encoder = pickle.load(open("models/std_encoder.enc","rb"))
    data["title_emotion"] = custom_encoder.encode_emotion(data["title_emotion"])
    data["text_emotion"] = custom_encoder.encode_emotion(data["text_emotion"])
    data["title_intent"] = custom_encoder.encode_intent(data["title_intent"])
    data["text_taxo"] = encoder.transform([data["text_taxo"]])[0]
    data["title_sentiment"] = custom_encoder.encode_sentiment(data["title_sentiment"])

    return data

def builder(title,text,api_key):
    set_api_key(api_key)  # sets the API key

    # get the emotion of title:
    title_emotion = api_call.get_emotion(title)
    title_emotion_score = title_emotion[1]
    title_emotion = title_emotion[0]

    # get the emotion of text:
    text_emotion = api_call.get_emotion(text)
    text_emotion_score = text_emotion[1]
    text_emotion = text_emotion[0]

    title_intent = api_call.get_intent(title)
    title_intent_score = title_intent[1]
    title_intent = title_intent[0]

    text_taxo = api_call.get_taxo(text)
    text_taxo_score = text_taxo[1]
    text_taxo = text_taxo[0]

    keywords = api_call.get_kw(text)

    has_religion = nlp_custom.has_relig(keywords)

    has_bait = nlp_custom.has_bait(title)

    title_sentiment = api_call.get_sentiment(title)
    title_sentiment_score = title_sentiment[1]
    title_sentiment = title_sentiment[0]

    title_w_count = nlp_custom.get_length(title)
    body_w_count = nlp_custom.get_length(text)

    title_errors = nlp_custom.get_eng_mistakes(title)
    text_errors = nlp_custom.get_eng_mistakes(text)

    data = {"title_emotion": title_emotion,
            "title_emotion_score": title_emotion_score,
            "text_emotion": text_emotion,
            "text_emotion_score": text_emotion_score,
            "title_intent": title_intent,
            "title_intent_score": title_intent_score,
            "text_taxo": text_taxo,
            "text_taxo_score": text_taxo_score,
            "keywords": keywords,
            "has_rel": has_religion,
            "has_bait": has_bait,
            "title_sentiment": title_sentiment,
            "title_sentiment_score": title_sentiment_score,
            "title_w_count": title_w_count,
            "body_w_count": body_w_count,
            "title_errors": title_errors,
            "text_errors": text_errors}
    return data

def pipeline(title,text,api_key):
    # title = "Omar questions domicile law for J&K"
    # text = " Former Jammu and Kashmir Chief Minister Omar Abdullah questioned the “suspect timing” of the domicile rules defined by the centre amid  prevailing situation owing to Covid-19 outbreak. “Talk about suspect timing. At a time when all our efforts & attention should be focused on the #COVID outbreak the government slips in a new domicile law for J&K. Insult is heaped on injury when we see the law offers none of the protections that had been promised,” Omar wrote on Twitter. "
    # api_key = "Fq0rdRKXqpPRoqyIoIN0oOyPpPo3WGtiuDMeRKwuwqM"
    data = builder(title,text,api_key)
    features = [data['title_emotion'],data['text_emotion'],data['title_intent'],data['text_taxo'],data['title_sentiment']]
    data = encode(data)
    prediction = hybrid_ensemble(data)

    ann_score = prediction[15]
    m1_score = prediction[14]
    m2_score = prediction[13]
    m3_score = prediction[12]
    features.extend([m1_score,m2_score,m3_score,ann_score])

    return features