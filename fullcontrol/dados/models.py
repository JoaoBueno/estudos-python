# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Savemdip(models.Model):
    em_codigo = models.SmallIntegerField(primary_key=True)
    em_razsoc = models.CharField(max_length=40, blank=True, null=True)
    em_fanta = models.CharField(max_length=16, blank=True, null=True)
    em_endereco = models.CharField(max_length=40, blank=True, null=True)
    em_bairro = models.CharField(max_length=20, blank=True, null=True)
    em_cidade = models.CharField(max_length=20, blank=True, null=True)
    em_estado = models.CharField(max_length=2, blank=True, null=True)
    em_cep = models.IntegerField(blank=True, null=True)
    em_cgc = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    em_inscr = models.CharField(max_length=15, blank=True, null=True)
    em_jucesp = models.IntegerField(blank=True, null=True)
    em_data = models.IntegerField(blank=True, null=True)
    em_ddd = models.SmallIntegerField(blank=True, null=True)
    em_telefone = models.IntegerField(blank=True, null=True)
    em_fax = models.IntegerField(blank=True, null=True)
    em_digin = models.SmallIntegerField(blank=True, null=True)
    em_qtdig = models.SmallIntegerField(blank=True, null=True)
    em_palav = models.CharField(max_length=12, blank=True, null=True)
    em_senha = models.IntegerField(blank=True, null=True)
    em_tipo = models.CharField(max_length=1, blank=True, null=True)
    em_endnum = models.IntegerField(blank=True, null=True)
    em_release_log = models.SmallIntegerField(blank=True, null=True)
    em_release_param = models.SmallIntegerField(blank=True, null=True)
    em_pais = models.CharField(max_length=2, blank=True, null=True)
    em_filler = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'savemdip'
