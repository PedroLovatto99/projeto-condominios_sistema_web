from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Bloco, Apartamento, Residente


class ResidenteAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'apartamento', 'cpf_cnpj', 'telefone', 'email')
    list_filter = ('apartamento__bloco',)
    # history_list_display = ('history_date', 'history_type', 'history_user')


class ApartamentoAdmin(SimpleHistoryAdmin):
    list_display = ('numero', 'bloco')
    list_filter = ('bloco', 'numero')


class BlocoAdmin(SimpleHistoryAdmin):
    list_display = ('numero', 'cor')


admin.site.register(Bloco, BlocoAdmin)
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Residente, ResidenteAdmin)
