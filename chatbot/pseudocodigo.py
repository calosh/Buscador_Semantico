
def chat_bot(solicitud_json):
    if not solicitud_json['slots']:
        res= "Vuelva a intentar"
    else:
        input_text, slot, intent = solicitud_json
        umbral = 0.70

        if slot == "enfermedad" and intent < umbral:
            res = "Repita la pregunta"

        elif slot == "descripcion":
            chat = getLastChat(id_chat)
            enfermedad = chat['enfermedad']
            plantas = consultaSPARQL(enfermedad)
            res = generarDescripcion(plantas)

        elif slot == "enfermedad" and intent >= umbral:
            plantas = consultaSPARQL(enfermedad)
            res = generarRespuesta(plantas)

        elif slot == "saludo":
            res = "Hola!!!"

        else:
            res = "Repita la pregunta"

    return res