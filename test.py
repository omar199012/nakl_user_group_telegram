import configparser
import traceback
from pyrogram import Client
import os

config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']

"""for i in os.listdir('ses'):
    try:
        app = Client('ses/'+i.split('.')[0], api_id=api_id, api_hash=api_hash, bot_token="5865245455:AAH6kx2w89zr7frlzJrfMuAG-IC75VZKsJM")

        app.start()
        chat_id = "@TESTER_DR_GR"
        message_count = 10
        messages = app.get_chat_history(chat_id, limit=message_count)
        for i in messages:
            print(i, encoding='utf-8')
        '''for message in messages:
            user_id = message.from_user.id
            user = app.get_chat_member(chat_id, user_id).user
            print(user)'''

        app.stop()
        break
    except Exception as er:
        traceback.print_exc()
        print(er)"""

from pyrogram import Client
for i in os.listdir('ses'):
    try:
        app = Client('ses/'+i.split('.')[0], api_id=api_id, api_hash=api_hash)
        app.start()
        chat_id = "@TESTER_DR_GR"
        message_count = 10
        messages = app.get_chat_history(chat_id, limit=message_count)
        for message in messages:
            user_id = message.from_user.id
            user = app.get_chat_member(chat_id, user_id).user
            print('@'+user.username)
        app.stop()
        break
    except Exception as er:
        print(er)