#!/usr/bin/env python
import os
import sys

from SBC.settings import BASE_DIR

from chatbot.metodos import get_input_slots_intent, get_plantas_medicinales

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SBC.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)



'''

https://www.youtube.com/watch?v=4fcDku71LLY
https://github.com/eternnoir/pyTelegramBotAPI



'''

import json
import telebot

from metodos import pregunta, consulta_sparql
from chatbot.clave import clave

bot = telebot.TeleBot(clave)

from app.models import Log, ImagenPlanta


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    log = Log(log_json="Hola")
    log.save()
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['desc'])
def send_descripcion(message):
    print(message)
    s = Log(log_json="aaaaa")
    s.save()
    bot.reply_to(message, "Hola")



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("message")
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

    print("ESTA EST EL JSON SIN NADA")
    print(respuesta_json)
    if not respuesta_json['slots']:
        respuesta = "Please, repita la pregunra: None"
    else:
        input, slots, intent = list(get_input_slots_intent(respuesta_json))[0]

        print("SLOT")
        print(slots[0][0])
        print("INTENT")
        print(intent[0][1])
        umbral = 0.60
        if slots[0][0] == "enfermedad" and intent[0][1] < umbral:
            respuesta = "Please, repita la pregunta: < 0.70"
        elif slots[0][0] == "desc":
            respuesta = ""

            chats = Log.objects.filter(id_chat=chat_id).order_by('-time')[0]

            lista_plantas = consulta_sparql(chats.entity)
            lista_nombres_plantas = []
            lista_nombres_desc = []
            for i in lista_plantas:
                lista_nombres_plantas.append(i[0])
                lista_nombres_desc.append(i[1])

            l = zip(lista_nombres_plantas,lista_nombres_desc)
            for i in l:
                respuesta = respuesta + "{0}: {1}\n".format(i[0],i[1])

        elif slots[0][0] == "enfermedad" and intent[0][1]>=umbral:
            lista_plantas = consulta_sparql(slots[0][1])
            print("Esta es la lista de plantas")
            print(lista_plantas)
            lista_nombres_plantas = []
            for i in lista_plantas:
                lista_nombres_plantas.append(i[0])
            respuesta = "Las plantas que son buenas para el/la %s son: " %(slots[0][1])

            log = Log(texto_json=respuesta_json, log_json=message, id_chat=chat_id, pregunta=input, slots=slots[0][0],
                      intent= intent[0][1], entity=slots[0][1])
            log.save()

            respuesta = respuesta + get_plantas_medicinales(lista_nombres_plantas)


        elif slots[0][0] == "saludo":
        #else:
            respuesta = "Hola!!"

        #else:
        #    respuesta = "Error desconocido"

        elif slots[0][0] == "foto":
            print("Prueba imagen")

            respuesta = ""

            chats = Log.objects.filter(id_chat=chat_id).order_by('-time')[0]

            lista_plantas = consulta_sparql(chats.entity)
            lista_nombres_plantas = []
            for i in lista_plantas:
                lista_nombres_plantas.append(i[0])

            print("Lista de plantas")
            print(lista_nombres_plantas)
            for i in lista_nombres_plantas:
                message = "Planta: %s" %(i)
                bot.send_message(chat_id, message)
                print("Plata uri")

                foto = ImagenPlanta.objects.get(title=i)
                planta_url = foto.foto

                planta_url = "static/imagenes_plantas/"+str(planta_url)
                print(planta_url)
                photo = open(os.path.join(BASE_DIR, planta_url), 'rb')

                bot.send_photo(chat_id, photo)

            respuesta = ""

    if (respuesta):
        bot.send_message(chat_id, respuesta)
    #send_message(chat_id, text)


print("Se inicio el bot")
bot.polling()



