 # coding: utf-8
# Your code here!
from __future__ import print_function
import requests

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content':output
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
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "呼び出し"
    speech_output = "こんにちは、今のきになる通貨の値段を聞いてみましょう"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "こんにちは、今の気になる通貨の値段を聞いてみましょう"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "終わり"
    speech_output = "使ってくれてありがとう、また呼んでね "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def help():
    card_title="ヘルプ"
    a="仮想通貨のレートを取得するものになります。"
    b="例えば、ビットコインの価格を教えて。"
    c="ネムの値段は。"
    d="など聞いてみてください。"
    e="聞いたらスキルは終了しますのでまた呼んでくださいね！"
    speech_output=a+b+c+d+e
    should_end_session=False
    return build_response({},build_speechlet_response(
        card_title,speech_output,None,should_end_session))
        # TODO: write code...
        
def rate(coin):
    URL="https://coincheck.com/api/rate/"
    coin_price=requests.get(URL+coin+"_jpy")
    data=coin_price.json()
    rate_new=round(float(data['rate']),2)
    return str(rate_new)
    
def qash_jpy():
    URL='https://api.quoine.com/products'
    qash=requests.get(URL+"/50")
    data=qash.json()
    data2=float(data["last_traded_price"])
    qash_jpy=str(round(data2,2))
    return qash_jpy
    
def usd_jpy():
    URL="http://api.aoikujira.com/kawase/json/usd"
    ks=requests.get(URL)
    ks2=ks.json()
    data=round(float(ks2["JPY"]),2)
    return data
    
def binance(coinname):
    URL="https://api.binance.com/api/v3/ticker/price?symbol="
    coindata=requests.get(URL+coinname)
    cd2=coindata.json()
    cd3=round(float(cd2["price"]),2)
    cd4=round(cd3*usd_jpy(),2)
    return str(cd4)
def binance_btc(coinname):
    URL="https://api.binance.com/api/v3/ticker/price?symbol="
    coindata=requests.get(URL+coinname)
    cd2=coindata.json()
    cd3=float(cd2["price"])
    cd4=round(cd3*float(rate("btc")),2)
    return str(cd4)


    
def mona():
    URL="https://api.zaif.jp/api/1/last_price/mona_jpy"
    data1=requests.get(URL)
    data2=data1.json()
    mona1=round(float(data2["last_price"]),2)
    return str(mona1)
    
def speech(speech_output,card_title):
    reprompt_text =speech_output
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, True))
def set_coinprice_text(intent, session):
    card_title = "仮想通貨の値段"
    end="スキルを終了します！また呼んでくださいね！"
  #  session_attributes = {}
 #   should_end_session = True
    # スロットの中にlanguage変数があるか確認する
    if 'crypto' in intent['slots']:
        coin = len(intent['slots']['crypto'])
        if coin == 4:
            coinname=intent['slots']['crypto']['value']
            other=len(intent["slots"]["crypto"]["resolutions"]["resolutionsPerAuthority"][0])
        else:
            coinname="none"
            other=0
    
        if other ==3:
            othername=intent["slots"]["crypto"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
        else:
            othername="none"
        print(coinname)
        
        if coinname == 'ビットコイン' or othername=='ビットコイン':
            speech_output = '今のビットコインの価格はコインチェック参照で'+rate("btc")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'イーサリアム' or othername=='イーサリアム':
            speech_output = '今のイーサリアムの価格はコインチェック参照で'+rate("eth")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'イーサリアムクラシック' or othername=='イーサリアムクラシック':
            speech_output = '今のイーサリアムクラシックの価格はコインチェック参照で'+rate("etc")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'リスク' or othername=='リスク':
            speech_output = '今のリスクの価格はコインチェック参照で'+rate("lsk")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'ファクトム' or othername=='ファクトム':
            speech_output = '今のファクトムの価格はコインチェック参照で'+rate("fct")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'リップル' or othername=='リップル':
            speech_output = '今のリップルの価格はコインチェック参照で'+rate("xrp")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == "ネム" or othername == "ネム":
            speech_output = '今のネムの価格はコインチェック参照で'+rate("xem")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname == 'ライトコイン' or othername == 'ライトコイン':
            speech_output = '今のライトコインの価格はコインチェック参照で'+rate("ltc")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="ビットコインキャッシュ" or othername=="ビットコインキャッシュ":
            speech_output = '今のビットコインキャッシュの価格はコインチェック参照で'+rate("bch")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="リキッドキャッシュ" or othername=="リキッドキャッシュ":
            speech_output='今のリキッドキャッシュの価格はコイン参照で'+qash_jpy()+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="イーオス" or othername=="イーオス" :
            speech_output = '今のイーオスの価格はバイナンス参照で'+binance("EOSUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="トロン" or othername=="トロン":
            speech_output = '今のトロンの価格はバイナンス参照で'+binance("TRXUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="ネオ" or othername=="ネオ":
            speech_output = '今のネオの価格はバイナンス参照で'+binance("NEOUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="バイナンスコイン" or othername=="バイナンスコイン":
            speech_output = '今のバイナンスコインの価格はバイナンス参照で'+binance("BNBUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="ステラ" or othername=="ステラ":
            speech_output = '今のステラの価格はバイナンス参照で'+binance("XLMUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="アイオータ" or othername=="アイオータ":
            speech_output = '今のアイオータの価格はバイナンス参照で'+binance("IOTAUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="キュータム" or othername=="キュータム":
            speech_output = '今のキュータムの価格はバイナンス参照で'+binance("QTUMUSDT")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="パウンディエックス" or othername=="パウンディエックス":
            speech_output = '今のパウンディエックスの価格はバイナンス参照で'+binance_btc("NPXSBTC")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="ダッシュ" or othername=="ダッシュ":
            speech_output = '今のダッシュの価格はバイナンス参照で'+binance_btc("DASHBTC")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="モネロ" or othername=="モネロ":
            speech_output = '今のモネロの価格はバイナンス参照で'+binance_btc("XMRBTC")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="ジーキャッシュ" or othername=="ジーキャッシュ":
            speech_output = '今のジーキャッシュの価格はバイナンス参照で'+binance_btc("ZECBTC")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="オミセゴー" or othername=="オミセゴー":
            speech_output = '今のオミセゴーの価格はバイナンス参照で'+binance_btc("OMGBTC")+'円です。'+end
            return speech(speech_output,card_title)
        elif coinname=="モナコイン" or othername=="モナコイン":
            speech_output = '今のモナコインの価格はザイフ参照で'+mona()+'円です。'+end
            return speech(speech_output,card_title)
        else:
            return  help()
        


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()
    
def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
   # Dispatch to your skill's intent handlers
    if intent_name == "cryptoprice":
        return set_coinprice_text(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        
        
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
