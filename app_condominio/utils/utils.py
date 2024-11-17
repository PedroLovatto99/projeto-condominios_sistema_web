import datetime
from app_condominio.models import HistoricoMensal, Apartamento, Residente

def salvar_historico_mensal(bloco, user):
    hoje = datetime.date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # Verificar se já existe um histórico para o mês atual
    if HistoricoMensal.objects.filter(bloco=bloco, mes=mes_atual, ano=ano_atual).exists():
        return  # Evitar salvar múltiplas vezes para o mesmo mês

    # Capturar o estado atual da tabela
    apartamentos = Apartamento.objects.filter(bloco=bloco)
    residentes = Residente.objects.filter(apartamento__in=apartamentos)

    dados = []
    for apartamento in apartamentos:
        residentes_apartamento = [
            {
                'nome': residente.nome,
                'cpf_cnpj': residente.cpf_cnpj,
                'telefone': residente.telefone,
                'email': residente.email,
                'data_inicio': str(residente.data_inicio),
                'data_fim': str(residente.data_fim),
                'valor_aluguel': residente.valor_aluguel,
                'valor_condominio': residente.valor_condominio,
                'outros': residente.outros,
                'valor_gas': residente.valor_gas,
                'total_boleto': residente.total_boleto,
                'data_vencimento': str(residente.data_vencimento),
                'unidade_consumidora': residente.unidade_consumidora,
            }
            for residente in residentes if residente.apartamento == apartamento
        ]
        dados.append({
            'apartamento': apartamento.numero,
            'residentes': residentes_apartamento,
        })

    # Salvar no modelo HistoricoMensal
    HistoricoMensal.objects.create(
        bloco=bloco,
        mes=mes_atual,
        ano=ano_atual,
        dados=dados,
        criado_por=user
    )
