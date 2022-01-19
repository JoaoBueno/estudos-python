from rest_framework import viewsets
from dados.api import serializers
from dados import models

class DadosViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DadosSerializer
    queryset = models.Savemdip.objects.all()