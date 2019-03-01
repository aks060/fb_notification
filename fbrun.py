import requests
import time
import subprocess
import sqlite3
import os
from bs4 import BeautifulSoup

fl=open('test.html', 'w+')
frndshow=None
mssgshow=None
notifyshow=None
yourname='aks060'
s = requests.session()
addr='/home/root/.mozilla/firefox/'		#Your Firefox directory address

def setup():
	dir=str(os.popen('ls -d '+addr+'*/').read())
	dir=dir.split()
	reqdir=max(dir, key=len).split('/')
	reqdir=reqdir[-2]
	ckadd=addr+reqdir+'/cookies.sqlite'
	os.popen('cp '+ckadd+' /tmp/')
	time.sleep(1)
	ckadd='/tmp/cookies.sqlite' 
	conn=sqlite3.connect(ckadd)
	cur=conn.execute('SELECT * FROM moz_cookies where baseDomain LIKE ?', ('%'+'facebook%',))
	for row in cur:
		my_cookie = {"name":str(row[3]),"value":str(row[4]),"domain":str(row[5]),"path":str(row[6])}
		s.cookies.set(**my_cookie)
	print('Working with '+str(len(s.cookies))+' values...')

setup()	

while 1:
	rtemp=s.get('https://www.facebook.com/friends/requests')
	cont=str(rtemp.content.decode())

	try:
	 	ind=cont.index('Respond to Your ')
	 	minind=cont.index(' Friend Request')
	 	frnd=int(cont[ind+16:minind])
	except Exception as e:
	 	frnd=0
	soup =BeautifulSoup(cont, 'html.parser')
	mssg=soup.find("span", {"id": "mercurymessagesCountValue"}).text
	notify=soup.find("span", {"id": "notificationsCountValue"}).text

	if int(mssg)>0 and (mssgshow is None or mssgshow!=mssg):
		showmssg=yourname+' You have '+mssg+' new messages'
		os.system('notify-send -u critical "'+showmssg+'"')
		os.system('spd-say "'+showmssg+'"')
		time.sleep(5)
	mssgshow=mssg

	if int(notify)>0 and (notifyshow is None or notifyshow!=notify):
		showmssg=yourname+' You have '+notify+' new notifications'
		os.system('notify-send -u critical "'+showmssg+'"')
		os.system('spd-say "'+showmssg+'"')
		time.sleep(5)
	notifyshow=notify
	
	if int(frnd)>0 and (frndshow is None or frndshow!=frnd):
		showmssg=yourname+' You have '+frnd+' new friend requests'
		os.system('notify-send -u critical "'+showmssg+'"')
		os.system('spd-say "'+showmssg+'"')
		time.sleep(5)
	frndshow=frnd
	
	time.sleep(1)
