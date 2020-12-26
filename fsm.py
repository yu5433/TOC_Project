from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_newest_page(self, event):
        text = event.message.text
        return text == "新文章"

    def on_enter_newest_page(self, event):
        send_text_message(event.reply_token, "請輸入欲搜尋分類")
        self.go_back()
    
    def is_going_to_favorite_page(self, event):
        text = event.message.text
        return text == "精選文章"

    def on_enter_newest_page(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入欲查看文章")
        self.go_back()
    

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