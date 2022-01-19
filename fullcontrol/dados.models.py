# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aigefcop(models.Model):
    fco_empresa = models.OneToOneField('Aigeramp', models.DO_NOTHING, db_column='fco_empresa', primary_key=True)
    fco_fco = models.DecimalField(max_digits=15, decimal_places=0)
    fco_eclien = models.CharField(max_length=1, blank=True, null=True)
    fco_eforne = models.CharField(max_length=1, blank=True, null=True)
    fco_etrans = models.CharField(max_length=1, blank=True, null=True)
    fco_erural = models.CharField(max_length=1, blank=True, null=True)
    fco_eoutro = models.CharField(max_length=1, blank=True, null=True)
    fco_jurfis = models.CharField(max_length=1, blank=True, null=True)
    fco_nome = models.CharField(max_length=55, blank=True, null=True)
    fco_nomred = models.CharField(max_length=30, blank=True, null=True)
    fco_usado = models.CharField(max_length=1, blank=True, null=True)
    fco_cnpj = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    fco_inscr = models.CharField(max_length=15, blank=True, null=True)
    fco_cep = models.IntegerField(blank=True, null=True)
    fco_tipo = models.CharField(max_length=10, blank=True, null=True)
    fco_endereco = models.CharField(max_length=50, blank=True, null=True)
    fco_endnum = models.IntegerField(blank=True, null=True)
    fco_compleme = models.CharField(max_length=20, blank=True, null=True)
    fco_bairro = models.CharField(max_length=40, blank=True, null=True)
    fco_munic = models.IntegerField(blank=True, null=True)
    fco_cidade = models.CharField(max_length=40, blank=True, null=True)
    fco_uf = models.CharField(max_length=2, blank=True, null=True)
    fco_paisfiller = models.SmallIntegerField(blank=True, null=True)
    fco_cxpost = models.IntegerField(blank=True, null=True)
    fco_ddd = models.SmallIntegerField(blank=True, null=True)
    fco_numtel = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fco_ddd1 = models.SmallIntegerField(blank=True, null=True)
    fco_numtel1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fco_dddcel = models.SmallIntegerField(blank=True, null=True)
    fco_numcel = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fco_dddfax = models.SmallIntegerField(blank=True, null=True)
    fco_numtelfax = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fco_email = models.CharField(max_length=50, blank=True, null=True)
    fco_homepage = models.CharField(max_length=50, blank=True, null=True)
    fco_ramo = models.SmallIntegerField(blank=True, null=True)
    fco_transp = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    fco_tranrd = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    fco_grupo = models.IntegerField(blank=True, null=True)
    fco_rg = models.CharField(max_length=20, blank=True, null=True)
    fco_orgexp_rg = models.CharField(max_length=10, blank=True, null=True)
    fco_uf_rg = models.CharField(max_length=2, blank=True, null=True)
    fco_favorecido = models.CharField(max_length=55, blank=True, null=True)
    fco_habcred = models.CharField(max_length=1, blank=True, null=True)
    fco_idioma = models.SmallIntegerField(blank=True, null=True)
    fco_nit = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True)
    fco_maxfat = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    fco_dtnasc = models.IntegerField(blank=True, null=True)
    fco_taman = models.CharField(max_length=3, blank=True, null=True)
    fco_simpl = models.CharField(max_length=2, blank=True, null=True)
    fco_zfranca = models.CharField(max_length=1, blank=True, null=True)
    fco_suframa = models.CharField(max_length=12, blank=True, null=True)
    fco_percicm = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fco_serie = models.CharField(max_length=3, blank=True, null=True)
    fco_opfsai = models.SmallIntegerField(blank=True, null=True)
    fco_opfent = models.SmallIntegerField(blank=True, null=True)
    fco_almox = models.IntegerField(blank=True, null=True)
    fco_montadora = models.CharField(max_length=1, blank=True, null=True)
    fco_mensa = models.IntegerField(blank=True, null=True)
    fco_repre = models.IntegerField(blank=True, null=True)
    fco_gerencia = models.SmallIntegerField(blank=True, null=True)
    fco_condpg = models.SmallIntegerField(blank=True, null=True)
    fco_tabpre = models.IntegerField(blank=True, null=True)
    fco_usapoc = models.CharField(max_length=1, blank=True, null=True)
    fco_credito = models.CharField(max_length=2, blank=True, null=True)
    fco_limcred = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    fco_fatura = models.CharField(max_length=1, blank=True, null=True)
    fco_encfin = models.SmallIntegerField(blank=True, null=True)
    fco_sitcob = models.SmallIntegerField(blank=True, null=True)
    fco_banco = models.SmallIntegerField(blank=True, null=True)
    fco_agencia = models.CharField(max_length=6, blank=True, null=True)
    fco_ccorrente = models.CharField(max_length=12, blank=True, null=True)
    fco_usuar = models.CharField(max_length=12, blank=True, null=True)
    fco_data = models.IntegerField(blank=True, null=True)
    fco_datasin = models.IntegerField(blank=True, null=True)
    fco_telas = models.CharField(max_length=6, blank=True, null=True)
    fco_observ = models.CharField(max_length=50, blank=True, null=True)
    fco_for_plajax = models.SmallIntegerField(blank=True, null=True)
    fco_flag = models.CharField(max_length=1, blank=True, null=True)
    fco_iso = models.CharField(max_length=1, blank=True, null=True)
    fco_qs = models.CharField(max_length=1, blank=True, null=True)
    fco_filler_gq = models.CharField(max_length=1, blank=True, null=True)
    fco_filler_em = models.CharField(max_length=1, blank=True, null=True)
    fco_cobicms = models.CharField(max_length=1, blank=True, null=True)
    fco_limita = models.CharField(max_length=1, blank=True, null=True)
    fco_novo = models.CharField(max_length=1, blank=True, null=True)
    fco_sgrupo = models.IntegerField(blank=True, null=True)
    fco_mercado = models.CharField(max_length=1, blank=True, null=True)
    fco_eintegrado = models.CharField(max_length=1, blank=True, null=True)
    fco_eprodutor = models.CharField(max_length=1, blank=True, null=True)
    fco_earmazem = models.CharField(max_length=1, blank=True, null=True)
    fco_etecnico = models.CharField(max_length=1, blank=True, null=True)
    fco_eincubat = models.CharField(max_length=1, blank=True, null=True)
    fco_insrur = models.CharField(max_length=20, blank=True, null=True)
    fco_imprimir = models.CharField(max_length=1, blank=True, null=True)
    fco_serasa = models.CharField(max_length=1, blank=True, null=True)
    fco_dataser = models.IntegerField(blank=True, null=True)
    fco_numserasa = models.CharField(max_length=10, blank=True, null=True)
    fco_codfco_importado = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    fco_senha = models.CharField(max_length=32, blank=True, null=True)
    fco_reclama = models.CharField(max_length=18, blank=True, null=True)
    fco_dataser_env = models.IntegerField(blank=True, null=True)
    fco_tipofd = models.CharField(max_length=1, blank=True, null=True)
    fco_tabfixa = models.SmallIntegerField(blank=True, null=True)
    fco_filler_modnf = models.SmallIntegerField(blank=True, null=True)
    fco_libnrf = models.CharField(max_length=1, blank=True, null=True)
    fco_libcon = models.CharField(max_length=1, blank=True, null=True)
    fco_libreq = models.CharField(max_length=1, blank=True, null=True)
    fco_libchq = models.CharField(max_length=1, blank=True, null=True)
    fco_modelonf = models.SmallIntegerField(blank=True, null=True)
    fco_cfrete = models.SmallIntegerField(blank=True, null=True)
    fco_dataval = models.IntegerField(blank=True, null=True)
    fco_lucro = models.CharField(max_length=1, blank=True, null=True)
    fco_contrib_ie = models.CharField(max_length=1, blank=True, null=True)
    fco_ignora_dtent = models.CharField(max_length=1, blank=True, null=True)
    fco_liquida_tudo = models.CharField(max_length=1, blank=True, null=True)
    fco_separa_pedcli = models.CharField(max_length=1, blank=True, null=True)
    fco_apaga_previte = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aigefcop'
        unique_together = (('fco_empresa', 'fco_fco'), ('fco_empresa', 'fco_grupo', 'fco_fco'),)


class Aigeramp(models.Model):
    ram_empresa = models.OneToOneField('Savemdip', models.DO_NOTHING, db_column='ram_empresa', primary_key=True)
    ram_ramo = models.SmallIntegerField()
    ram_descr = models.CharField(max_length=40, blank=True, null=True)
    ram_grupo = models.IntegerField(blank=True, null=True)
    ram_filler = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aigeramp'
        unique_together = (('ram_empresa', 'ram_ramo'),)

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