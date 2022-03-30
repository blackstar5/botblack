import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
import requests
import urllib3
from Crypto.Cipher import AES
from hosyn_bot_file  import Bot,encryption
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def hasInsult(msg):
	swData = [False,None]
	for i in open("hosyn.bot.del.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                    bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def info_hosyn(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
            text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_ping(text,chat,bot):
    try:
        site = text[7:-1]
        jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
        text = str(jd)
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ping err')
    return True

def get_gold(text,chat,bot):
    try:
        r = json.loads(requests.get('https://www.wirexteam.ga/gold').text)
        change = str(r['data']['last_update'])
        r = r['gold']
        text = ''
        for o in r:
            text += o['name'] + ' : ' + o['nerkh_feli'] + '\n'
        text += '\n\nآخرین تغییر : ' + change
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + ' به پیوی شما ارسال شد', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_pa_na_pa(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/pa-na-pa/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz pa na pa err')
    return True

def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True

def get_zekr(text,chat,bot):
    try:                        
        jd = requests.get('http://api.codebazan.ir/zekr/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zekr err')
    return True

def get_zaman(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/time-date/?td=all').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zaman err')
    return True

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def sex(text,chat,bot):
    try:
        res = requests.get('https://s6.uupload.ir/files/screenshot_۲۰۲۲۰۲۱۲-۱۱۴۵۰۱_imdf.jpg')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')
    return True

def get_dialog(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dialog/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dialog err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        send_text = 'بای بای 🖖'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        send_text = 'سلام دوست عزیز به ' + group + ' خوش آمدی ❤ \n لطفا قوانین رو رعایت کن ✅'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('hosyn.bot.help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '!usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

g_usvl = ''
test_usvl = ''
auth = "rdzryjswfkhkathhdvzjtqhxberkttyk"
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        hosynAdmins = open('hosyn.bot.del.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            print('hosyn wolfam davish')
                            if text == '!start':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'با سلام به  بات خوش امدید برای دریافت دستورات کلمه دستورات را ارسال نمیایید',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'سلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ســــلــــام عــــشــــقم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                        
                                    
                            if text == 'عه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره بــــه مـــــولـــــا😐😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                                                                                 
                                    
                            if text == '😂' or text =='🤣🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کــــم بــــخـــنـــد اخــــرش مـــیـــگـــوزی گـــپـــو بـــه گـــا مـــیـــدی هـــا 🤣💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                  
                                    
                            if text == 'جون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'رون تــــــو کـــــون عـــــمـــــت😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                     
                                                                                    
                                    
                            if text == 'ارع':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آجـــــر پـــــاره😐🤣💫',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')   
                            if text == 'آفرین':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــــاکــــریــــم حــــاجــــی😁❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'بلک استار':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سازندمه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'افرین':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــــاکــــریــــم حــــاجــــی😁❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'خبی؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بــــخــــبــــی شــــمـــا تــــو خــــبـــــی🙁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'خبی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بــــخــــبــــی شــــمـــا تــــو خــــبـــــی🙁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == '🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'یــــعـــنـــی ایــــنــــقــــد خــــنـــده داش؟؟؟؟😐🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'چطوری؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خـــوبـــم تـــــو چــــطـــوری عـــــشــــقــــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                           
                            if text == 'چطوری':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خـــوبـــم تـــــو چــــطـــوری عـــــشــــقــــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'سازنده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Im a Black Star🖤⭐ @TOCREATE',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == '😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هـــــا چــــه مــــرگــــتــــه😐💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == '😐😂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــیـــزع خــــنــــده داری دیـــدی بـــگـــو مــــاعـــم بـــخـــنـــدیـــم😂❗️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'داش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جونم',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                         
                                                                             
                            if text == '😔':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عــهــهـــهــهــهــهــه چــرا نــاراحــتــی عـــشــقـــم چـــیـــزی شـــده😢کـــســـی چـــیـــزی گـــفـــتـــه بـــهـــت بـــگـــو شـــلــــوارش بـــکـــشـــم پـــایـــیـــن😢💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == ' بات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جـــونـــم عـــشـــقــــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'رل میخوام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــنـــم یــــه ســــاکــــه پــــر از پـــــول مــــخـــام🤣',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'مـــــنـــم یــــه ســــاکــــه پــــر از پـــــول مــــخـــام🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دلــــار بــــاشــــه بــــهـــتــــرــه🤣💫',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'GIF':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عجب گیفم داره🤣',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اره':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آجــــر پــــاره😐🤣💫️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'گیف':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عجب گیفم ک داری😐😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رل پی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بــیـــا بــا عـــمـــم رل بـــزن خـــوب بـــهـــت حـــال مــــیـــده هـــا پــــارش کـــن ولــــش کـــن❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                           
                            if text == 'داداش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'من داداش نیستم بات هستم',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'چخبرا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هـــیـــچ بــــمـــولـــا فــــقـــطـ دارم تـــــوســــطـ ســــازنــــدم پــــشـــرفــــت مــــیــــکــــنـــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'سلم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'الــــفـــشـــو خــــوردی حــــقــــیـــر😐💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'هعی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'روزگــار بــدیـــه...     گـــنـــجـــشـــک قـــنـــاری شـــده!    تـــخـــتــه چـــوب خـــیـــابــان دفـــتـــر یـــادگـــاری شـــده...🚶‍♂️️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'صلم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حـــقـــیــر مـــثـــل ادم ســـلـــام کــــن دا😐💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'صلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خـــیـــخ ایـــنـــو نـــیــگـــا بـــهـــش بــــخـــنـــدیـــن بـــلـــکـــه از ایــــن بــــه بــــعــــد درس ســـلــــام کــــرد🙁💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'ص':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــن ســاقـــیـــه ایـــنـــو زنـــده مـــیــــخــوام😐',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == '🤔':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فــکــر زنـــو بـــچـــتـــو مـــیــکــنـــی یـــا ایــنـــکــه تـــو شـــب زفـــاف چـــجـــوری پـــرده زنـــم بــــزنـــم؟🤣💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == '😈':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داشـــح مـــا هـــم شـــــاخـــیــم بـــمـــولــــا😹😈',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'ب کیرم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داش بــه هــســـتــه خـــرمـــات مـــیــگــی کــیــر؟🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'بکیرم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داش بــه هــســـتــه خـــرمـــات مـــیــگــی کــیــر؟🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                     
                            if text == 'حق':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ســتــاده مــبــارزه بــا حــق گــویــان: کــص نــگــو کــیــرم بــه نــصــلــه یــتــیــمــت🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == '🖕':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ایــنــو بــکــن کــص عــمــت تــا پــاره شــه جــیــگــر🤤💋 فــقــط شــرمــنــده نــخ و ســوزن نـــدارم نــمــیـــتـــونــم پـــارگــیــشــو بــدوزم و خــیــاطــی بــلــد نــیــســتــم😥',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == 'کص نگو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کــص گــفــتــنــی نــیــس کــه جــیــگــر کــص کــردنــیــه اوفــفــفــفــفــفــ🤤💋 ابـم اومـد بــیــا بــریــزم تــوت🤤💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                                                                                                    
                            if text == 'چرا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــون چ چــســـبــیــده بــه را😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                   
                            if text == 'چر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــون چ چــســـبــیــده بــه ر😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'چرا؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــون چ چــســـبــیــده بــه را😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                       
                            if text == 'چر؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چـــون چ چــســـبــیــده بــه ر😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                          
                            if text == '.':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــقــطـــه نـــفـــرس یـــتـــیـــم😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                      
                            if text == '😭':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گـــریـــه نـــکـــن زشـــتـــه بــــمــــولـــا🙁💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')               
                                                                                                                       
                            if text == '😒':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عــه بــچــه هـــا ایـــنم بـــلـــده قـــیـــافـــه بــــگـــره بـــهـــش بـــخــــنــدیـــن کــــیـــر نـــشــه بــــچـــم😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == '😏':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عــه بــچــه هـــا ایـــنم بـــلـــده قـــیـــافـــه بــــگـــره بـــهـــش بـــخــــنــدیـــن کــــیـــر نـــشــه بــــچـــم😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == 'کص ننت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'صــرم کــص نــنــت مــیــکــنــم پــصــرم نــنــه خــوش اصــتــایــل لــش  کــص نــنــت مــیــکــنــم پــصــرم مــادرحــراجــی نــنــتــو مــفــتــی گــایــیــدم کــص نــامــوصــت صــگ صــفــت کــص نــنــت بــشــع الــهــی حــرویــر خــر تــو کــص خــواهــرت  خــار لــش  خــارقـهــوه خــارکــونــی  خــار کــصــو  گــونــخــور  گــوخــوردی  خــار خــونــی مــمــه مــادرت دهــنــم  کــیــرم لــا مــمــه مــادرت  دیــشــب مــادرتــو از بــالــا تــا پــایــیــن مــثــل کــون اســرایــیــلــی لــیــص زدم✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                         
                            if text == '💋':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اه اه چــنــدش بــوســم نــکــن کــورونــا هــس مــیــخــوای بــدبــخــتــم کــنــی دیــوث پــولــم نـــدارم بـــرم دکـــتـــر😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                            
                            if text == 'تایپرم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حـــقـــیــر مــمــبــرو نـــیــگـــا کـــنـــن بـــهـــش یــــکـــم بـــخــنــدیـــن کـــیــر نـــشـــه بـــچـــم😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                          
                            if text == 'ب تخمم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'از داشــتــه هات یـــکـــم مایـــه بــزار شــاخ مـــجازی😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                     
                            if text == ' ربات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جانم؟',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                        
                            if text == 'شب خوش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'افــریــن بــورو بــخــواب دیــر وقــتــه شــبــکــه پــویــا ســاعــت 10 بــســتــه شــده تــو هــنــوز نــخــوابــیــدی😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                    
                            if text == 'ها':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هاعو کیر خر',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                               
                            if text == 'هان':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هانو زهر مار',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                                                                                                          
                            if text == 'صبح بخیر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'صــبــح بــخـــیــر عـــزیـــزم ایـــنـــشـــالــا امـــروز روز خــبــی داشــتــه بــاشــی😁❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                 
                            if text == 'پرده زن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ایــنــجــا هــمــه مــنــحــرفــه مــنــظــورت اشــتــبــاهــی مــیـگــیــرن مــنــظــور تــو پــرده پــنــجــره هــس اونــا پــرده کــوص مــیــفــهــمــن خــاک بـــر ســرشــون😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                         
                            if text == 'تلوزیون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خـــو بـــنــظــرت تــو تـــلــوزیـــن فــیــلـــم مــیــداد ســـازنــدم ایــنــجا چــیــکــار مــیــکــرد مــیــشــنــســت تــلــوزیــن مــیــدیــد دا😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                     
                            if text == 'هکرم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خــو اولــن بــکــیــرم بــعــدــشــم پــســره گــلــم مـــنـــو بـــهـــک مــنــتـــظـــرم😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                        
                            if text == 'کیر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اونــو بــکــن کــص عــمـــت تــا پــاره شــه جــیــگــر🙄💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                        
                            if text == 'ها':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اوم',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                                                                                                                        
                            if text == 'خر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اگه بگم خودتی ناراحت نمیشی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                   
                            if text == 'چخبر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ســلــامــتــی🙂💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'الو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مــگــه تــلــفــنــه مــیــگــی الــو😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'نه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ای نــکــمــه بــگــیــری😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'کسی نیس':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــه هــمــه حــولــا دارن تــو پــیــوی هــم دیــگــه ســکــس چــت مــیــکـــنــن😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'س':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــه هــمــه حــولــا دارن تــو پــیــوی هــم دیــگــه ســکــس چــت مــیــکـــنــن😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'کسی نیس؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــه هــمــه حــولــا دارن تــو پــیــوی هــم دــیــگه ســکــس چــت مــیــکــنــن😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چیکارم داری',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'ربات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جــونــم عــشــقــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'لین6ک گپ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://rubika.ir/joing/BJIACHJD0TFGQRDIJFKENHCSBMOFKYSI',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'لی6نک':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://rubika.ir/joing/BJIACHJD0TFGQRDIJFKENHCSBMOFKYSI',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'هیچی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اوکــی حــلــه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'داشمهه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                       
                            if text == 'شاخم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بن',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                                                                                                                        
                            if text == 'هوف':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اره حــرص بــوخــور خــیــلــی کــیــر شــدی😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                   
                            if text == 'زر نزن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عـــــمــــت بـــــزنــــه بــــرا مـــــن کـــــافـــــیـــــه جــــیـــگــــر😈✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'به تو چه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'تـــربـــــچـــه اگـــه کــــــون عــــمــــت بـــــزارن بـــــه مــــن چــــــه😂😈',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'خر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عــــمـــت صـــــدا مــــزنــــی جــــیگـــــر؟🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'سازندت کیه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' بلک استار',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'اوسکول':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داری عـــمـــت صــــدا مــــیـــزنــــی🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بات اوسکول':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هـــوشـــع اروم مـــن عـــمـــت نــیـــســم هـــا هــی اوســــکــــول صـــدام مـــیـــزنــــی🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بات خر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حـــتـــمـــا مـــنـــو بـــا عـــمـــت اشـــتـــبــاهــی گــرفـــتـــی جـــیـــگـــر🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'شعر بگو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــشــود فـــاش کـــســـی آنـــچـــه مــــیـــان مـــن و تـــوســتـــتــا اشـــارات نـــظــر نـــامـــه رســــان مــن و تـــوســـتــگـــوش کــن بـــا لــب خـــامـــوش ســخــن مـــی گــویـــم پـــاســـخــم گـــو بـــه نـــگــاهــی کـــه زبـــان مـــن و تـــوســـتـــروزگـــاری شـــد و کـــس مـــرد ره عـــشـــق نــدیــدحـــالــیــا چــشـــم جــهـــانــی نــگـــران مـــن و تـــوســتـــگــرچــه در خـــلـــوت راز دل مـــا کـــس نـــرســـیدهــــمــــه جــــا زمـــزمـــه ی عـــشـــق نـــهـــان مـــن و تــــوســـت',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'فعلا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کــجـــا مـــیـــری جـــیـــگـــر دلـــم بــــرات تـــنـــگ مــــیــــشـــــه😢💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بای':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کــجـــا مـــیـــری جـــیـــگـــر دلـــم بــــرات تـــنـــگ مــــیــــشـــــه😢💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'به من ج نمیده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خـــو لـــاقــــل ادم حـــســــابـــت نــــمیـــکـــنـــم دا جـــیـــگـــر😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'خدافظ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کــجـــا مـــیـــری جـــیـــگـــر دلـــم بــــرات تـــنـــگ مــــیــــشـــــه😢💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                                                                  
                            if text == 'عمه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــن گـــــوه مــــیــــخـــورم عــــمــــه تـــو بـــاشــــم تـــو ایــــن زمـــانـــه عــــمــــه هـــا بــــه گــــا رفــــتـــه هــــســــتـــن😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                                                                                                                        
                            if text == 'ننه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بـــه جـــون عــــمـــت تــــا اون حــــدی پــــیـــر نـــشـــدم کـــه نـــنـــه صــــدام بـــزنـــی🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                   
                            if text == 'کصشعر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مــگـــه کـــص هـــم شـــعـــر مـــیـــگـــه والـــا تـــازه مــیـــشـــنـــوم بــــرم از کــــص عــــمــــت بــــزنـــــم بـــــرام شـــــعـــــر بــــگــــه😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'ننه جون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گــــوه نــــخـــور مــــن در اون حــــدی پـــیـــر نــــشــــدم کــــه نـــنـــه صــــدام بــــزنــــی بــــورو عــــمــــت نــــنــــه صـــــدا بــــــزن🙄💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'کونی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عـــمـــتــو بـــا مـــن اشــــتــــبــــاهـــی نـــگــــیــــر جـــیــــگــــر😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بکصم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'از کـــوصــــت مــــایـــــع نـــــزار دیـــــدی تـــــوت گـــــزاشـــــتــــــــن جـــــیـــــغ زدی😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'چرا ج نمیده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خــــو لـــاقـــل ادم حــــســـابـــت نـــمــــیـــکــــنــــم دا😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'قدرت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'تــــو بــــاز رفــــتـــی بــــالــــا مـــمـــبـــر بــــچــــه بـــــیـــا پـــــایــــیـــــن ســــرمــــــون درد گـــــرف😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'به کصم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'از کـــوصــــت مــــایـــــع نـــــزار دیـــــدی تـــــوت گـــــزاشـــــتــــــــن جـــــیـــــغ زدی😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'جر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــــخـــوری یــــه وخ😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'خفه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نـــمـــیـــشــــم اگــــه مــــیــــتـــونــی بـــن بــــزن مـــنــــو😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'اهنگ بخون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'لــیــلــای مـــن دریـــای مـــن _ آســـوده در رویـــای مـــن ایـــن لـــحـــظـــه در هـــوای تـــو _ گـــم شــــده در صــــدای تـــومـــن عــــاشــــقـــم مـــــجـــنـــون تـــو _ گــــمـــگـــشـــتــه در بـــارون تـــو مــــجـــنـــون لـــیــــلـــی بــــی‌خــــبـــــر _ در کــــوچــــه هـــاي در بـــه در مـــســـت و پــــریــــشــــون و خـــــراب _ هــــر آرزو نــــقــــش بــــر آب شــــایــــد کــــه روزی عــــاقــــبــــت _ آروم بــــگــــیــــرد در دلـــــت',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'سیکتیر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پــــش عـــمــــت ســــیــــکــــتــــیــــر کــــنـــــم🤤💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'سیکتیر کن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پــــش عـــمــــت ســــیــــکــــتــــیــــر کــــنـــــم🤤💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                                                                  
                            if text == 'سیک کن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پــــش عـــمــــت ســــیــــکــــ کــــنـــــم🤤💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                            if text == 'باشه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آفــــریـــن بــــر تــــو پــــســــر یـــا دخـــتـــــر گــــلـــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'باش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آفــــریـــن بــــر تــــو پــــســــر یـــا دخـــتـــــر گــــلـــم😁💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'خخخخ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' نخند زشت میشی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'اصل بده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' ندارم',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'آره':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آجـــــر پـــــاره😐🤣💫️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == '😹':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گـــربــــه چـــیـــه خـــزو خــیــل😹💫️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == '❤':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جــــونـــنــــنــــنــــــــــ🤤♥💫️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'دعوا پی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بــــچـــه بـــیــــا پـــایـــــیــــن ســـرمــــون درد گــــرف😐😂🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'نمیخوام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'ب کیرم‌️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'صل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــث ادم ســــلــــام کــــن دا😐️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'زیر ابیا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دارن زیـــــر اب ســــکــــس انــــجـــــام مــــیــــدن کـــــــارشــــــون نـــــداشـــــتــــه بـــــاش🤣💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'اخطار':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بـــبــــیـــن کــــاربــــر گــــرامـــــی ایــــن یــــه اخــــطـــــار اســـــت اگــــه یــــه بـــــارم قـــــوانــــیــــن رعــــایـــــت نـــــکـــنــــی ریـــــم مــــیــــشی حـــــلــــه😈✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                       
                            if text == 'فدات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ایـــــنــــشــــــالـــا بــــشــــی😹❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                                                                                                                        
                            if text == 'گوه نخور':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مــــن تـــورو نـــمــــیـــخــــورم عـــنـــتـــر😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                   
                            if text == 'فال':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'تـــــو ایــــنــــده تـــــو کــــونـــت مــــیــــزارن😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'فال بگیر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'تـــــو ایــــنــــده تـــــو کــــونـــت مــــیــــزارن😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'شاعر میگه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'شـــــاعـــر مـــــال مـــنـــو مـــیــــخــــوره😹بــــه مــــن چــــه شــــــاعـــــر مـــــیــــگه😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'سل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــث ادم ســـــلـــــام کــــن حــــقــــیر😐️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بخورمت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــــمــــال داش🤣💫',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'سیلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره ســـــیــــــلــــات😐🤣😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'بیو تیکه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '▂▃▅▇█▓▒░ شایـב از نظر تو بـב باشم ولے بنظر خوـבم عالیم ░▒▓█▇▅▃▂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو عاشقانه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '•اُکسیژِنِع تویِ ریِع هآمـی لَنَتـیِع دوسـت داشتَنـی😽🌹:)♡',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو شاخ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خ‍‌ودت‍‌و پ‍‌ی‍‌دا ک‍‌ن‍‌‍ی خ‍‌ی‍‍‌ل‍‌ی‍‌ارو گ‍‌م م‍‌ی‍‌ک‍‌ن‍‌ی ای‍‌ن ش‍‌روعِ یہ م‍‌س‍‌ی‍‌ر ط‍‌ول‍‌ان‍‌ی‍ہ کہ ت‍‌ه‍‌ش ق‍‌ش‍‌ن‍‌گہ -! 🤍🩹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                                                                  
                            if text == 'بیو رفیق':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' ‏دردی که با دارو خوب نشه قَطعا با ❪بَغــــل❫ط خوب میشه🕊♥️رفیق🍭🍒★                                                                   𝓣𝓱𝓮 𝓹𝓪𝓲𝓷𝓽𝓱𝓪𝓽 𝓭𝓸𝓮𝓼𝓷𝓽 𝓰𝓸 𝓪𝔀𝓪𝔂 𝔀𝓲𝓽𝓱 𝓶𝓮𝓭𝓲𝓬𝓲𝓷𝓮 𝓲𝓽𝓵𝓵 𝓫𝓮 𝓰𝓸𝓷𝓮 𝔀𝓲𝓽𝓱 𝓱𝓾𝓰𝓼 .',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                                                                                                                        
                            if text == 'بیو خیانت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بۼۻ ڮڹ...ڲڕيۿ ڬڼ...ڋڨ ڮڼ...ٳمٲ بٳ آډماې بي اړزڜ دږڍ دڷ ڹڬڼ❥',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')         
                            if text == 'استارت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ربات روشن شد✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'بیو جذاب':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '༺ زندگے ات یـک قصـہ ایـست کـہ توسط یـک خداے خوب نوشتـہ شده! ༻',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'بیو فانتزی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ناشنوا باش وقتی کهـ به آرزوهای قشنگت میگن محالهـ💘🍀✨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو لاتی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'رفاقت ما مث پیازه🌱 لایه هاش به هم چسبیده😊 هرکی بخواد جدامون کنه اشکش در میاد💪',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو غمگین':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دودی کہ از سیگار بالا میره همون اشڪایی کہ قرار بود پایین بیوفتہ:)',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو شاد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'رفیـقِ خُل و چل نداشته باشی نصفِ عمرت بر فناست؛داشته باشی، کل عمرت🤪♥️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو لاکچری':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '☠♡نیستـــــ در دیـــــده مــــا منـــــزلتـــے دنیـــا رامـــــا نبینیܩ کســے را کــــہ نبینــــد مــــا را♡☠',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو پسرونه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داداش رسم لاتی💪🏼به چاقو زدنو عرق خوردن نیست 🔪🍻رسم لاتی بودن تو سه چیزه غیرت،ادب،معرفت،',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو دخترونه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🌼⃟▨꯭݊═╝مَِِـَِِـن َِِیَِِـَِِـه َِِدخَِِـَِِـتَِِـَِِـر َِِبَِِـَِِـی َِِاَِِعَِِـَِِـصَِِـَِِـاَِِب َِِمَِِـَِِـهَِِـَِِـربَِِـَِِـوَِِـَِِـنَِِـَِِـم َِِ 🌼⃟▨꯭݊═╝',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو مغرور':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اونجـایے ڪہ دیدے حرفت ارزش نداره؛ حـرفت رو عـوض نڪـن،جاتـو عوض ڪـن😏 ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو دلشکسته':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '༺ دنیـا دیـد من دقیـقا چـہ چیـزایـے رو دوست دارم،همونا رو ازم گرفـت ༻',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'بیو ساده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '👑پادشاه جهنم خودت باش نه کارگر بهشت دیگران👑',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')

                            if text == 'خوبی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــمــــنـــون شــــــمــــا خــــوبــــی؟؟؟؟',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            elif text.startswith('!nim http://') == True or text.startswith('!nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('!info @'):
                                tawd10 = Thread(target=info_hosyn, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('!search ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('!wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + '!wiki-s ['
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')
                            elif text.startswith('جوک'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('نام'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                            elif text.startswith('خاطره'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('دانستنی'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('په نه په'):
                                tawd24 = Thread(target=get_pa_na_pa, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('الکی'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('داستان'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('ذکر'):
                                tawd205 = Thread(target=get_zekr, args=(text, chat, bot,))
                                tawd205.start()
                            elif text.startswith('بیو'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!search-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                            elif text.startswith('ajab') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('!search-i ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('بن') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('ترجمه'):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('!myket-s ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('ویکی'):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('نرخ ارز'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('نرخ طلا'):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('پینگ'):
                                tawd21 = Thread(target=get_ping, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('دیالوگ'):
                                tawd215 = Thread(target=get_dialog, args=(text, chat, bot,))
                                tawd215.start()
                            elif text.startswith('!font ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('!font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('!whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('!vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('حدیث'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()
                            elif text.startswith('!weather ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('زمان') or msg.get("text").startswith("ساعت") or msg.get("text").startswith("تاریخ"):
                                tawd219 = Thread(target=get_zaman, args=(text, chat, bot,))
                                tawd219.start()
                            elif text.startswith('مستهجن'):
                                tawd27 = Thread(target=get_sex, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                            elif text.startswith("!add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'اضافه شد' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                            elif text.startswith('!math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                            elif text.startswith('شات'):
                                tawd16 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('بگو'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('دانش'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('!write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('!help'):
                                tawd38 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd38.start()
                            elif text.startswith('دستورات'):
                                tawd38 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd38.start()
                            elif text.startswith('!usvl_start') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_stop') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'usvl is stopped', chat['last_message']['message_id'])  
                            elif text.startswith('!usvl_test') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'test usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_untest') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'test usvl is stopped', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in hosynAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print('hosyn wolfam davsh‌')
    except:
        print('Hosyn wolfam‌')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
