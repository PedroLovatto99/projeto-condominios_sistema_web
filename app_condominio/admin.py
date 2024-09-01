from django.contrib import admin
from .models import *


class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'apartamento', 'data_nascimento', 'cpf', 'email')

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bloco')

admin.site.register(Bloco)
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Residente, ResidenteAdmin)
