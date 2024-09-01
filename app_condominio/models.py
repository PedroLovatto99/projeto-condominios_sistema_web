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
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    cpf = models.CharField(max_length=11, verbose_name="CPF", null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", null=True, blank=True)
    foto = models.ImageField(upload_to="fotos", null=True, blank=True)

    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"

    def __str__(self):
        return self.nome + " - "+ str(self.apartamento)