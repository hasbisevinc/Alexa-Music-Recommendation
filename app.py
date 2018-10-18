import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ASK_APPLICATION_ID = 'amzn1.ask.skill.4a1322fb-0be1-4aba-a683-8fac05f69696'
ASK_VERIFY_REQUESTS = True
ASK_VERIFY_TIMESTAMP_DEBUG = True


@ask.intent("music_recommendation")
def main_function():
    return dinner_recommendation()

	
@ask.intent("AMAZON.StopIntent")
def stop_function():
    return statement("See you tomorrow")

	
@ask.intent("AMAZON.CancelIntent")
def cancel_function():
    return statement("See you tomorrow")


@ask.launch
def launched():
    return dinner_recommendation()

@ask.session_ended
def session_ended():
    return "{}", 200

# --------------- Main handler ------------------
def lambda_handler(event, context):
    if event['session']['application']['applicationId'] != "amzn1.ask.skill.4a1322fb-0be1-4aba-a683-8fac05f69696":
        print("wrong app id")
        return ''
    print("event.session.application.applicationId=" +
          str(event['session']['application']['applicationId']))
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


# --------------- Response handler ------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    jj = {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    return app.response_class(json.dumps(jj), content_type='application/json')


# --------------- Events ------------------
def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "music_recommendation":
        return dinner_recommendation()


#--------------- App Functions ------------------------
def dinner_recommendation():
    session_attributes = {}
    card_title = "Music Recommendation"
    dinner = get_dinner()
    speech_output = "Here is a music recommendation for you. You can listen "+dinner
    reprompt_text = "Music recommendation is "+dinner
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_dinner():
    now = datetime.datetime.now()
    day = now.day
    return food_list[int(day)%9]


#---------------- Food List ----------------------------
#BURAYA_YENI_STRINGLER
food_list = ("Despacito by Luis Fonsi", "faded by alan walker", "Take Me To Church by Hozier", "Come with Me Now by KONGOS", "All of Me by John Legend", "Ride by twenty one pilots"
, "Imagine Dragons by Radioactive", "Do I Wanna Know by Arctic Monkeys", "Zombie by The Cranberries")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
        app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.4a1322fb-0be1-4aba-a683-8fac05f69696'
        app.config['ASK_VERIFY_REQUESTS'] = True
        app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

