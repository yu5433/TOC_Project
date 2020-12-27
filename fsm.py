from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup
from utils import send_text_message
import requests
#crawling hottest article recently
def getPageNumber(content):
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5: endIndex]
    return int(pageNumber)+1
def findHotArtical(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    articleList = []
    for r_ent in soup.find_all(class_ = 'r-ent'):
        if (r_ent.find(class_ = 'hl f1')):
            hot = r_ent.find(class_='hl f1').text.strip()
            try:
                link = r_ent.find('a')['href']
                if link:
                    title = r_ent.find(class_ = 'title').text.strip()
                    url_link = 'http://www.ptt.cc'+link
                    articleList.append({'title':title, 'link':url_link})
            except Exception as e:
                print('noting', e)
    return articleList
def get_hot_href(url):
    hotArticle = []
    rs = requests.get(url)
    soup = BeautifulSoup(rs.text, 'html.parser')
    allPageURL = soup.select('.btn.wide')[1]['href']
    startPage = getPageNumber(allPageURL)
    indexList = []
    for page in range(startPage, startPage-4, -1):
        pageURL = 'http://www.ptt.cc/bbs/marvel'+'/index{}.html'.format(page)
        indexList.append(pageURL)
    while indexList:
        index = indexList.pop(0)
        res = requests.get(index)
        hotArticle += findHotArtical(res)
    content = ''
    for article in hotArticle:
        data = '{}\n{}\n'.format(article.get('title'), article.get('link'))
        content += data
    return content

#crawling recent article with type
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


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_newest_page(self, event):
        text = event.message.text
        return text == "新文章"

    def on_enter_newest_page(self, event):
        text = "使用者欲觀看文章分類\n請輸入「經驗」、「創作」、「翻譯」"
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
    def is_going_to_hottest_page(self, event):
        text = event.message.text
        return text == "熱門文章"
    def on_enter_hottest_page(self, event):
        content = "以下為近日熱門文章\n"
        url = "https://www.ptt.cc/bbs/marvel/index.html"
        content+=get_hot_href(url)
        content+="為您返回主畫面^__^\n"
        send_text_message(event.reply_token, content)
        self.go_back()
    def is_going_to_classical_page(self, event):
        text = event.message.text
        return text == "經典文章"
    def on_enter_classical_page(self, event):
        content = "以下為Marvel版精選文章\n"
        content += "[翻譯] Nosleep - 前房客留下了生存指南（1）\nhttps://www.ptt.cc/bbs/marvel/M.1566137420.A.7D1.html \n"
        content += "[翻譯] 日本怪談：深夜電臺廣播01\n https://www.ptt.cc/bbs/marvel/M.1577017556.A.2F5.html \n"
        content += "[翻譯] Nosleep-屍體化妝師\n https://www.ptt.cc/bbs/marvel/M.1578220152.A.886.html \n"
        content += "[翻譯] Nosleep-太空女孩\n https://www.ptt.cc/bbs/marvel/M.1579713441.A.EED.html \n"
        content += "[翻譯] Nosleep-我在網上徵到惡魔室友(1)\n https://www.ptt.cc/bbs/marvel/M.1543501533.A.E93.html \n"
        content += "[轉錄] 真人真事-不眠山\n https://www.ptt.cc/bbs/marvel/M.1446446701.A.FF1.html \n"
        content += "為您返回主畫面^__^\n"
        send_text_message(event.reply_token, content)        
        self.go_back()