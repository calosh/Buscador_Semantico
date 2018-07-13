# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf8')


cadena = """
SELECT * WHERE{
?especie skos:prefLabel "Verbena litoralis Kunth." .
?especie skos:related ?related .
?related skos:broader <http://plantas_medicinales.org/planta/usos> .
?related skos:prefLabel ?nameUso .
}
"""

print(cadena)
cadena = """
SELECT * WHERE{
?especie skos:prefLabel "%s" .
?especie skos:related ?related .
?related skos:broader <http://plantas_medicinales.org/planta/usos> .
?related skos:prefLabel ?nameUso .
}
""" %("Hola")
print(cadena)