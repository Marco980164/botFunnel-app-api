import requests
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import InstanciaConversacion
from instanciaConversacion import serializers
from openai import OpenAI


class ChatBotAPIView(viewsets.ModelViewSet):
    serializer_class = serializers.ChatbotRequestSerializer
    queryset = InstanciaConversacion.objects.all().order_by('id')
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idConversacion = serializer.validated_data.get('idConversacion')
        idPregunta = serializer.validated_data.get('idPregunta')
        pregunta = serializer.validated_data.get('pregunta')
        respuesta = serializer.validated_data.get('respuesta')

        api_url = "http://127.0.0.1:8000/api/configBot/configBot/"
        headers = { 'content-type': 'application/json' }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        nombre = data[0].get('nombre')
        proposito = data[0].get('proposito')
        nombreNegocio = data[0].get('nombreNegocio')
        descripcionNegocio = data[0].get('descripcionNegocio')
        infoExtra = data[0].get('infoExtra')

        api_url = "http://127.0.0.1:8000/api/modelo/conversaciones/"

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for conversacion in data:
            if conversacion.get('id') == idConversacion:
                conversacion = conversacion
                break

        api_url = "http://127.0.0.1:8000/api/modelo/preguntas/"

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for elemento in data:
            if elemento.get('id') == idPregunta:
                preguntaDesdeId = elemento.get('pregunta')
                break


        revisionRespuesta = ("De acuerdo la pregunta y respuesta que te mande el usuario revisa lo siguiente: ¿La respuesta es valida para la pregunta? Si es valida responde con 'true' de lo contrario responde con un 'false'")
        promptRevisionRespuesta = ("Pregunta: " + pregunta + " Respuesta: " + respuesta)

        evaluacionPreguntas = ("Evalua la pregunta junto con la respuesta en un rango del 1 al 10 dependiendo de que tan acertada fue la respuesta. Regresa exclusivamente el valor de la calificacion.")

        correccionUsuario = ("Tu nombre es " + nombre + "Tu proposito es: "+ proposito + "el nombre del negocio en donde estas es: " + nombreNegocio + "la descripcion del negocio es: " + descripcionNegocio + "informacion extra: " + infoExtra +"Dile al usuario que la respuesta no es correcta o resuelve su duda si es que te esta preguntado algo, y despues repitele la pregunta. Repite la pregunta: " + pregunta)

        client = OpenAI(api_key="")
        resultadoRevisionRespuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": revisionRespuesta},
                {"role": "user", "content": promptRevisionRespuesta},
            ]
        )

        if resultadoRevisionRespuesta.choices[0].message.content == "true":
            revisionRespuestaBoolean = True
        else:
            revisionRespuestaBoolean = False

        if revisionRespuestaBoolean:
            resultadoEvaluacionPreguntas = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": evaluacionPreguntas},
                    {"role": "user", "content": "Pregunta: " + pregunta + " Respuesta: " + respuesta}
                ]
            )

            calificacion = resultadoEvaluacionPreguntas.choices[0].message.content

            response_data = {
                "pregunta": pregunta,
                "respuesta": f"{revisionRespuesta}",
                "calificacion": calificacion,
                "respuestaValida": revisionRespuestaBoolean
            }

        else:
            resultadoCorreccionUsuario = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": correccionUsuario},
                ]
            )

            repeticionDePregunta = resultadoCorreccionUsuario.choices[0].message.content

            response_data = {
                "pregunta": pregunta,
                "respuesta": f"{repeticionDePregunta}",
                "calificacion": 0,
                "respuestaValida": revisionRespuestaBoolean
            }

        response_serializer = serializers.ChatbotResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
