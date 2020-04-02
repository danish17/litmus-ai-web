def encode_emotion(emotion):
    to_return = -1
    if emotion == "Happy":
        to_return = 0
    elif emotion == "Angry":
        to_return = 1
    elif emotion == "Excited":
        to_return = 2
    elif emotion == "Sad":
        to_return = 3
    elif emotion == "Fear":
        to_return = 4
    elif emotion == "Bored":
        to_return = 5
    return to_return


def encode_intent(intent):
    to_return = -1
    if intent == "news".casefold():
        to_return = 0
    elif intent == "feedback".casefold():
        to_return = 1
    elif intent == "query".casefold():
        to_return = 2
    elif intent == "marketing".casefold():
        to_return = 3
    elif intent == "spam".casefold():
        to_return = 5
    return to_return

def encode_sentiment(sentiment):
    to_return = -1
    if sentiment == "negative".casefold():
        to_return = 0
    elif sentiment == "positive".casefold():
        to_return = 1
    elif sentiment == "neutral".casefold():
        to_return = 2
    return to_return
