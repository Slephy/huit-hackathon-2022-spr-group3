import os
import random
import string
import datetime as dt
from flask import Flask, request, abort
from geopy.distance import geodesic
import scraping

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    LocationMessage,
    StickerMessage,
)

# (緯度, 経度)
TokyoStation = (35.681382, 139.76608399999998)
NagoyaStation = (35.170915, 136.881537)

global_test_num = 0

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


def makeTrainResult(data, event):  # 取得したデータから何かしらをユーザに返す関数(テキスト?リッチメニュー?)
    # datetime debug
    try:
        departureTimes, arrivalTimes, trainDescriptions, prices = data

    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("error:データが正しく受け取られませんでした。"+str(e)))

    txtArr = []
    order = ["先発", "次発", "次次発"]
    textTemplate = \
        """[{0}]
{1}
{2} ---> {3}
{4}"""
    for i in range(3):
        txt = textTemplate.format(
            order[i], trainDescriptions[i], departureTimes[i], arrivalTimes[i], prices[i])
        txtArr.append(txt)
    return txtArr


# メッセージを受け取った時のイベント
@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    txt = event.message.text
    txtArr = txt.split()
    replyTexts = []
    line_bot_api.push_message(
        event.source.user_id, TextSendMessage(text="検索中です..."))
    try:
        status, trainData, tsuukaData = scraping.get_traindata(
            txtArr[0], txtArr[1])
        if status == -1:
            replyTexts.append("正しく検索できませんでした")
        elif status == -2:
            replyTexts.append("乗り換えが発生していないか、確認してください")
        else:
            replyTexts = makeTrainResult(trainData, event)
    except Exception as e:
        # 例外
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("error:", str(e)))
    # 成功
    replyTexts = [TextSendMessage(text=txt) for txt in replyTexts]
    line_bot_api.reply_message(event.reply_token, replyTexts)


# 位置情報を受け取った時のイベント
@ handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    msgs = []
    msg_pos = (event.message.latitude, event.message.longitude)
    msg = f"緯度:{msg_pos[0]}、経度:{msg_pos[1]}ですね！特定しました！"
    msgs.append(TextSendMessage(text=msg))

    dist = geodesic(TokyoStation, msg_pos).km
    if(dist > 0.5):
        msg = f"僕の家との距離は{dist}kmだね！"
        msgs.append(TextSendMessage(text=msg))

    else:
        msg = "ってあれ？これ僕の家のすぐ近くじゃん！？"
        msgs.append(TextSendMessage(text=msg))
        msg = "そうだよ、僕の家は東京駅なんだ…。どうしてわかったの？"
        msgs.append(TextSendMessage(text=msg))

    line_bot_api.reply_message(event.reply_token, msgs)


# スタンプを受け取った時のイベント
@ handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    global global_test_num
    global_test_num += 1
    msg = str(global_test_num)
    # msg = "いいスタンプですね！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


# 上記以外のものを受け取ったときのイベント（画像など）
@ handler.default()
def default(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="その形式の入力には対応していません"))
    print(event)


if __name__ == "__main__":
    app.run()
