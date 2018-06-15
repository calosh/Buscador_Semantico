# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect


from SPARQLWrapper import SPARQLWrapper, JSON
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse



import time


# Create your views here.


from .forms import EnfermedadForm


def index(request):
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
    return render(request, 'index.html', {'datos':datos})



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

