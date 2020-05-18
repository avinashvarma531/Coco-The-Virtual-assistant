import speech_recognition as sr
from tasks.personality import *
from tasks.automate import *
from datetime import datetime 
from time import sleep
import pyttsx3 as tts
import os
from random import choice
import smtplib
from email.message import EmailMessage
import concurrent.futures

#List of commands
COMMANDS=[
	{
		'acceptance':['ok','yeah','sure','yes'],
		'confirmations':['yes','yeah','haa','yup','yes boss'],
		'acks':['done','finished','completed'],
		'disagree':['no','never','not ok'],
		'gratitude':['thanks','thank you','thank you so much'],
		'gratitude-reply':['no mention.','anything for you','you are welcome','it\'s ok']

	}	
]

#List of wakeup calls
wakeup=['hey coco','wake up','coco']


engine=tts.init()								#configuration of text to speech
engine.setProperty('rate',145)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

"""This function is for the assistant to talk"""
def talk( audio):
	print(audio)
	engine.say(audio)
	engine.runAndWait()

def addName( name):
	os.environ.put('MY_NAME',name)
	talk('Name added.')

"""listen functions which listens to the user voice for command recognition"""
def listen(r):
	#talk('Waiting for your command.')
	with sr.Microphone() as src:
		r.adjust_for_ambient_noise(src,duration=1)
		while True:
			print('listening...')
			try:
				audio=r.listen(src,timeout=5)
				with concurrent.futures.ThreadPoolExecutor() as exe:
						f=exe.submit(r.recognize_google,audio)
				print('recognizing..')
				cmmd=f.result()
				print(cmmd)
				return cmmd
			except KeyboardInterrupt:
				exit()
			except Exception as e:
				print(e)
				continue

"""Emailing a person"""	
def emailing(r):
	
	def send_email( to, sub, body):
		talk('Sending email to '+to)
		Email_id='[YOUR_GMAIL-ID]'
		Email_pwd='[YOUR_GMAIL-PWD]'
		msg=EmailMessage()
		msg['From']=Email_id
		msg['To']=to
		msg['Subject']=sub
		msg.set_content(body)
		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			smtp.login(Email_id,Email_pwd)
			smtp.send_message(msg)
		talk('Email sent!')
	
	abort=False
	recipient=None
	subject=None
	body=None
	talk('send an email? But I cannot add mail attachments. Is that ok?')
	cmmd=listen(r)
	while True:
		if (cmmd in COMMANDS[0]['acceptance']) or (cmmd in COMMANDS[0]['confirmations']):
			
			talk('who is the recipient? Type in the mail-id.')
			recipient=input(': ')
			
			talk('what is the subject?')
			subject=listen(r)
			talk('is the subject correct?\n{}'.format(subject))
			while  True:
				crt=listen(r)
				if crt in COMMANDS[0]['confirmations']:
					break
				elif crt in ['abort','cancel']:						#say 'abort' or 'cancel' to cancel the activity.
					talk(choice(COMMANDS[0]['acceptance']))
					abort=True
					break		
				elif crt in COMMANDS[0]['disagree']:
					talk('Sorry my bad! please type in.')
					subject=input(': ')
					break
				else:
					talk('give yes or no opinion')
			
			if not abort:
				talk('what is the body?')
				body=listen(r)
				talk('is the body correct?\n{}'.format(body))
				while  True:
					crt=listen(r)
					if crt in COMMANDS[0]['confirmations']:
						break
					elif crt in ['abort','cancel']:					#say 'abort' or 'cancel' to cancel the activity.
						talk(choice(COMMANDS[0]['acceptance']))
						abort=True
						break		
					elif crt in COMMANDS[0]['disagree']:
						talk('Sorry my bad! please type in.')
						body=input(': ')
						break
					else:
						talk('give yes or no opinion')		
				
				if not abort:
					send_email(recipient,subject,body)
			break
		elif cmmd in COMMANDS[0]['disagree']:
			talk(choice(COMMANDS[0]['acceptance']))
			break
		else:
			talk('Please tell whether it is ok or not.')
			cmmd=listen(r)


