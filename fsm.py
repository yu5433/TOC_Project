from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup
from utils import send_text_message

import requests

def get_all_href(num, url):
    dict ={}
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")
    for item in results:
        a_item = item.select_one("a")
        title = item.text
        if a_item:
            if '經驗' in title and num == 0:
                dict[title] = 'https://www.ptt.cc'+ a_item.get('href')
    return dict


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_newest_page(self, event):
        text = event.message.text
        return text == "新文章"

    def on_enter_newest_page(self, event):
        text = "使用者欲觀看文章分類\n請輸入\"經驗\"、\"創作\"、\"翻譯\""
        send_text_message(event.reply_token, text) 

    def is_going_to_experience_page(self, event):
        text = event.message.text
        return text == "經驗"
    def on_enter_experience_page(self, event):
        #send_text_message(event.reply_token, "trigger experience")
        url = "https://www.ptt.cc/bbs/marvel/index.html"
        dict.update(get_all_href(0, url))
        for page in range(1,3):
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            url = next_page_url
            dict.update(get_all_href(0, url = url))
        send_text_message(event.reply_token, dict) 

    def is_going_to_favorite_page(self, event):
        text = event.message.text
        return text == "精選文章"

    def on_enter_favorite_page(self, event):
        send_text_message(event.reply_token, "請輸入欲查看文章")
    

"""
    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()
"""