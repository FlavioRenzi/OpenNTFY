import asyncio
import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Button
from textual.containers import Center, Horizontal
from telegram import Bot


class TokenSet(App):
    CSS = """
    #token {
        width: 70%;
    }
    #buttons {
        width: 70%;
    }
    #buttons > * {
        width: 50%;
    }
    """
    def compose(self) -> ComposeResult:
        with Center(): yield Label("Insert your Telegram Bot Token")
        with Center(): yield Input(placeholder="Telegram Bot Token", id="token")
        with Center(): yield Label("Do you know your chat id?")
        with Center():
            with Horizontal(id="buttons"):
                yield Button("Yes", id="yes", variant="primary")
                yield Button("No", id="no", variant="error")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit((self.query_one('#token').value, event.button.id))

class ChatIdSet(App):
    CSS = """
    #chatid {
        width: 70%;
    }
    """
    def compose(self) -> ComposeResult:
        with Center(): yield Label("Insert your chat id")
        with Center(): yield Input(placeholder="Chat id", id="chatid")
        with Center(): yield Button("Confirm", id="confirm", variant="primary")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(self.query_one('#chatid').value)
        
class GetChatId(App):
    def compose(self) -> ComposeResult:
        with Center(): yield Label("Send a message to your bot")
        with Center(): yield Label("Press the button below when you're done")
        with Center(): yield Button("Done", id="done", variant="primary")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit()

class CheckId(App):
    def __init__(self,username: str = "", chat_id: int = 0):
        self.username = username
        self.chat_id = chat_id
        super().__init__()
    CSS = """
    #buttons {
        width: 70%;
    }
    #buttons > * {
        width: 50%;
    }
    """
    def compose(self) -> ComposeResult:
        with Center(): yield Label("You are:")
        with Center(): yield Label("@"+self.username+" chat id: "+str(self.chat_id))
        with Center(): yield Label("Is that you?")
        with Center(): 
            with Horizontal(id="buttons"):
                yield Button("Yes", id="yes", variant="primary")
                yield Button("No", id="no", variant="error")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

class TestBot(App):
    def compose(self) -> ComposeResult:
        with Center(): yield Label("Send a test message to your bot")
        with Center(): yield Button("Send test message", id="send", variant="primary")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit()
class FinalCheck(App):
    CSS = """
    #buttons {
        width: 70%;
    }
    #buttons > * {
        width: 50%;
    }
    """
    def compose(self) -> ComposeResult:
        with Center(): yield Label("Do you recieve the message?")
        with Center(): 
            with Horizontal(id="buttons"):
                yield Button("Yes", id="yes", variant="primary")
                yield Button("No", id="no", variant="error")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

def run(config_path: str):
    loop = asyncio.get_event_loop()
    finished = False
    while not finished:
        token, known_chatid = TokenSet().run()
        bot = Bot(token)
        if known_chatid == "yes":
            chat_id = ChatIdSet().run()
        else:
            getted_id = False
            while not getted_id:
                GetChatId().run()
                up = loop.run_until_complete(bot.get_updates(offset=-1, limit=1, timeout=0))
                chat_id = up[0]['message']['chat']['id']
                username = up[0]['message']['chat']['username']
                getted_id = True if CheckId(username=username,chat_id=chat_id).run() == "yes" else False
        TestBot().run()

        loop.run_until_complete(bot.send_message(chat_id=chat_id, text="Test message"))
        
        finished = True if FinalCheck().run() == "yes" else False
    #print(token, known_chatid)
    #(os.path.expanduser('~')+'/.config/OpenNTFY/config.json'))
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as config_file:
            config = {'TELEGRAM_TOKEN': token, 'TELEGRAM_CHAT_ID': chat_id}
            config_file.write(json.dumps(config))
    else:
        with open(config_path, 'rw') as config_file:
            config = json.load(config_file)
            config.update({'TELEGRAM_TOKEN': token, 'TELEGRAM_CHAT_ID': chat_id})
            config_file.write(json.dumps(config))
    
if __name__ == "__main__":
    run()