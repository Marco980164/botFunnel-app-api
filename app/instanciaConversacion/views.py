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

        pregunta = serializer.validated_data.get('pregunta')

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


        config = (
            f"Eres un chatbot que se llama {nombre} con el propósito de {proposito} dentro del entorno de {descripcionNegocio} llamada {nombreNegocio}."
            f"Contexto extra: {infoExtra}"

            # f"Complejidad del lenguaje: {complexity}."
            # f"Propósito de la conversación: {conversation_purpose}."
            # f"Emoción de la conversación: {emotion}."
            # f"Uso de analogías: {analogies}."
            # f"Nivel de empatía: {empathy}."
            # f"Longitud de respuestas: {length}."
            # f"Nivel de retroalimentación por parte del cliente: {feedback}."
            # f"Tono de la conversación: {tone}."

        )

        # client = OpenAI(api_key="")
        # prueba = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": "Hola, ¿cómo estás?"},
        #     ]
        # )

        # cosa =prueba.choices[0].message.content

        response_data = {
            'pregunta': pregunta,
            'respuesta': f"{config}",
            'calificacion': 10
        }

        response_serializer = serializers.ChatbotResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
