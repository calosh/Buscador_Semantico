# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from textacy.similarity import jaccard

reload(sys)
sys.setdefaultencoding('utf8')


from operator import itemgetter


from django.shortcuts import render, redirect


from SPARQLWrapper import SPARQLWrapper, JSON
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse


# Create your views here.
import spacy
nlp = spacy.load('es_core_news_md')
sparql = SPARQLWrapper("http://dbpedia.org/sparql/")


def index(request):

    return render(request, 'index.html')

def buscador_pm_index(request):
    '''
    Buscardor semantico de plantas medicinales
    :param request:
    :return:lista de plantas medicinales
    '''
    datos = []
    if request.method == 'POST':

        pass

    else:
        sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
        # http://localhost:8890/plantas
        sparql.setQuery("""
                    SELECT * WHERE{
                        ?a skos:broader ?c .
                        ?c skos:prefLabel 'Enfermedades' .
                        ?a skos:prefLabel ?d .
                        }
                   
                """)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        datos = []
        for result in results["results"]["bindings"]:
            #print(result)
            datos.append(result["d"]["value"])

        #print(datos)
    return render(request, 'buscador_semantico.html', {'datos':datos})



def plantas_ajax(request):
    if request.is_ajax():
        #enfermedad_form = EnfermedadForm(request.POST)
        #enfermedad_form = request.POST['lista']
        #id_region = int(request.GET['lista'])
        enfermedad_form = (request.GET['id'])
        print(enfermedad_form)
        sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
        # http://localhost:8890/plantas
        sparql.setQuery("""
            SELECT * WHERE{
                ?planta skos:related ?enfermedad .
                ?planta skos:prefLabel ?nombre .
                ?planta skos:definition ?definition .
                ?enfermedad skos:prefLabel '"""+enfermedad_form+"""' .
                }
        """)
        # definition
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        #print(results)
        datos = []
        for result in results["results"]["bindings"]:
            # print(result)
            datos.append([result["nombre"]["value"],result["definition"]["value"]])

        # https://github.com/django-crispy-forms/django-crispy-forms/issues/553

        t = get_template('plantas_medicinales.html')
        html = t.render({'datos':datos})
        html = html + ""
        response = JsonResponse({'plantas': html})
        return HttpResponse(response.content)
    else:
        return redirect("/")


def extraccion_informacion(request):
    #o = u"Dr. José Barbosa, Rector Canciller UTPL, saluda a los estudiantes, docentes y administrativos por el Cuadragésimo Segundo Aniversario de fundación de la Universidad Técnica Particular de Loja."
    if request.method=="POST":
        text = request.POST['consulta']

        #consulta = u'''Dr. José Barbosa, Rector Canciller UTPL, saluda a los estudiantes, docentes y administrativos por el Cuadragésimo Segundo Aniversario de fundación de la Universidad Técnica Particular de Loja. '''
        print(text)
        doc1 = nlp(text)

        # Listado de entidades reconocidas por la libreria
        lista_entidades = []
        for ent in doc1.ents:
            # print ent.text, ent.lemma_, ent.pos_, ent.is_stop, ent.is_punct
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            lista_entidades.append([ent.text, ent.start_char, ent.end_char, ent.label_])

        m_entidades = []
        conjunto_matriz_triples = []
        conjunto_matriz_triples2 = []
        for entidad in lista_entidades:
            print("Tabla")
            print(lista_entidades)
            print('Entidad: {0} --> tipo: {1}'.format(entidad[0],entidad[3]))

            consulta = '''SELECT * WHERE{
?uri rdfs:label ?label .
?uri foaf:name ?name .
?uri rdfs:comment ?comment .
                                
FILTER (?label = "%s"@es || ?label = "%s"@en || ?name="%s"@es || ?name="%s"@en)
FILTER (lang(?label) = 'es')
FILTER (lang(?comment) = 'es')
}
''' % (str(entidad[0]),str(entidad[0]), str(entidad[0]), str(entidad[0]))



            print consulta
            sparql.setQuery(consulta)
            # definition
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            # print(results)
            conjunto_triples = []
            conjunto_triples2 = []
            for result in results["results"]["bindings"]:
                # print(result)
                # EJEMPLO: [u'http://www.wikidata.org/entity/Q332989', u'ciudad', u'Loja', u'Loja']
                conjunto_triples.append([result["uri"]["value"], result["name"]["value"], result["label"]["value"], result["comment"]["value"],entidad[0]])
                conjunto_triples2.append(result["uri"]["value"])

            if results:
                m_entidades.append(entidad[0])
                conjunto_matriz_triples.append(conjunto_triples)
                conjunto_matriz_triples2.append(conjunto_triples2)

            #lista.append([entidad[0], conjunto_matriz_triples])

        print("Esta es la lista de datos")
        print(conjunto_matriz_triples)


        similitud = []
        maxima_similitud = []
        for entidad_triples in conjunto_matriz_triples:
            for triple in entidad_triples:

                print(triple)
                sim = jaccard(triple[1], text)
                print("Se compara: ")
                print(triple[1]+" -- " +text)
                print(sim)


                similitud.append([triple[0], triple[1], triple[2], sim])

            if similitud:
                similitud = sorted(similitud, key=itemgetter(3), reverse=True)

                maxima_similitud.append(similitud[0])
            else:
                maxima_similitud.append(None)
            similitud = []

        print(maxima_similitud)

        entidades = maxima_similitud

        # html
        cont = 0
        for entidad in lista_entidades:
            if entidades[cont] is not None:
                link = "<a href=" + entidades[cont][0] + ">" + lista_entidades[cont][0] + "</a>"
                mayor = lista_entidades[cont][2]
                menor = lista_entidades[cont][1]
                n = mayor - menor

                longuitud = len(link) - (n)
                # print(longuitud)

                text = text[:lista_entidades[cont][1]] + link + text[lista_entidades[cont][2]:]

                for triple in lista_entidades:
                    triple[1] = triple[1] + longuitud
                    triple[2] = triple[2] + longuitud

            cont = cont + 1

        print(text)

        lista = zip(m_entidades, conjunto_matriz_triples2)

        return render(request, 'anotador.html', {'texto':text, 'listado':maxima_similitud, 'lista':lista})
    listado = []
    texto = ""
    lista = []
    return render(request, 'anotador.html', {'texto':texto, 'listado':listado, 'lista':lista})
