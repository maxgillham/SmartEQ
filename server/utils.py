"""
This module will be for utilities or helper functions to be used in the flask server
"""
import requests
from flask import jsonify
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import ast
import keys

# azure sdk for python
try:
    import azure.cognitiveservices.speech as speechsdk
except:
    print('The azure.cognitiveservices.speech module is not found')


def get_emotion(path_to_img) -> dict:
    """
    Get location of face, emotion rating for photo, given path to photo

    """
    subscription_key = keys.keys['face_key']
    image_data = open(path_to_img, "rb").read()
    url = "https://eastus.api.cognitive.microsoft.com/face/v1.0/detect"
    params = "?returnFaceAttributes=emotion"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
    response = requests.post(url+params, headers=headers, data=image_data)
    response.raise_for_status()
    unformatted = response.json()[0]['faceAttributes']['emotion']
    return get_highest_emotion(unformatted)


def get_highest_emotion(emotion_dict) -> dict:
    """
    Iterates over emotions in dictionary, returns the one with the highest match value,
    and also the second highest.
    """
    highest_value = 0
    second_value = 0
    highest_emotion = "No emotion"
    second_emotion = "No emotion"
    for emotion in emotion_dict:
        if emotion_dict[emotion] > highest_value:
            second_value = highest_value
            second_emotion = highest_emotion
            highest_value = emotion_dict[emotion]
            highest_emotion = emotion
    output = {}
    output['Emotion'] = highest_emotion
    output['Value'] = highest_value
    return output


def get_speech_text():
    """
    Listens to the mic of the user and converts what they said into text
    """
    speech_key, service_region = keys.keys['speech_key'], "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        output = json_format(result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        output = json_format("No speech could be recognized")
    else:
        output = json_format("Cancelled")
    output = json_format(result.text)
    return output


def get_sentiment(body):
    """
    Performs sentiment analysis on the text inputted in "body" using Microsoft Azure.
    Returns int between 0 and 1, closer to 1 is more positive, opposite is more negative.
    """
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': keys.keys['sent_key'],
    }
    params = urllib.parse.urlencode({
    })
    conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data


class SentimentRating():
    """
    This will be the overarching container class for our sentiment ratings, we'll use
    methods in here to return the current instance of sentiment rating, and also the overarching
    average rating. The overarching rating weighs the current sentiment more than previous sentiment.
    """
    def __init__(self):
        # init to neutral
        self.rating = 0.5

    def update_rating(self, latest_score) -> None:
        """
        Updates rating, weighing recent analyses more
        """
        self.rating = (0.2*self.rating + 0.8*latest_score)/1

    def get_rating(self) -> float:
        return self.rating


def json_format(text: str) -> str:
    """
    json formatting, to be used when feeding speech text to sentiment analysis
    """
    dicti = {"documents": [{"language": "en", "id": "1", "text": text}]}
    json_dict = json.dumps(dicti)
    return json_dict


def unwrap_sentiment(sentiment) -> float:
    """
    Unwraps the sentiment data from its many layers
    """
    return ast.literal_eval(sentiment.decode('utf-8'))["documents"][0]["score"]


def start_mic(sent_rating) -> float:
    """
    Used by sockets to start the mic, and also send ratings.
    """
    #sent = SentimentRating()
    speech_text = get_speech_text()
    if "No speech could be recognized" in speech_text:
        speech_text = json_format("butter")
    analysis = get_sentiment(speech_text)
    unwrapped = unwrap_sentiment(analysis)
    sent_rating.update_rating(unwrapped)
    #print('Average rating', sent.get_rating())
    return sent_rating.get_rating()


if __name__ == '__main__':
    #sent = SentimentRating()
    #for i in range(5): print(start_mic(sent))
    print(keys.keys)
