# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import snips_nlu

snips_nlu.load_resources("es")


'''
1)
(venv) calosh@chigo ~/PycharmProjects/SBC/pruebas $ snips-nlu generate-dataset es entity_enfermedad.txt intent_enfermedad.txt > dataset.json

2) Ejecutar Entrenamiento


'''

import io
import json
from snips_nlu import SnipsNLUEngine, load_resources


with io.open("trained.json") as f:
    engine_dict = json.load(f)

engine = SnipsNLUEngine.from_dict(engine_dict)

#phrase = raw_input("Pregunta: ")


def pregunta(phrase):
    r = engine.parse(unicode(phrase))
    return json.dumps(r, indent=2)
    #print(json.dumps(r, indent=2))



from SPARQLWrapper import SPARQLWrapper, JSON

def consulta_sparql(enfermedad):
    sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
    # http://localhost:8890/plantas
    sparql.setQuery("""
                SELECT * WHERE{
                    ?planta skos:related ?enfermedad .
                    ?planta skos:prefLabel ?nombre .
                    ?planta skos:definition ?definition .
                    ?enfermedad skos:prefLabel ?label .
FILTER regex(?label, '"""+enfermedad+"""', 'i')
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
