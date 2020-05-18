import requests
import json
import random

"""Will do the API call to owlbot to fetch the meaning of the given word"""
def dictionary(word):
	url='https://owlbot.info/api/v4/dictionary/'
	auth='[AUTHORIZATION-KEY]'		#Provide the api key given by the owlbot
	head={'Authorization':auth}
	res=requests.get(url+word,headers=head)
	x=json.loads(res.text)
	fmt_str=[]
	try:
		for d in x['definitions']:
			fmt_str.append('type: '+d['type']+', definition: '+d['definition'])
	except :
		fmt_str.append('There is no definition for '+word)

	return('\n'.join(fmt_str))

"""Will do the API call to adviceslip to fetch a random advice"""
def advice():
	url='https://api.adviceslip.com/advice'
	res=requests.get(url)
	x=json.loads(res.text)
	return x['slip']['advice']

"""Will do the API call to forismatic to fetch a random quote"""
def quote():
	url='http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
	res=requests.post(url)
	x=res.json()
	return (x['quoteText'])

"""Will do the API call to joke-api to fetch a random joke"""
def joke():
	l=['https://official-joke-api.appspot.com/jokes/random','https://official-joke-api.appspot.com/random_joke']
	url=l[random.randint(0,1)]
	res=requests.get(url)
	x=json.loads(res.text)
	return (x['setup']+'\n'+x['punchline'])	

