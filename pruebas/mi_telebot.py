'''

https://www.youtube.com/watch?v=4fcDku71LLY
https://github.com/eternnoir/pyTelegramBotAPI



'''
import json

from snips_prueba import pregunta, consulta_sparql

import telebot

bot = telebot.TeleBot("579712633:AAEBY8HSwTxf01ZmHf80Z7cy6QOCT1pKxzM")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    #bot.reply_to(message, message.text)

    chat_id = message.chat.id
    try:
        texto = message.json['text']
    except AttributeError:
        texto = "N/A"
    print("ESte es el texto")
    print(texto)
    respuesta_json = pregunta(texto)
    respuesta_json = json.loads(respuesta_json)

    print(type(respuesta_json))
    print(respuesta_json)
    try:
        intencion = respuesta_json['slots'][0]['entity'] #enfermedad
        enfermedad = respuesta_json['slots'][0]['value']['value']

        lista_plantas = consulta_sparql(enfermedad)
        print("ESta es la lista de plantas")
        print(lista_plantas)
        platas_srt = ""
        lista_nombres_plantas = []
        for i in lista_plantas:
            lista_nombres_plantas.append(i[0])
        for j in lista_nombres_plantas:
            if lista_nombres_plantas[-1]==j:
                platas_srt = platas_srt + " y "+j
            elif lista_nombres_plantas[-2]==j:
                platas_srt = platas_srt + j + " "
            else:
                platas_srt = platas_srt + j + ", "



        print("Plnatas")
        print(platas_srt)

        print("ESta es la intencion")
        print(intencion)
        print("ESta es la enfermedad")
        print(enfermedad)
    except IndexError:
        platas_srt = "No hay planta"
    bot.send_message(chat_id, platas_srt)
    #send_message(chat_id, text)


print "Se inicio el bot"
bot.polling()


