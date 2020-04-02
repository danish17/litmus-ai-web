import numpy as np
from flask import Flask, request, render_template, jsonify
from src import predict as main_app

app = Flask(__name__, static_url_path="/static")

#Max Age Zeroing to serve fresh
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/404')
def error():
    return render_template('404.html')

@app.route('/form')
def feedback():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():

    title = request.form.get('title')
    text = request.form.get('text')
    text = text.replace("\r",'')
    text = text.replace("\n",'')

    api_key = "Fq0rdRKXqpPRoqyIoIN0oOyPpPo3WGtiuDMeRKwuwqM"

    return_vals = main_app.pipeline(title,text,api_key)

    vote_1 = return_vals[5]
    vote_2 = return_vals[6]
    vote_3 = return_vals[7]
    vote_4 = round(return_vals[8])

    title_emotion_resp = return_vals[0]
    text_emotion_resp = return_vals[1]
    intent_resp = return_vals[2]
    taxonomy = return_vals[3]
    sentiment_resp = return_vals[4]

    score = (0.8*vote_1 + vote_2 + 0.6*vote_3 + 0.8*vote_4)/3.2

    vote_1 = "fake" if vote_1 >= 0.4 else "true"
    vote_2 = "fake" if vote_2 >= 0.4 else "true"
    vote_3 = "fake" if vote_3 >= 0.4 else "true"
    vote_4 = "fake" if vote_4 >= 0.4 else "true"

    if(score >= 0.0 and score < 0.100):
        prediction = "true"
    elif(score >= 0.100 and score <0.400):
        prediction = "seems true"
    elif(score >= 0.400 and score <=0.600):
        prediction = "not sure"
    elif(score > 0.600 and score <0.800):
        prediction = "seems fake"
    elif(score >=0.800 and score <= 1):
        prediction = "fake"

    message = '''The model has classified this news as \"{}\". 
    The title of this news has  \"{}\" emotion, and the text has a \"{}\" emotion. 
    The text seems to be a \"{}\", and has been classified as \"{}\", and the title seems sentimentally \"{}\".'''.format(prediction,title_emotion_resp,text_emotion_resp,intent_resp,taxonomy,sentiment_resp)

    votes = '''Random Forest classified it as \"{}\", Logistic Regression classified it as \"{}\", Naive Bayes classified it as \"{}\".\n 
    The master neural network classified it as \"{}\"'''.format(vote_3,vote_2,vote_1,vote_4)

    alert = "Are you sure that this is a news article? The machine doesn't think so! The results may be unexpected." if intent_resp != "news" else " "

    return render_template('index.html',
                           prediction= prediction,
                           message = message,
                           votes= votes,
                           alert = alert,
                           title=title,
                           text=text)

if __name__ == '__main__':
    app.run(debug=True)
