from django.contrib import admin
from .models import *
from django.forms import TextInput


class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'apartamento', 'cpf_cnpj', 'telefone', 'email')
    list_filter = ('apartamento__bloco',)

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('bloco','numero')
    list_filter = ('bloco','numero')

class BlocoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cor')

admin.site.register(Bloco, BlocoAdmin)
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Residente, ResidenteAdmin)
