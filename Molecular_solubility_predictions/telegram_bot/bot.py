import telebot
import config
from telebot import TeleBot, types

from lightgbm import LGBMRegressor
import lightgbm

import pandas as pd
def transform(smiles):

	data_l = pd.DataFrame([smiles], columns=['smiles'])
	train_r = pd.DataFrame()

	train_r['count'] = data_l['smiles'].map(lambda x: len(str(x)))
	train_r['Ccount'] = data_l['smiles'].map(lambda x: str(x).count('C'))
	train_r['Ocount'] = data_l['smiles'].map(lambda x: str(x).count('O'))
	train_r['Ncount'] = data_l['smiles'].map(lambda x: str(x).count('N'))
	train_r['Fcount'] = data_l['smiles'].map(lambda x: str(x).count('F'))
	train_r['Scount'] = data_l['smiles'].map(lambda x: str(x).count('S'))

	train_r['ccount'] = data_l['smiles'].map(lambda x: str(x).count('c'))
	#train['ocount'] = train['smiles'].map(lambda x: str(x).count('o'))
	train_r['ncount'] = data_l['smiles'].map(lambda x: str(x).count('n'))

	train_r['r'] = data_l['smiles'].map(lambda x: 1 if '=' in str(x) else 0)
	train_r['h'] = data_l['smiles'].map(lambda x: 1 if '#' in str(x) else 0)

	return train_r

model = lightgbm.Booster(model_file='model_1.txt')

bot = telebot.TeleBot(config.TOKEN)
print('starting bot...')


states = {}	
inventories = {}

def process_state(user, state):

    # стикер ПОСЛУШАЙТЕ
    if state == 0:
        print(0)

        bot.send_message(user, 'Введите smiles представление молекулы')



def process_answer(user, message):

	# звезды стикер
    if states[user] == 0:
    	print('state 0:', message.text)

    	text = message.text

    	df = transform(text)

    	bot.send_message(user, model.predict(df))

    	states[user] = 1

    process_state(user, states[user])



@bot.message_handler(commands=["start"])
def start_game(message):
    user = message.chat.id
    # print(message.location)
    states[user] = 0
    inventories[user] = []

    bot.send_message(user, "Привет!")

    print('sending start message')

    process_state(user, states[user])


@bot.message_handler(content_types=['text'])
def send_welcome(message):
	user = message.chat.id

	print('answer')
	process_answer(user, message)

def starting():

	try:
		bot.polling(none_stop=True)
	except:
		starting()	

starting()
