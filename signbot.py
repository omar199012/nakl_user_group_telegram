from telethon.sync import TelegramClient
from telethon import events, Button
import json
import configparser
import logging
from t import *
import os
from phone_iso3166.country import *
import telethon

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']
client = telethon.TelegramClient('ownsession/signbot', api_id, api_hash) 

token = config['Token']['signbot']
#channel = config['App']['channel']
idbot =  int(token.split(':')[0])

client.start(bot_token=token)
client.connect()
dev = json.loads(config['App']['dev'])



check = [
            [Button.inline('تأكيد الحساب', "check")]
    ]
keyboard = [
                [Button.text("تسجيل حساب جديد", resize=True)],
            ]
@client.on(events.NewMessage())
async def main(event):
    chattt = await event.get_chat()
    if chattt.__class__.__name__ != 'User':
        return
        
    try:
        b = event.message.peer_id.channel_id
        b = f"-100{b}"
    except:
        pass

    ms_id = event.message.id
    text = event.raw_text.split("\n")[0]
    cleantext = event.raw_text
    fid = event.sender_id
    chat = event.chat_id
    ex = text.split("-")
    getdata = get(str(fid), "sql/cache_code.sqlite3") or 'None|None'
    data = getdata.split('|')
    if fid == idbot:
        return

    if fid not in dev:
        return

    if fid in dev:
        if text == 'c':
            await client.disconnect()
            return
    ban = read('data/ban.txt')
    ban = ban.split("\n")
    

    if str(fid) in ban:
        await event.reply('قد تم حظرك من البوت')
        return
# start
    resatart = [
                [Button.text("إلغاء العملية", resize=True)]
            ]

    sms = [
                [Button.inline('إضغط لإرسال الكود برسالة sms',"sms")]
            ]
  
    usersbot = read('data/memberssignbot.txt')
    usersbot = usersbot.split("\n")
    if str(fid) not in usersbot:
        file_append('data/memberssignbot.txt', str(fid) + "\n")  

    if fid in dev:
        exx = text.split(' ')
        if text == '/admin':
            luser = len(usersbot)
            allaccount = len(read('data/all.txt').split("\n")) - 1
            await event.reply(f"""
أهلا بك

عدد المشتركين : {luser}
عدد الأرقام في السيرفر : {allaccount}

لإرسال رسالة جماعية :
/send مرحبا بكم

عضوية
/pro id_user

إلغاء عضوية
/del id_user

تعيين رسالة اسعار الدول
/ms abc def.....
            """)

        if exx[0] == '/send':
            r = cleantext.replace('/send', '').replace("\n", 'BBBBBCCCC')
            await event.reply('جار الإرسالٍ')
            send_shell('loopsendsignbot.py', r)
        
        if exx[0] == '/ms':
            r = cleantext.replace('/ms ', '')
            file_put('ms.txt', r)
            await event.reply('تم الحفظ')
            return


        
        if exx[0] == '/pro' and exx[1] != '':
            put(str(exx[1]), 'pro', "sql/users.sqlite3")
            await event.reply('تم ترقية العضو')
            await client.send_message(int(exx[1]), "تمت ترقية حسابك")
            return

        if exx[0] == '/del' and exx[1] != '':
            put(str(exx[1]), 'None', "sql/users.sqlite3")
            await event.reply('تم إلغاء ترقية العضو')
            await client.send_message(int(exx[1]), "تمت إلغاء ترقية حسابك")
            return

        if exx[0] == '/ban':
            file_append('data/c.txt', exx[1]+',')
            await event.reply('تم')
            return
        if exx[0] == '/unban':
            r = read('data/c.txt')
            file_put('data/c.txt', r.replace(exx[1]+',', ''))
            await event.reply('تم')
            return

            
    if text == 'c' and fid in dev:
        await event.reply('ok')
        await client.disconnect()
    is_pro = get(str(fid), "sql/users.sqlite3")

        
    if text == '/start':
        await event.reply(f"""
مرحباً بك في بوت التسليم

        """, buttons=keyboard)
        return

    if text == 'إلغاء العملية':
        try:
            numbb = 237849234
            numb = numbb[-7:]
            try:
                os.remove('ses/'+data[1]+'.session')
            except:
                pass
            ev = read('data/numbers.txt').replace(numb, '')
            file_put('data/numbers.txt', ev)
        except:
            pass
        put(str(fid), 'None|None', "sql/cache_code.sqlite3")
        await event.reply('''
مرحباً بك في بوت التسليم

        ''', buttons=keyboard)
        return


    if text == 'تسجيل حساب جديد':
        put(str(fid), 'new|', "sql/cache_code.sqlite3")
        await event.reply(""""
ارسل الرقم مسبوقا بنداء الدولة
        
مثال :
+963951674345
        
        """ , buttons=resatart)
        return


    if text and data[0] == 'new':
        checknumber = read('data/numbers.txt').split("\n")
        text = '+' + text.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').replace('.', '').replace('+00', '').replace('+0', '').replace('+', '')
        fone = text.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').replace('.', '').replace('+00', '').replace('+0', '').replace('+', '')
        tel = text[-7:]
        if not is_int(fone):
            await event.reply('يرجى إرسال رقم صحيح')
            return
        if tel in checknumber:
            await event.reply('الرقم مسجل مسبقا!، ارسل رقم آخر…')
            return
        if is_pro != 'pro' and fid not in dev:
            if phone_country(fone) in read('data/c.txt').split(','):
                await event.reply('هذه الدولة محظورة، لا يمكنك تفعيل الأرقام من هذه الدولة..')
                return
        if cleantext[0] != '+':
            await event.reply("""
يرجى ارسال الرقم مسبوقا بنداء الدولة و +

مثال :
+967737669980
            """) 
            return
        await event.reply('انتظر قليلا جار المعالجة...')
        send_shell('python3', 'sign.py', 'new', text, str(fid))
    
    if text and data[0] == 'code':
        if not is_int(text):
            await event.reply('أرقام فقط...')
            return
        c = text.replace('a', '1').replace('b', '2').replace('c', '3').replace('d', '4').replace('e', '5').replace('f', '6').replace('g', '7').replace('h', '8').replace('i', '9').replace('j', '0')
        await event.reply('سيتم التحقق من الكود انتظر قليلا...')
        put(str(fid), 'addcode|'+c, "sql/cache_code.sqlite3")
        return

    if text and data[0] == 'pass':
        await event.reply('سيتم التحقق من كلمة المرور انتظر قليلا...')
        put(str(fid), 'addpass|'+text, "sql/cache_code.sqlite3")
        return

    if text == '/check' and data[0] == 'checking':
        await event.reply('انتظر قليلا...')
        return

    if text == '/check' and data[0] == 'check':
        #put(str(fid), 'checking|None', "sql/cache_code.sqlite3")
        await event.reply('سيتم التحقق من الحساب انتظر قليلا...')
        send_shell('python3', 'check.py', data[1], str(fid), data[2])
        #put(str(fid), 'addpass|'+text, "sql/cache_code.sqlite3")
        return



client.run_until_disconnected()
