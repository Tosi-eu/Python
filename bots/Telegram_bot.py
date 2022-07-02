# -*- coding: utf-8 -*-
import requests 
import telebot
from telebot import types
import pymysql #SQL library
from datetime import date, datetime
import pgeocode

conn = pymysql.connect(host='127.0.0.1', 
unix_socket='/opt/lampp/var/mysql/mysql.sock', #qual base ele deve se conectar
user='root', #usuario
passwd=None,
charset='utf8mb4', #vazio
db='users_tele') #nome do banco de dados

# 127.0.0.1 é igual localhost

cur = pymysql.cursors.SSDictCursor(conn)

API_TOKEN = '5121391345:AAFk9ApsdfmXhUUpzBCYil-UJqJKDZ_KmH4'

bot = telebot.TeleBot(API_TOKEN) #telebot = summary \\ Telebot = commands \\ Applying token
user_dict = {} #variables

class User:
	def __init__(self,name):
		self.name = name
		self.load = None
		self.workout = None
		self.exercise = None
		self.mail = None
		self.data = None
		self.uf = None
		self.sity = None

@bot.message_handler(commands=['start'])

def send_welcome(message):
	msg = bot.reply_to(message,"Tudo bem? Este é o bot que salva as suas façanhas marombísticas!")#inserindo mensagem
	cid = message.chat.id
	bot.send_message(cid, "Teve uma carga legal e quer salvar? Faço isso pra ti :)")
	bot.send_message(cid, "Nosso id é: " + str(cid))
	bot.send_message(cid, "Qual seu nome?: ")
	
	while(message.isalpha() == False):
		bot.send_message(cid, "Oxi, tem caracter inválido aí, reescreva: )
		
	bot.register_next_step_handler(msg,process_name_step) #next

def process_name_step(message):
	try:
		chat_id = message.chat.id
		name = message.text
		user = User(name)
		user_dict[chat_id] = user #armazenando o chat_id desta conversa, único
		msg = bot.reply_to(message,'Qual a carga máxima no exercício que você vai colocar [Kg\Lbs]?')
		bot.register_next_step_handler(msg,process_load_step)
	except Exception as e:
		bot.reply_to(message,e)

def process_load_step(message):
	try:
		chat_id = message.chat.id
		load = message.text
		if not load.isdigit():
			msg = bot.reply_to(message,"Você precisa digitar um número! Qual sua carga máxima nesse exercício [Kg\Lbs]?")
			bot.register_next_step_handler(msg,process_load_step)
			return
		user = user_dict[chat_id]
		user.load = load
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) #cria a opção
		markup.add('Peito', 'Costas', 'Pernas', 'Bíceps', 'Tríceps', 'Ombros') #quais as categorias
		msg = bot.reply_to(message, 'Selecione o tipo de treino:',reply_markup=markup) #envia a opcao
		bot.register_next_step_handler(msg, process_workout_step)
	except Exception as e:
		bot.reply_to(message, 'Oops, algo deu errado')
		print(e)

def process_workout_step(message):
	try:
		chat_id = message.chat.id
		workout = message.text
		user = user_dict[chat_id]
		if (workout == u'Peito') or (workout == u'Costas') or (workout == u'Pernas') or (workout == u'Bíceps') or (workout == u'Tríceps') or (workout == u'Ombros'):
			user.workout = workout
		else:
			raise Exception()
		msg = bot.reply_to(message,'Qual o exercício?')
		bot.register_next_step_handler(msg, process_exercise_step)
		
	except Exception as e:
		bot.reply_to(message,e)

def process_exercise_step(message):
	try:
		chat_id = message.chat.id
		exercise = message.text
		user = user_dict[chat_id]	
		user.exercise = exercise
		msg = bot.reply_to(message, 'Para finalizarmos, você mora em que país?')
		bot.register_next_step_handler(msg, process_cep_step)
	except Exception as e:
		bot.reply_to(message,e)
		
def process_cep_step(message):
	try:
		chat_id = message.chat.id
		country = message.text
		user = user_dict[chat_id]
		user.country = country
		
		# convert date to brazilian format
		calendar = datetime.today().strftime('%d/%m/%Y')
		user.data = calendar
		
		msg = bot.reply_to(message,'E qual seu CEP?')	
		bot.register_next_step_handler(msg, process_cep_step_final)
			
	except Exception as e:
		bot.reply_to(message,e)
		
def process_cep_step_final(message):
	try:
		chat_id = message.chat.id
		CEP = message.text
		user = user_dict[chat_id]
		
		# get zipcode data
		
		nomi = pgeocode.Nominatim(user.country)
		nomi.query_postal_code(CEP)
		
		# convert date to brazilian format
		calendar = datetime.today().strftime('%d/%m/%Y')
		user.data = calendar
		
		uf = nomi.query_postal_code(CEP)['country_code']
		city = nomi.query_postal_code(CEP)['place_name']
		user.uf = uf
		user.city = city
		
		# nome da base
		cur.execute("USE users_tele") #executando base a ser usada
		sql = "INSERT INTO users (username,chat_id_users,workout_users,exercise_users,load_users, data_users, country_user, city_user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" #comando
		val = (user.name,str(chat_id),user.workout,user.exercise,str(user.load), str(calendar), str(uf), str(city))
		cur.execute(sql,val)#comando insert + valores
		conn.commit() #ação do comando digitado	
	
	except Exception as e:
		bot.reply_to(message,e)	
		
	finally:
		msg = bot.reply_to(message,'Obrigado por se cadastrar!')	
		
			
bot.enable_save_next_step_handlers(delay=1) #step
bot.load_next_step_handlers()

bot.polling()
