dicicionario = {u'input': u'Hola como estas',
                u'slots': [{u'range': {u'start': 0, u'end': 4}, u'entity': u'saludo', u'slotName': u'saludo', u'value': {u'kind': u'Custom', u'value': u'Hola'}, u'rawValue': u'Hola'}, {u'range': {u'start': 5, u'end': 15}, u'entity': u'pregunta', u'slotName': u'pregunta', u'value': {u'kind': u'Custom', u'value': u'como estas'}, u'rawValue': u'como estas'}],
                u'intent': {u'intentName': u'saludo', u'probability': 1.0}}




print(type(dicicionario))


for i in dicicionario:
    print(i)


input = dicicionario['input']
slots = dicicionario['slots']
intent = dicicionario['intent']



print(input)
print("SLOTS")
print(slots)
'''
[{u'range': {u'start': 0, u'end': 4}, u'rawValue': u'Hola', u'slotName': u'saludo', 
u'value': {u'kind': u'Custom', u'value': u'Hola'}, u'entity': u'saludo'}, 
{u'range': {u'start': 5, u'end': 15}, u'rawValue': u'como estas', u'slotName': u'pregunta', 
u'value': {u'kind': u'Custom', u'value': u'como estas'}, u'entity': u'pregunta'}]
'''
for i in slots:
    print(i)
#print(intent)


from datetime import datetime
print datetime.now()