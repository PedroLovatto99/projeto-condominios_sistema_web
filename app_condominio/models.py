from django.db import models


class Bloco(models.Model):
    CORES_SELECT = [
        ("#FFD700", "Amarelo"),
        ("#1F497D", "Azul"),
        ("#00B050", "Verde"),
    ]
    numero = models.PositiveIntegerField(verbose_name="Número")
    cor = models.CharField(max_length=7, choices=CORES_SELECT)

    class Meta:
        verbose_name = "Bloco"
        verbose_name_plural = "Blocos"

    def __str__(self):
        return "Bloco " + str(self.numero)

class Apartamento(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.PROTECT)
    numero = models.PositiveIntegerField(verbose_name="Número")

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"

    def __str__(self):
        return "Apartamento " + str(self.numero) + " - " + str(self.bloco)

class Residente(models.Model):
    nome = models.CharField(max_length=100)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT)
    cpf_cnpj = models.CharField(verbose_name="CPF/CNPJ", max_length=18)
    telefone = models.CharField(verbose_name="Telefone", max_length=15)
    email = models.EmailField(verbose_name="E-mail")
    data_inicio = models.DateField(verbose_name="Data de Início do contrato")
    data_fim = models.DateField(verbose_name="Data de Término do contrato")
    prorrogacao = models.DateField(verbose_name="Data de Prorrogação do Contrato", null=True, blank=True)
    numero_cadastro = models.IntegerField(verbose_name="Numero de Cadastro")
    valor_aluguel = models.FloatField(verbose_name="Valor do Aluguel")
    valor_condominio = models.FloatField(verbose_name="Valor do Condomínio")
    outros = models.FloatField(verbose_name="Outros valores a pagar", null=True, blank=True)
    valor_gas = models.FloatField(verbose_name="Valor do Gás", null=True, blank=True)
    data_vencimento = models.DateField(verbose_name="Data de Vencimento do boleto", null=True, blank=True)
    unidade_consumidora = models.CharField(verbose_name="Unidade Consumidora", null=True, blank=True, max_length=100)
    
    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"

    def __str__(self):
        return self.nome + " - "+ str(self.apartamento)