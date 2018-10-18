import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ASK_APPLICATION_ID = 'BURAYA_SKILL_ID'
ASK_VERIFY_REQUESTS = True
ASK_VERIFY_TIMESTAMP_DEBUG = True


@ask.intent("BURAYA_INTENT_NAME")
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
    if event['session']['application']['applicationId'] != "BURAYA_SKILL_ID":
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
    if intent_name == "BURAYA_INTENT_NAME":
        return dinner_recommendation()


#--------------- App Functions ------------------------
def dinner_recommendation():
    #BURAYA_KART_VE_SESLI_MESAJLAR_GELECEK
    session_attributes = {}
    card_title = "Daily Dinner Recommendation"
    dinner = get_dinner()
    speech_output = "Here is the daily dinner recommendation for you. You can cook "+dinner+" today."
    reprompt_text = "Today's dinner recommendation is "+dinner
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_dinner():
    now = datetime.datetime.now()
    day = now.day
    return food_list[int(day)%10]


#---------------- Food List ----------------------------
#BURAYA_YENI_STRINGLER
food_list = ("lemony chicken tenders", "herbed lemon cod", "turkey couscous", "veggie calzones", "chicken lazone", "savory chicken with rice"
, "turkey pesto fettucine", "balsamic garlic chicken", "slow cooker chicken with dill", "rotini with peas")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
	app.config['ASK_APPLICATION_ID'] = 'BURAYA_SKILL_ID'
	app.config['ASK_VERIFY_REQUESTS'] = True
	app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

