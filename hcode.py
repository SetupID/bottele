#!/usr/bin/python3
#-*- visit : <heartscode.net/> -*-

import requests,telebot,time
from telebot import types
from bs4 import BeautifulSoup as bs
token = '<token-ur-boot>'
bot = telebot.TeleBot(token)
def golek(m,film,cid):
	result = {}
	s = 'https://kawanfilm21.org/?s='+film[6:]
	header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
	h2 = header.update({'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
	req = requests.get(s,headers=header).text
	scrap = bs(req,'html.parser')
	try:
		div = scrap.find('div',{'class': 'content-thumbnail text-center'})
		link = div.a.get('href')
		al = requests.get(link,headers=header).text #access link
		scrp = bs(al,'html.parser')
		id = scrp.find('div',{'id':'muvipro_player_content_id'}).get('data-id')
		d = {'action':'muvipro_player_content','tab':'player1','post_id':id}
		pos = requests.post('https://kawanfilm21.org/wp-admin/admin-ajax.php',headers=h2,data=d).text
		result['title'] = scrp.find('h1',{'class':'entry-title'}).get_text()
		result['description'] = scrp.find_all('p')[1].get_text()
		result['quality'] = scrp.find('span',{'class':'gmr-movie-quality'}).a.get_text()
		stream = bs(pos,'html.parser').iframe.get('src')
		result['streaming'] = 'https:'+stream
		gl = []  #get link
		for l in scrp.find_all('ul',{'class':'list-inline gmr-download-list clearfix'}):
			for a in l.find_all('a'):
				gl.append({a.get_text() : a.get('href')})
		result['download_link'] = gl
		hasil = f"title : {result['title']}\nDescription : {result['description']}\nLink Stream : {result['streaming']}"

		bot.reply_to(m,hasil)
		for i in result['download_link']:
			for k,v in i.items():
                        #print(abang(f"[{k}] : "+ijo(v)))
				msg = f".::Download Link::.\n[{k}] : "+v
				bot.send_message(cid,msg)
	except AttributeError:
		bot.reply_to(m,"oh sorry bos,i'cant find what u search :(")
		return True
@bot.message_handler(commands=['cari'])
def command_score(m):
    cid = m.chat.id
    golek(m,m.text,cid)

@bot.message_handler(commands=['start'])
def command_bisi(m):
    cid = m.chat.id 
    msg = "hi, thanks for starting me ! >//<\n"
    bot.send_message(cid, msg)
@bot.message_handler(commands=['help'])
def send_h(m):
	bot.reply_to(m,"for searching film u can use command /cari ex: /cari Iron Man")
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_join(m):
	bot.send_message(m.chat.id, f"Hi [{m.new_chat_member.username}](tg://user?id={m.new_chat_member.id}) nice to meet u >//<",parse_mode="Markdown")
bot.polling(none_stop=True)
while True:
    time.sleep(300) 
