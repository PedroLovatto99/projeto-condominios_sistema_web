from django.db import models


class Bloco(models.Model):
    numero = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Bloco"
        verbose_name_plural = "Blocos"

    def __str__(self):
        return "Bloco " + str(self.numero)

class Apartamento(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.PROTECT)
    numero = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"

    def __str__(self):
        return "Apartamento " + str(self.numero) + " - " + str(self.bloco)

class Residente(models.Model):
    nome = models.CharField(max_length=100)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT)
    cpf_cnpj = models.CharField(verbose_name="CPF/CNPJ", max_length=18, null=True, blank=True)
    telefone = models.CharField(verbose_name="Telefone", max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", null=True, blank=True)
    data_inicio = models.DateField(verbose_name="Data de Início do contrato", null=True, blank=True)
    data_fim = models.DateField(verbose_name="Data de Término do contrato", null=True, blank=True)
    prorrogacao = models.DateField(verbose_name="Data de Prorrogação do Contrato", null=True, blank=True)
    numero_cadastro = models.IntegerField(verbose_name="Numero de Cadastro", null=True, blank=True)
    valor_aluguel = models.FloatField(verbose_name="Valor do Aluguel", null=True, blank=True)
    valor_condominio = models.FloatField(verbose_name="Valor do Condomínio", null=True, blank=True)
    outros = models.FloatField(verbose_name="Outros valores a pagar", null=True, blank=True)
    valor_gas = models.FloatField(verbose_name="Valor do Gás", null=True, blank=True)
    data_vencimento = models.DateField(verbose_name="Data de Vencimento do boleto", null=True, blank=True)
    unidade_consumidora = models.CharField(verbose_name="Unidade Consumidora", null=True, blank=True, max_length=100)
    
    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"

    def __str__(self):
        return self.nome + " - "+ str(self.apartamento)