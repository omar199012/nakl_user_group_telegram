import traceback
from pyrogram import Client
from pyrogram.raw import functions
import sys, os
import configparser
import asyncio
import logging
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch, UserBannedInChannel
try:
    from .t import get, put, is_tele
except:
    from t import get, put, is_tele




logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']

arg = sys.argv
command = arg[1]
ses = arg[2].split('.')[0]


async def apicodetelegramchannel():
    try:
        app = Client('ses/'+ses, api_id=api_id, api_hash=api_hash)
        cc = await app.connect()
        if command == 'check':
            try:
                await app.get_me()
                print('true')
            except:
                print('false : get_me()')
        await app.get_me()
    except Exception as d:
        er = str(d).replace('Telegram says: ', '').split(' - ')
        if er[0] in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
            try:
                os.remove('ses/'+ses+'.session')
            except:
                pass
        if command == 'check':
            print(er[0])

        print('false', d)
        cc = False
        return
    if not cc:
        print('false', 'hmmmm')
        return
    
    try:
        await app.invoke(functions.account.UpdateStatus(
            offline=False
        ))
    except:
        pass

    if command == 'join':
        url1 = is_tele(arg[3])[1]
        if arg[3] == arg[4]:
            url2 = url1
        else:
            url2 = is_tele(arg[4])[1]
        print(url1, url2)
        try:
            x1 = await app.join_chat(url1)
            if arg[3] == arg[4]:
                x2 = x1
            else:
                x2 = await app.join_chat(url2)
            print('true')
            print(x1.id)
            print(x2.id)
        except Exception as er:
            print('false', er)
            pass
    #await app.add_chat_members()
    if command == 'left':
        url1 = int(arg[3])
        url2 = int(arg[4])
        try:
            await app.leave_chat(url1)
            if arg[3] != arg[4]:
                await app.leave_chat(url2)
            print('true')
        except Exception as er:
            print('false', er)
            pass
        pass


    if command == 'getusers':
        ig = int(arg[3])
        ig2 = int(arg[4])
        #id = arg[4]
        users = ''
        users_list = []
        ok_user = []
        is_hidden = 'false'
        try: 
            geting2 = app.get_chat_members(ig2)#, filter=enums.ChatMembersFilter.RECENT)
            #print(geting)
            async for m2 in geting2:
                #print(m)
                #print(m.user.phone_number)
                if m2.user.id is not None:
                    users_list.append(m2.user.id)
                
            
            geting = app.get_chat_members(ig)#, filter=enums.ChatMembersFilter.RECENT)
            #print(geting)
            async for m in geting:
                #print(m)
                #print(m.user.phone_number)
                if m.user.id in users_list:
                    continue
                if m.user.username is not None:
                    #if m.user.username not in users_list:
                    users += "@"+str(m.user.username)+','
                else:
                    if m.user.phone_number is not None:
                        #if m.user.phone_number not in users_list:
                        users += "+"+str(m.user.phone_number)+','
                pass
            if len(users.split(',')) < 100:
                is_hidden = 'true'
                users = ''
                message_count = int(get('quality', 'sql/quality.sqlite3')) or 20000
                messages = app.get_chat_history(ig, limit=message_count)
                async for message in messages:
                    if message is None:
                        continue
                    #print(message
                    try:
                        if message.from_user.is_bot:
                            continue
                    except:
                        pass
                    try:
                        user_id = message.from_user.id
                        if user_id in users_list:
                            continue
                        #print(user_id)
                        if user_id in ok_user:
                            #print('continue')
                            continue

                        user = await app.get_chat(user_id)
                        #print(user.username)
                    except Exception as er:
                        #print(er)
                        continue

                    ok_user.append(user_id)
                    user_name_member =  user.username
                    '''if user_name_member is None:
                        user_name_member = user.phone_number'''
                        

                    if user_name_member is not None:# and user_name_member not in users_list:
                        #print(user_name_member)
                        users += "@"+str(user_name_member)+','
                        #ok_user.append(user_name_member)

            print('true')
            print(users)
            print(is_hidden)
        except Exception as er:
            #traceback.print_exc()
            print('false', er)

            pass

    if command == 'adduser':
        id_g = arg[3]
        user_for_add = arg[4]
        id = arg[5]

        added_ok = False
        flood_wait = False
        user_banned = False
        other_errors = False
        privacy_user = False
        user_too_much = False
        contact_required = False

        try:
            await app.add_chat_members(int(id_g), user_for_add)
            print('true', user_for_add)
            added_ok = True
        except FloodWait as e:
            print('FloodWait', user_for_add)
            flood_wait = True
            #added -= 1
        except PeerFlood as e:
            print('PeerFlood', user_for_add, ses)
            user_banned = True
            #added -= 1
            #banned_sessions.append(s)
        except UserBannedInChannel as e:
            print('PeerFlood', user_for_add, ses)
            user_banned = True
        except UserPrivacyRestricted as et:
            print('UserPrivacyRestricted', user_for_add)
            privacy_user = True
        except UserNotMutualContact as et:
            print('UserNotMutualContact', user_for_add)
            contact_required = True
        except UserChannelsTooMuch as et:
            print('UserChannelsTooMuch', user_for_add)
            user_too_much = True
        except Exception as er:
            print(er, 'all', user_for_add)
            other_errors = True
        

        if added_ok:
            put(id,int(get(id, "sql/added_ok.sqlite3")) + 1, "sql/added_ok.sqlite3")
        if flood_wait:
            put(id,int(get(id, "sql/flood_wait.sqlite3")) + 1, "sql/flood_wait.sqlite3")
        if user_banned:
            u_b = get(id, "sql/user_banned.sqlite3") or ''
            put(id,  u_b + ',' + ses, "sql/user_banned.sqlite3")
        if privacy_user:
            put(id,int(get(id, "sql/privacy_user.sqlite3")) + 1, "sql/privacy_user.sqlite3")
        if contact_required:
            put(id,int(get(id, "sql/contact_required.sqlite3")) + 1, "sql/contact_required.sqlite3")
        if user_too_much:
            put(id,int(get(id, "sql/user_too_much.sqlite3")) + 1, "sql/user_too_much.sqlite3")
        if other_errors:
            put(id,int(get(id, "sql/other_errors.sqlite3")) + 1, "sql/other_errors.sqlite3")


        '''return
        try:
            #await app.add_contact(user_add)
            await app.add_chat_members(int(id_g), user_add)
            print('true')
        except FloodWait as e:
            print('flood')
            print(ses)
        except PeerFlood as e:
            print('flood')
            print(ses)
        except UserPrivacyRestricted as et:
            #print()
            print('continue')
        except UserNotMutualContact as et:
            print('continue')
        except UserChannelsTooMuch as et:
            print('continue')
        except Exception as er:
            print(er, 'all')
        pass'''


    if command == 'send':
        ad = arg[3]
        ads = get(ad)
        user_for_send = arg[4]
        try:
            #await app.add_contact(user_add)
            await app.send_message(user_for_send, ads)
            print('true')
        except FloodWait as e:
            print('flood')
            #print(ses)
        except UserRestricted as et:
            #print()
            print('continue')
        except PeerFlood as et:
            print('flood')
        except Exception as er:
            print(er, 'all')
        pass


asyncio.get_event_loop().run_until_complete(apicodetelegramchannel())
