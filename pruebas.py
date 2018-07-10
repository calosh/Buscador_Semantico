# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf8')


lista1 = ["Loja", "Ecuaodr"]
lista2 = [[1,2,3,3],[4,1,2,3,1]]


print(zip(lista1, lista2))