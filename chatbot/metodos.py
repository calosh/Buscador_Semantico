# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import snips_nlu

snips_nlu.load_resources("es")

from SPARQLWrapper import SPARQLWrapper, JSON


import io
import json
from snips_nlu import SnipsNLUEngine, load_resources

with io.open("entrenamiento/trained.json") as f:
    engine_dict = json.load(f)

engine = SnipsNLUEngine.from_dict(engine_dict)


def pregunta(phrase):
    r = engine.parse(unicode(phrase))
    return json.dumps(r, indent=2)
    # print(json.dumps(r, indent=2))


def consulta_sparql(enfermedad):
    sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
    # http://localhost:8890/plantas
    sparql.setQuery("""
                SELECT * WHERE{
                    ?planta skos:related ?enfermedad .
                    ?planta skos:prefLabel ?nombre .
                    ?planta skos:definition ?definition .
                    ?enfermedad skos:prefLabel ?label .
FILTER regex(?label, '""" + enfermedad + """', 'i')
                    }
            """)
    # definition
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results)
    datos = []
    for result in results["results"]["bindings"]:
        # print(result)
        datos.append([result["nombre"]["value"], result["definition"]["value"]])
    return datos



def dicccionario_slots_entity(json):
    """
    Obtiene los elementos: input, slots y intent
    :param json:
    :return: lista
    """

    for i in json:
        yield json[i]


def get_slots(slots):
    """
    Obtiene los diferentes valores del array de slots
    :param slots:
    :return: array [entity][value]
    """

    for slot in slots:
        yield slot['entity'], slot['value']['value']


def get_intent(intent):
    """
    Obtiene el nombre del intent y la probabilidad
    :param intent:
    :return: list [intent, probabilidad]
    """
    # {u'intentName': u'saludo', u'probability': 0.7856671964209185}}
    yield intent['intentName'], intent['probability']



def get_input_slots_intent(json_text):
    """
    Obtiene input, slots e intent
    :param json_text:
    :return: generador-list[input, slots, intent]
    """
    input, slots, intent = dicccionario_slots_entity(json_text)
    yield input, list(get_slots(slots)), list(get_intent(intent))


def get_plantas_medicinales(lista_nombres_plantas):
    """
    Retorna la respuesta de las plantas
    :param lista_nombres_plantas:
    :return:
    """
    if not lista_nombres_plantas:
        respuesta = "No hay planta medicinal"
    else:
        respuesta = ""
        for j in lista_nombres_plantas:

            if len(lista_nombres_plantas) == 1:
                respuesta = j
                break
            elif lista_nombres_plantas[-1] == j:
                respuesta = respuesta + " y " + j
            elif lista_nombres_plantas[-2] == j:
                respuesta = respuesta + j + " "
            else:
                respuesta = respuesta + j + ", "

    return respuesta




