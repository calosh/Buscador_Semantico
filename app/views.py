# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from textacy.similarity import jaccard

reload(sys)
sys.setdefaultencoding('utf8')

import unidecode

from operator import itemgetter

from django.shortcuts import render, redirect
import json, ast

from SPARQLWrapper import SPARQLWrapper, JSON
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse


# Create your views here.
import spacy
nlp = spacy.load('es_core_news_md')
#nlp = spacy.load('es', disable=['parse',"ner"])
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


def buscador_skos(request):
    '''
    Buscardor semantico de plantas medicinales
    :param request:
    :return:lista de plantas medicinales
    '''

    if request.method == 'POST':
        print(request.POST)
        planta = request.POST.get('lista')
        print(planta)
        datos = grafico_nodos(planta)
        return render(request, 'visualizador3.html', datos)

    else:
        sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas-skos")
        # http://localhost:8890/plantas
        sparql.setQuery("""
        SELECT * WHERE{
?uri rdf:type <http://dbpedia.org/resource/Medicinal_plants> .
?uri skos:prefLabel ?nombre .
}                     
                """)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        datos = []
        for result in results["results"]["bindings"]:
            # print(result)
            datos.append(result["nombre"]["value"])

    return render(request, 'buscador_semantico_skos.html', {'datos': datos})


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
        consulta_form = text

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

        return render(request, 'anotador.html', {'texto':text, 'listado':maxima_similitud, 'lista':lista, 'consulta':consulta_form})
    listado = []
    consulta_form = "La Universidad Técnica Particular de Loja es una institución educativa del sur del Ecuador"
    texto = ""
    lista = []
    return render(request, 'anotador.html', {'texto':texto,'consulta':consulta_form,'listado':listado, 'lista':lista})


