import asyncio
import logging
from telethon.sync import TelegramClient
import time
from t import *
import sys, os, random, requests, configparser, json
try:
    from .t import *
except:
    pass
config = configparser.ConfigParser() 
config.read("config.ini")
from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch


logging.getLogger("pyrogram").setLevel(logging.WARNING)

token = config['Token']['mybot']
api_id = config['App']['id']
api_hash = config['App']['hash']

arg = sys.argv
command = arg[1]


def sendms(chat_id, text):
    URL = "https://api.telegram.org/bot"+token+"/sendmessage"
    PARAMS = {'chat_id': chat_id, 'text': text}
    requests.get(url=URL, params=PARAMS)

id = randtext(6)
sessions = os.listdir('ses')
random.shuffle(sessions)

count = len(sessions)

if command == 'join':
    num = int(arg[2])
    user = arg[3]
    url1 = arg[4]
    url2 = arg[5]
    num_of_ac = arg[6]
    times = arg[7]
    put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times, "sql/cache2.sqlite3")
    join = 0
    for i in sessions:
        if join == num:
            break
        
        ses = i.split('.')[0]
        c = 'false'
        c = send_command('add_user.py', 'join', i, url1, url2)
        print(c)
        sp = c.split("\n")
        if 'true' in sp:
            if sp[0] == 'true':
                id1 = sp[1]
                id2 = sp[2]
            else:
                id1 = sp[2]
                id2 = sp[3]
            join += 1
            g = get(id)
            for_leave = ses+"|"+id1+"|"+id2
            if g == 0:
                put(id, for_leave+',')
            else:
                ss = get(id)
                put(id, ss+for_leave+',')
        else:
            pass
    sendms(user, f"""
✅ :: تم تنفيذ أمر اشتراك الحسابات 

🔰 :: عدد الحسابات المشتركة : {join}
🚶‍♂:: لمغادرة الحسابات : 
/left_{id}

🛎 :: يتم الآن جلب الأعضاء المجموعة وتخزينها

#ملاحظة يتم اكتشاف المجموعات التي أخفت الأعضاء تلقائيا 😎
    """)
    get_sessions = str(get(id)).split(',')
    for ii in get_sessions:
        if ii == '':
            continue
        spl = ii.split('|')
        s = spl[0]
        ig = spl[1]
        ig2 = spl[2]
        c2 = send_command('add_user.py', 'getusers', s, ig, ig2)
        ex = c2.split("\n")
        if ex[2] == 'true':
            is_hidden = 'نعم'
        else:
            is_hidden = 'لا'
        if 'true' in ex:
            put(id, ex[1], 'sql/users.sqlite3')
            counts = len(str(ex[1]).split(','))
            sendms(user, f"""
✅ :: تم تنفيذ أمر جلب الأعضاء 

👥 :: عدد الأعضاء : {counts}
👀 :: الأعضاء مخفية : {is_hidden}

☑️ :: لبدء النقل :
/begin_{id}
    """)
            break



if command == 'left':
    user = arg[2]
    id = arg[3]
    get_sessions = str(get(id)).split(',')
    #print(get_sessions)
    for ii in get_sessions:
        if ii == '':
            continue
        spl = ii.split('|')
        s = spl[0]
        ig = spl[1]
        ig2 = spl[2]
        c2 = send_command('add_user.py', 'left', s, ig, ig2)
    sendms(user, f"""
تم المغادرة بنجاح..
""")
    pass

