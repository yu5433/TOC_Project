import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()

#build a construction of state
machine = TocMachine(
    states=["user", "newest_page", "classical_page", "hottest_page", "creation_page", "experience_page", "translation_page"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "newest_page",
            "conditions": "is_going_to_newest_page",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "hottest_page",
            "conditions": "is_going_to_hottest_page",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "classical_page",
            "conditions": "is_going_to_classical_page",
        },
        {
            "trigger": "advance",
            "source": "newest_page",
            "dest": "experience_page",
            "conditions": "is_going_to_experience_page",
        },
        {
            "trigger": "advance",
            "source": "newest_page",
            "dest": "creation_page",
            "conditions": "is_going_to_creation_page",
        },
        {
            "trigger": "advance",
            "source": "newest_page",
            "dest": "translation_page",
            "conditions": "is_going_to_translation_page",
        },
        {"trigger": "go_back", "source": ["newest_page", "hottest_page", "classical_page", "experience_page", "creation_page", "translation_page"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

"""
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

"""
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if event.message.text == "fsm":
                send_image_message(event.reply_token, 'https://i.ibb.co/9HxHDnz/fsm.png?')
            if event.message.text == "幫助":
                if machine.state == "newest_page":
                    send_text_message(event.reply_token, "使用者欲觀看文章分類\n請輸入「經驗」、「創作」、「翻譯」")
                elif machine.state == "user":
                    send_text_message(event.reply_token, "輸入「新文章」查看近日新文章。\n輸入「熱門文章」查看近日爆文。\n輸入「經典文章」查看Marvel版精選好文。\n隨時輸入「fsm」可以查看狀態圖。")
            elif machine.state == 'user':
                send_text_message(event.reply_token, "輸入「新文章」查看近日新文章。\n輸入「熱門文章」查看近日爆文。\n輸入「經典文章」查看Marvel版精選好文。\n隨時輸入「fsm」可以查看狀態圖。")
            elif machine.state == 'newest_page':
                send_text_message(event.reply_token, "使用者欲觀看文章分類\n請輸入「經驗」、「創作」、「翻譯」")
            
            #send_text_message(event.reply_token, "Not Entering any State")
    
    return "OK"

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)