"""Welcome Talk"""
def startTalk(r):
	name=os.environ.get('MY_NAME')
	t=datetime.now().time().strftime('%H:%M:%S')
	hr1,min1,sec1=map(int,t.split(':'))
	meridian_eq=None
	if (hr1==0 and min1>=0) or (hr1>0 and hr1<12):
		meridian_eq='morning'  
	elif (hr1==12 and min1>=0) or (hr1>12 and hr1<16):
		meridian_eq='afternoon'
	elif (hr1==16 and min1>=0) or (hr1>16 and hr1<24):
		meridian_eq='evening'
	if name!=None:
		talk('Good {0} {1}!'.format(meridian_eq,name))
	else:
		talk('Good {0}!\nsorry! I don\'t know your name! Please tell your name, not in a sentence but just your name.'.format(meridian_eq))
		name=listen(r)
		while name!=None:
			addName(name)

"""Checks whether the given command contains a Thank you note"""
def check( cmmd, l):
	for x in l:
		if x in cmmd:
			return True
	else:
		return False

"""Assistant function"""
def assistant():
	r = sr.Recognizer()
	r.non_speaking_duration = 0.2
	r.pause_threshold = 0.2
	r.energy_threshold = 200
	startTalk(r)

	while True:	
		cmmd = listen(r)
		if check(cmmd,wakeup):     	#checks whether the input command is a wake up command or not
			talk(choice(COMMANDS[0]['confirmations']) + '! I am ready for your commands.')	
			while True:				
				cmmd = listen(r)

				#Thankyou replies(try saying: thank you (or) thanks)
				if check(cmmd,COMMANDS[0]['gratitude']):
					talk(choice(COMMANDS[0]['gratitude-reply']))

				#email(try saying: send an email (or) email a friend)
				elif 'email' in cmmd:
					emailing(r)			
				
				#word definitions or meanings(try saying: what is the meaning of [word] (or) definition of [word])
				elif ('meaning' in cmmd) or ('definition' in cmmd):
					cmmd=list(cmmd.split())[-1]
					talk(dictionary(cmmd))
				#joke(try saying: tell me a joke (or) i want a joke)
				elif 'joke' in cmmd:	
					talk(joke())
					
				#quote(try saying: give me a nice quote (or) i want a quote)
				elif 'quote' in cmmd:
					talk(quote())
				
				#advice(try saying: give an advice (or) i want an advice)
				elif 'advice' in cmmd:
					talk(advice())	
				
				#end assisting(try saying: bye bye (or) quit)
				elif ('quit' in cmmd) or ('bye' in cmmd):
					talk('anytime. Bye bye!')
					exit()
				#assistant sleep mode(try saying: assistant take rest (or) go to sleep)
				elif ('take rest' in cmmd) or ('sleep' in cmmd):
					talk(choice(COMMANDS[0]['acceptance']))
					break

				#name of the assistant(try saying: what is you name (or) tell me your name (or) who are you)
				elif ('your name' in cmmd) or ('who are you' in cmmd):
					talk('I am coco, your personal and virtual assistant.')
				
				#Logging off of windows(try saying: system inactivity lock screen (or) system inactivity shutdown)
				elif 'system inactivity' in cmmd:
					x=sysInActivity(cmmd[18:])
					if x is not None:
						talk(x)

				#Switching on/off toggles (try saying: switch on Wi-Fi (or) toggle night light)
				elif ('switch on' in cmmd) or ('toggle' in cmmd):
					x=switchOn(cmmd[10:]) if ('switch on' in cmmd) else switchOn(cmmd[7:])
					if x is not None:
						talk(x)

				#Open settings(try saying: brightness settings (or) display settings)
				elif 'settings'==(cmmd.split())[-1]:
					openSettings(' '.join((cmmd.split())[:-1]))

				#Open in browser(try saying: open YouTube.com (or) open sastra.edu)
				elif 'open' in cmmd:
					browser(cmmd[5:])

				#Actual tasks(try saying: what can you do (or) tell what can you do for me)
				elif 'what can you do' in cmmd:
					talk('Tell a joke\nshutdown or hibernate or lock or restart\nGive an advice\nSwitch on or off toggles\nGive meaning of a word\nSend an email\nGive a quote\nopen windows settings\nSearch in web')

				#if command is not identified, Search in google
				else:
					talk('oops! wait, I am googling about, {}'.format(cmmd))
					googling(cmmd)