if command == 'begin':
    ban_ac = []
    p_user = 0
    user = arg[2]
    id = arg[3]
    try:
        client = TelegramClient('ownsession/'+id, api_id, api_hash)
        client.start(bot_token=token)
        ms = client.send_message(int(user), 'بدأ النقل سأخبرك بهذه الرسالة جميع التفاصيل..')
    except Exception as er:
        print(er, 'Error Bot')
        pass
    get_sessions = str(get(id)).split(',')
    #put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times, "sql/cache2.sqlite3")
    get_info = str(get(id, "sql/cache2.sqlite3")).split("|")
    id_g = get_info[3]
    num_of_ac = get_info[4]
    times = get_info[5]
    all_users = str(get(id, 'sql/users.sqlite3')).split(',')
    dis = False
    added = 0
    added_ok = 0

    try:
        user_banned = get(id, "sql/user_banned.sqlite3").split(',')
    except:
        user_banned = []
    
    while True:
        stop = False
        for ii in get_sessions:
            if added < 111:
                added +=1
                continue
            is_stop = get(id, "sql/stop.sqlite3")
            if is_stop == 'stop':
                stop = True
                break

            if ii == '':
                continue
            spl = ii.split('|')
            s = spl[0]
            ig = spl[1]
            ig2 = spl[2]
        
            if s in user_banned:
                continue
            
            try:
                user_for_add = all_users[added]
            except:
                break
            add = send_command('add_user.py', 'adduser', s, ig2, user_for_add, id)
            print(add) 
            added += 1
            if added_ok == int(num_of_ac):
                dis = True
                break
            time.sleep(int(times))
            '''try:

                app = Client('ses/'+s, api_id=api_id, api_hash=api_hash)
                cc = app.connect()

                try:
                    app.add_chat_members(int(ig2), user_for_add)
                    print('true')
                    added_ok += 1
                except FloodWait as e:
                    print('FloodWait', user_for_add)
                    flood_wait += 1
                    #added -= 1
                except PeerFlood as e:
                    print('PeerFlood', user_for_add, s)
                    user_banned += 1
                    #added -= 1
                    banned_sessions.append(s)
                except UserPrivacyRestricted as et:
                    print('UserPrivacyRestricted', user_for_add)
                    privacy_user += 1
                except UserNotMutualContact as et:
                    print('UserNotMutualContact', user_for_add)
                    contact_required += 1
                except UserChannelsTooMuch as et:
                    print('UserChannelsTooMuch', user_for_add)
                    user_too_much += 1 
                except Exception as er:
                    print(er, 'all', user_for_add)
                    other_errors += 1
                
                app.disconnect()
            except Exception as d:
                er = str(d).replace('Telegram says: ', '').split(' - ')
                print(d)
                if er[0] in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
                    try:
                        os.remove('ses/'+s+'.session')
                    except:
                        pass

                pass'''

        
        added_ok = int(get(id, "sql/added_ok.sqlite3"))
        flood_wait = int(get(id, "sql/flood_wait.sqlite3"))
        try:
            user_banned = get(id, "sql/user_banned.sqlite3").split(',')
        except:
            user_banned = []
        other_errors = int(get(id, "sql/other_errors.sqlite3"))
        privacy_user = int(get(id, "sql/privacy_user.sqlite3"))
        user_too_much = int(get(id, "sql/user_too_much.sqlite3"))
        contact_required = int(get(id, "sql/contact_required.sqlite3"))
        try:
            client.edit_message(ms, f"""
📮 :: العدد الكلي : {len(all_users)}
♻️ :: وصل إلى العدد : {added}

✅ :: تم نقل حتى الآن : {added_ok}

❌ :: أسباب عدم نجاح نقل بعض الأعضاء.. 

🧾 :: أعدادات الخصوصية : {privacy_user}
❗️ :: المستخدم ليس من جهات اتصالك : {contact_required}
🔕 :: المستخدم موجود في مجموعات كثيرة : {user_too_much}
🖌 :: أسباب أخرى : {other_errors}
🕒 :: حسابات محظورة مؤقتا : {flood_wait}
🚫 :: حسابات محظورة دائما : {len(user_banned)}

🛜 :: لإيقاف العملية :
/stop_{id}
    """)
        except: 
            pass
        if dis or stop:
            client.edit_message(ms, f"""
انتهى النقل..

📮 :: العدد الكلي : {len(all_users)}
♻️ :: وصل إلى العدد : {added}

✅ :: تم نقل : {added_ok}

❌ :: أسباب عدم نجاح نقل بعض الأعضاء.. 

🧾 :: أعدادات الخصوصية : {privacy_user}
❗️ :: المستخدم ليس من جهات اتصالك : {contact_required}
🔕 :: المستخدم موجود في مجموعات كثيرة : {user_too_much}
🖌 :: أسباب أخرى : {other_errors}
🕒 :: حسابات محظورة مؤقتا : {flood_wait}
🚫 :: حسابات محظورة دائما : {len(user_banned)}
"""+randtext(3))
            client.disconnect()
            break


if command == 'check':
    ok = 0
    er = ''
    user = arg[2]
    for i in os.listdir('ses'):
        add = send_command('add_user.py', 'check', i)
        exp = add.split("\n")
        if 'true' in exp:
            ok +=1
        else:
            if er not in er.split("\n"):
                er += exp[0]+"\n"
        pass
    
    sendms(user, f"""
انتهى الفحص..

عدد الحسابات الكلي : {len(os.listdir('ses'))}

عدد الحسابات السليمة : {ok}

""")
