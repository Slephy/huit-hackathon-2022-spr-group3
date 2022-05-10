import os, random
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    LocationMessage,
    StickerMessage,
)

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
    msg = f"「{event.message.text}」ですか？ ちょっとよくわかりませんね…"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    msg = "これは位置情報ですか？ ちょっとよくわかりませんね…"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    msg = "これはスタンプですか？ ちょっとよくわかりませんね…"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))



@handler.default()
def default(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="その形式の入力には対応していません"))
    print(event)

    


if __name__ == "__main__":
    app.run()