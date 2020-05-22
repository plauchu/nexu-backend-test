from rest_framework import serializers

class idModelsSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class betweenModelsSerializer(serializers.Serializer):
    greater = serializers.IntegerField()
    lower =serializers.IntegerField()

class ModelsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name =serializers.CharField(max_length=20)
