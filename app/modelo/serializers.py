"""
Serializers for modelo APIs.
"""

from rest_framework import serializers
from core.models import (
    Modelo,
    Conversacion,
    Pregunta,
)


class PreguntaSerializer(serializers.ModelSerializer):
    """Serializer for pregunta objects."""

    class Meta:
        model = Pregunta
        fields = ('id',
                  'pregunta',
                  'descripcion',
                  'tonopregunta',
                  'lenguaje')
        read_only_fields = ('id',)


class ConversacionSerializer(serializers.ModelSerializer):
    """Serializer for conversacion objects."""
    preguntas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Pregunta.objects.all(),
        required=False
    )

    class Meta:
        model = Conversacion
        fields = (
            'id',
            'nombre',
            'is_active',
            'complejidad',
            'proposito',
            'emocion',
            'analogias',
            'empatia',
            'longitudRespuesta',
            'retroalimentacion',
            'tono',
            'preguntas',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new conversacion."""
        preguntas = validated_data.pop('preguntas', [])
        conversacion = Conversacion.objects.create(**validated_data)
        # for pregunta in preguntas:
        #     pregunta_obj, created = Pregunta.objects.get_or_create(
        #         **pregunta,
        #     )
        #     conversacion.preguntas.add(pregunta_obj)
        conversacion.preguntas.set(preguntas)

        return conversacion

    def update(self, instance, validated_data):
        """Update a conversacion."""
        preguntas = validated_data.pop('preguntas', None)
        if preguntas is not None:
            # instance.preguntas.clear()
            # for pregunta in preguntas:
            #     pregunta_obj, created = Pregunta.objects.get_or_create(
            #         **pregunta,
            #     )
            #     instance.preguntas.add(pregunta_obj)
            instance.preguntas.set(preguntas)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ModeloSerializer(serializers.ModelSerializer):
    """Serializer for modelo objects."""
    conversaciones = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Conversacion.objects.all(),
        required=False
    )

    class Meta:
        model = Modelo
        fields = ('id', 'nombre', 'is_active', 'conversaciones')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new modelo."""
        conversaciones = validated_data.pop('conversaciones', [])
        modelo = Modelo.objects.create(**validated_data)
        # for conversacion in conversaciones:
        #     conversacion_obj, created = Conversacion.objects.get_or_create(
        #         **conversacion,
        #     )
        #     modelo.conversaciones.add(conversacion_obj)
        modelo.conversaciones.set(conversaciones)

        return modelo

    def update(self, instance, validated_data):
        """Update a modelo."""
        conversaciones = validated_data.pop('conversaciones', None)
        if conversaciones is not None:
            # instance.conversaciones.clear()
            # for conversacion in conversaciones:
            #     conversacion_obj, created = Conversacion.objects.get_or_create(
            #         **conversacion,
            #     )
            #     instance.conversaciones.add(conversacion_obj)
            instance.conversaciones.set(conversaciones)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ModeloDetailSerializer(ModeloSerializer):
    """Serializer for modelo detail objects."""

    class Meta(ModeloSerializer.Meta):
        fields = ModeloSerializer.Meta.fields + ('descripcion',)
