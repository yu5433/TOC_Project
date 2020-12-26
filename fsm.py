from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup
from utils import send_text_message
import requests

def get_txt(num, url):
    content = ""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")
    for item in results:
        a_item = item.select_one("a")
        title = item.text
        if a_item:
            if "經驗" in title and num == 0:
                content += title + "https://www.ptt.cc"+ a_item.get('href')
            elif "創作" in title and num == 1:
                content += title + "https://www.ptt.cc"+ a_item.get('href')
            elif "翻譯" in title and num == 2:
                content += title + "https://www.ptt.cc"+ a_item.get('href')
    return content

# def get_cre(url):
#     content = ""
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     results = soup.select("div.title")
#     for item in results:
#         a_item = item.select_one("a")
#         title = item.text
#         if a_item:
#             if '經驗' in title:
#                 content += title + "https://www.ptt.cc"+ a_item.get('href')
#     return content

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
        url = "https://www.ptt.cc/bbs/marvel/index.html"
        content = "以下為搜尋到的內容："
        content += get_txt(0, url)
        for page in range(1,3):
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            url = next_page_url
            content += get_txt(0, url = url)
        send_text_message(event.reply_token, content) 
        self.go_back()

    def is_going_to_creation_page(self, event):
        text = event.message.text
        return text == "創作"
    def on_enter_creation_page(self, event):
        url = "https://www.ptt.cc/bbs/marvel/index.html"
        content = "以下為搜尋到的內容："
        content += get_txt(1, url)
        for page in range(1,3):
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            url = next_page_url
            content += get_txt(1, url = url)
        send_text_message(event.reply_token, content) 
        self.go_back()
    
    def is_going_to_translation_page(self, event):
        text = event.message.text
        return text == "翻譯"
    def on_enter_translation_page(self, event):
        url = "https://www.ptt.cc/bbs/marvel/index.html"
        content = "以下為搜尋到的內容："
        content += get_txt(2, url)
        for page in range(1,3):
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            url = next_page_url
            content += get_txt(2, url = url)
        send_text_message(event.reply_token, content) 
        self.go_back()

    def is_going_to_favorite_page(self, event):
        text = event.message.text
        return text == "精選文章"

    def on_enter_favorite_page(self, event):
        send_text_message(event.reply_token, "請輸入欲查看文章")
        self.go_back()
    