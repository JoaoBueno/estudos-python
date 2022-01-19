from rest_framework import serializers
from dados import models

class DadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Savemdip
        fields = '__all__'
