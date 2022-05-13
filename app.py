import os
import random
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    txt = event.message.text
    txtArr = txt.split()
    # try:
    #     traindata = scraping.get_traindata(txtArr[0], txtArr[1])
    #     replyText = ""
    #     # msg = f"「{event.message.text}」ですか？ ちょっとよくわかりませんね…"
    #     if traindata[0] == -1:
    #         replyText = "正しく検索できませんでした"
    #     elif traindata[1] == -2:
    #         replyText = "乗り換えが発生していないか、確認してください"
    #     else:
    #         replyText = traindata
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text=replyText))
    # except Exception as e:
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text="error:"+str(e)))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=txt))


@handler.add(MessageEvent, message=LocationMessage)
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


@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    msg = "いいスタンプですね！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


@handler.default()
def default(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="その形式の入力には対応していません"))
    print(event)


if __name__ == "__main__":
    app.run()
