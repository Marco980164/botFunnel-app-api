from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatbotRequestSerializer, ChatbotResponseSerializer
from openai import OpenAI


class ChatBotAPIView(APIView):

    def post(self, request):
        serializer = ChatbotRequestSerializer(data=request.data)
        if serializer.is_valid():
            pregunta = serializer.validated_data('pregunta')

            

            response_data = {
                'respuesta': 'Hola, soy un chatbot',
                'calificacion': 10
            }

            response_serializer = ChatbotResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