def visualizador(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
    # http://localhost:8890/plantas
    sparql.setQuery("""
    SELECT ?familia ?especie WHERE{
?a rdf:type <http://purl.org/NET/biol/botany#family> .
?a skos:prefLabel ?familia .
?a skos:narrower ?narrower .
?narrower skos:prefLabel ?especie .
}
                    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    # Tree
    data = {}
    data['name'] = 'Familia'
    data['parent'] = 'null'
    list_dict = []

    datos = []
    datos2 = []

    for result in results["results"]["bindings"]:
        # print(result)
        datos.append(result["familia"]["value"])
        datos2.append(result["especie"]["value"])


        #list_dict.append({'name': result["familia"]["value"], 'children': []})
    '''
    # https://github.com/NorthwoodsSoftware/GoJS/blob/master/samples/orgChartStatic.html
    
    { key: 0, name: "Ban Ki-moon 반기문", nation: "South Korea", title: "Secretary-General of the United Nations", headOf: "Secretariat" },
        { key: 1, boss: 0, name: "Patricia O'Brien", nation: "Ireland", title: "Under-Secretary-General for Legal Affairs and United Nations Legal Counsel", headOf: "Office of Legal Affairs" },
          { key: 3, boss: 1, name: "Peter Taksøe-Jensen", nation: "Denmark", title: "Assistant Secretary-General for Legal Affairs" },
    '''

    listado = (zip(datos, datos2))
    datos = set(datos)

    x = []
    x.append({str('key'): "Familia", 'name': "Familia"})
    for i in datos:
        x.append(dict({str('key'):i, str('boss'):"Familia",'name': i}))
        for j in listado:
            if i == j[0]:
                x.append({str('key'): j[1],str('boss'):i, 'name': j[1]})




    json_data = ast.literal_eval(json.dumps(x))
    print(json_data)

    return render(request, 'visualizador.html', {'json_data':json_data})


def visualizador2(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
    # http://localhost:8890/plantas


    '''
    broader de la planta
    '''
    sparql.setQuery("""
    SELECT ?especie ?broaderName WHERE{
?especie skos:prefLabel "Verbena litoralis Kunth." .
?especie skos:broader ?broader .
?broader skos:prefLabel ?broaderName .

}
                    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Tree
    datos = []
    datos2 = []

    broaderName = ""

    for result in results["results"]["bindings"]:
        broaderName = result["broaderName"]["value"]

    '''
    Usos de la planta
    '''
    sparql.setQuery("""
SELECT * WHERE{
?especie skos:prefLabel "Verbena litoralis Kunth." .
?especie skos:related ?related .
?related skos:broader <http://plantas_medicinales.org/planta/usos> .
?related skos:prefLabel ?nameUso .
}
                        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    datosUso = []
    for result in results["results"]["bindings"]:
        datosUso.append(result["nameUso"]["value"])

    '''
    Nombres comunes

    '''
    sparql.setQuery("""
   SELECT * WHERE{
?especie skos:prefLabel "Verbena litoralis Kunth." .
?especie skos:related ?related .
?related rdf:type <http://plantas_medicinales.org/planta/Nombre_comun> .
?related skos:prefLabel ?nombreComun .
}

                            """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    nombresComunes = []
    for result in results["results"]["bindings"]:
        nombresComunes.append(result["nombreComun"]["value"])


    '''
    # https://github.com/NorthwoodsSoftware/GoJS/blob/master/samples/orgChartStatic.html
    { key: "Root", color: lavgrad },
          { key: "Left1", parent: "Root", dir: "left", color: bluegrad },
            { key: "leaf1", parent: "Left1" },
            { key: "leaf2", parent: "Left1" },
            { key: "Left2", parent: "Left1", color: bluegrad },
              { key: "leaf3", parent: "Left2" },
              { key: "leaf4", parent: "Left2" },
          { key: "Right1", parent: "Root", dir: "right", color: yellowgrad },
            { key: "Right2", parent: "Right1", color: yellowgrad },
              { key: "leaf5", parent: "Right2" },
              { key: "leaf6", parent: "Right2" },
              { key: "leaf7", parent: "Right2" },
            { key: "leaf8", parent: "Right1" },
            { key: "leaf9", parent: "Right1" }
    
    '''

    x = []



    nombrePlanta = "Verbena litoralis Kunth."
    root = nombrePlanta
    # Agregar planta
    x.append({str('key'): nombrePlanta})

    # Agregar familia
    x.append({str('key'): "Familia", 'parent': nombrePlanta,})
    x.append({str('key'): broaderName, 'parent': "Familia"})

    x.append({str('key'): "Usos", 'parent': nombrePlanta, "dir": "left" })
    for i in datosUso:
        x.append({str('key'): i, 'parent': "Usos"})

    x.append({str('key'): "Nombres comunes", 'parent': nombrePlanta, "dir": "right"})
    for i in nombresComunes:
        x.append({str('key'): i, 'parent': "Nombres comunes"})


    json_data = ast.literal_eval(json.dumps(x))
    print(json_data)

    return render(request, 'visualizador2.html', {'json_data': json_data, 'root':root})


def grafico_nodos(consulta):
    sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas")
    # http://localhost:8890/plantas

    nombrePlanta = consulta
    '''
    broader de la planta
    '''
    sparql.setQuery("""
        SELECT ?especie ?broaderName WHERE{
    ?especie skos:prefLabel "%s" .
    ?especie skos:broader ?broader .
    ?broader skos:prefLabel ?broaderName .

    }
                        """ % (nombrePlanta))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    broaderName = ""

    for result in results["results"]["bindings"]:
        broaderName = result["broaderName"]["value"]

    '''
    Usos de la planta
    '''
    sparql.setQuery("""
    SELECT * WHERE{
    ?especie skos:prefLabel "%s" .
    ?especie skos:related ?related .
    ?related skos:broader <http://plantas_medicinales.org/planta/usos> .
    ?related skos:prefLabel ?nameUso .
    }
                            """ % (nombrePlanta))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    datosUso = []
    for result in results["results"]["bindings"]:
        datosUso.append(result["nameUso"]["value"])

    '''
    Nombres comunes

    '''
    sparql.setQuery("""
       SELECT * WHERE{
    ?especie skos:prefLabel "%s" .
    ?especie skos:related ?related .
    ?related rdf:type <http://plantas_medicinales.org/planta/Nombre_comun> .
    ?related skos:prefLabel ?nombreComun .
    }

                                """ % (nombrePlanta))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    nombresComunes = []
    for result in results["results"]["bindings"]:
        nombresComunes.append(result["nombreComun"]["value"])

    '''
    # https://github.com/NorthwoodsSoftware/GoJS/blob/master/samples/orgChartStatic.html
    '''
    # Otras plantas
    sparql.setQuery("""
        SELECT * WHERE{
    ?uri skos:prefLabel "%s" .
    ?uri skos:narrower ?uri_planta .
    ?uri_planta skos:prefLabel ?planta .

    }
                                """ % (broaderName))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    otrasPlantas = []
    for result in results["results"]["bindings"]:
        otrasPlantas.append(result["planta"]["value"])

    node = []
    link = []

    # Agregar planta
    node.append({str('key'): nombrePlanta, 'text': nombrePlanta})

    # Agregar familia
    node.append({'key': broaderName, 'text': broaderName})
    link.append({'from': nombrePlanta, 'to': broaderName, 'text': "perternece a familia"})

    # Agregar otras plantas
    cont = 0
    for i in otrasPlantas:

        if i == nombrePlanta:
            break
        cont = cont + 1
    del otrasPlantas[cont]
    print(otrasPlantas)

    for i in otrasPlantas:
        node.append({'key': str(i), 'text': str(i)})
        link.append({'to': str(i), 'from': broaderName, 'text': "otras plantas"})

    # Agregar nombres comunes
    node.append({'key': "Nombres comunes", 'text': "Nombres comunes"})
    link.append({'from': nombrePlanta, 'to': "Nombres comunes", 'text': "tiene"})


    for i in nombresComunes:
        print(i)
        node.append({'key': unidecode.unidecode(i), 'text': unidecode.unidecode(i)})
        link.append({'to': unidecode.unidecode(i), 'from': "Nombres comunes", 'text': "nombre"})

    # Agregar usos
    node.append({'key': "Usos", 'text': "Usos"})
    link.append({'from': nombrePlanta, 'to': "Usos", 'text': "tiene"})

    print(datosUso)
    for i in datosUso:
        node.append({'key': i, 'text': i})
        link.append({'from': "Usos", 'to': i, 'text': "uso"})

    node = ast.literal_eval(json.dumps(node))
    link = ast.literal_eval(json.dumps(link))
    # json.dumps(foo, ensure_ascii=False)
    print(node)
    print(link)

    return {'node':node, 'link':link}