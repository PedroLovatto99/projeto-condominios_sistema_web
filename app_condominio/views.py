from django.shortcuts import render
from .models import *
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import pandas as pd
from django.http import HttpResponse
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from io import BytesIO
import datetime
from babel.dates import format_datetime


@method_decorator(login_required(login_url='login'), name='dispatch')
class BlocosListView(ListView):
    model = Bloco
    template_name = "blocos-lista.html"
    context_object_name = "blocos"
    ordering = ['numero']

@method_decorator(login_required(login_url='login'), name='dispatch')
class BlocoDetail(DetailView):
    model = Bloco
    template_name = 'bloco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        apartamentos = Apartamento.objects.filter(bloco=self.object).order_by("numero")
        residentes = Residente.objects.filter(apartamento__in=apartamentos)
        
        for residente in residentes:
            residente.total_boleto = (residente.valor_aluguel or 0) + \
                                     (residente.valor_condominio or 0) + \
                                     (residente.valor_gas or 0) + \
                                     (residente.outros or 0)

        context['apartamentos'] = apartamentos
        context['residentes'] = residentes

        return context

def login_view(request):
    login_form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blocos_lista') 
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('login')


def gerar_excel(request, bloco_id):
    # Obter os apartamentos e residentes relacionados ao bloco
    apartamentos = Apartamento.objects.filter(bloco_id=bloco_id)
    residentes = Residente.objects.filter(apartamento__in=apartamentos)
    
    # Preparar os dados para o DataFrame
    data = []
    for apartamento in apartamentos:
        for residente in residentes:
            if residente.apartamento == apartamento:
                total_boleto = (residente.valor_aluguel or 0) + (residente.valor_condominio or 0) + (residente.valor_gas or 0) + (residente.outros or 0)
                
                entry = {
                    'Apartamento': apartamento.numero,
                    'Residente': residente.nome,
                    'Email': residente.email,
                    'Telefone': residente.telefone,
                    'Data Início Contrato': residente.data_inicio,
                    'Data Fim Contrato': residente.data_fim,
                    'Prorrogação': residente.prorrogacao,
                    'Número Cadastro': residente.numero_cadastro,
                    'Valor Aluguel': residente.valor_aluguel,
                    'Valor Condomínio': residente.valor_condominio,
                    'Outros Valores': residente.outros,
                    'Valor Gás': residente.valor_gas,
                    'Data Vencimento Boleto': residente.data_vencimento,
                    'Unidade Consumidora': residente.unidade_consumidora,
                    'Total Boleto': total_boleto, 
                }
                if request.user.is_superuser:
                    entry['CPF/CNPJ'] = residente.cpf_cnpj
                data.append(entry)

    # Criar o DataFrame com os dados
    df = pd.DataFrame(data)

    # Criar um buffer de memória
    buffer = BytesIO()
    
    # Gerar o arquivo Excel no buffer
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Bloco')
        
        # Obter o workbook
        workbook = writer.book
        worksheet = writer.sheets['Bloco']
        
        # Adicionar título com o número do bloco
        bloco = Bloco.objects.get(pk=bloco_id)
        worksheet.insert_rows(1)  # Inserir uma nova linha no topo
        worksheet.merge_cells('A1:O1')  # Mesclar células para o título, considerando todas as colunas
        worksheet['A1'] = f'Bloco {bloco.numero}'
        worksheet['A1'].font = Font(bold=True, size=16, color="000000")  # Negrito, tamanho 16, cor preta
        worksheet['A1'].alignment = Alignment(horizontal='center', vertical='center')
        worksheet['A1'].fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")  # Cor de fundo

        # Ajustar a largura das colunas
        worksheet.column_dimensions['A'].width = 15  # Apartamento
        worksheet.column_dimensions['B'].width = 20  # Residente
        worksheet.column_dimensions['C'].width = 30  # Email
        worksheet.column_dimensions['D'].width = 20  # Telefone
        worksheet.column_dimensions['E'].width = 20  # Data Início Contrato
        worksheet.column_dimensions['F'].width = 20  # Data Fim Contrato
        worksheet.column_dimensions['G'].width = 20  # Prorrogação
        worksheet.column_dimensions['H'].width = 20  # Número Cadastro
        worksheet.column_dimensions['I'].width = 20  # Valor Aluguel
        worksheet.column_dimensions['J'].width = 20  # Valor Condomínio
        worksheet.column_dimensions['K'].width = 20  # Outros Valores
        worksheet.column_dimensions['L'].width = 20  # Valor Gás
        worksheet.column_dimensions['M'].width = 20  # Data Vencimento Boleto
        worksheet.column_dimensions['N'].width = 30  # Unidade Consumidora
        worksheet.column_dimensions['O'].width = 20  # Total Boleto
        if 'CPF/CNPJ' in df.columns:
            worksheet.column_dimensions['P'].width = 20  # CPF/CNPJ

        # Formatação do cabeçalho
        header_font = Font(bold=True, color="FFFFFF")
        header_alignment = Alignment(horizontal='center', vertical='center')
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        
        for cell in worksheet["2:2"]:  # A linha do cabeçalho após o título
            cell.font = header_font
            cell.alignment = header_alignment
            cell.fill = header_fill
        
        # Bordas para as células
        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))

        for row in worksheet.iter_rows(min_row=2):  # Aplicar bordas a partir da segunda linha
            for cell in row:
                cell.border = thin_border

    # Configurar a resposta HTTP com o conteúdo do buffer
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Bloco_{bloco_id}.xlsx"'
    
    return response

def gerar_excel_todos_blocos(request):
    # Obter todos os blocos
    blocos = Bloco.objects.all()

    # Criar um buffer de memória
    buffer = BytesIO()

    # Gerar o arquivo Excel no buffer
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for bloco in blocos:
            # Filtrar os apartamentos e residentes correspondentes ao bloco atual
            apartamentos = Apartamento.objects.filter(bloco=bloco)
            residentes = Residente.objects.filter(apartamento__in=apartamentos)
            
            data = []
            
            # Iterar sobre os apartamentos e residentes correspondentes
            for apartamento in apartamentos:
                for residente in residentes:
                    if residente.apartamento == apartamento:
                        total_boleto = (residente.valor_aluguel or 0) + (residente.valor_condominio or 0) + (residente.valor_gas or 0) + (residente.outros or 0)

                        # Organizar as informações na ordem desejada
                        entry = {
                            'Apartamento': apartamento.numero,
                            'Residente': residente.nome,
                            'CPF/CNPJ': residente.cpf_cnpj if request.user.is_superuser else None,  # Adicionar CPF/CNPJ aqui
                            'Email': residente.email,
                            'Telefone': residente.telefone,
                            'Data Início Contrato': residente.data_inicio,
                            'Data Fim Contrato': residente.data_fim,
                            'Prorrogação': residente.prorrogacao,
                            'Número Cadastro': residente.numero_cadastro,
                            'Valor Aluguel': residente.valor_aluguel,
                            'Valor Condomínio': residente.valor_condominio,
                            'Outros Valores': residente.outros,
                            'Valor Gás': residente.valor_gas,
                            'Data Vencimento Boleto': residente.data_vencimento,
                            'Unidade Consumidora': residente.unidade_consumidora,
                            'Total Boleto': total_boleto,  # Adicionar o total individual do boleto
                        }
                        data.append(entry)
            
            # Criar o DataFrame para o bloco atual
            if data:  # Verificar se há dados a serem inseridos
                df = pd.DataFrame(data)

                # Adicionar os dados à planilha
                df.to_excel(writer, index=False, sheet_name=f'Bloco {bloco.numero}')

                # Obter a aba ativa (sheet) para formatar
                worksheet = writer.sheets[f'Bloco {bloco.numero}']
                
                # Adicionar título
                worksheet.insert_rows(1)  # Inserir uma nova linha no topo
                worksheet.merge_cells('A1:P1')  # Mesclar células para o título
                worksheet['A1'] = f'Bloco {bloco.numero}'
                worksheet['A1'].font = Font(bold=True, size=16, color="000000")  # Negrito, tamanho 16, cor preta
                worksheet['A1'].alignment = Alignment(horizontal='center', vertical='center')  # Centralizar texto
                worksheet['A1'].fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")  # Cor de fundo

                # Ajustar a largura das colunas
                worksheet.column_dimensions['A'].width = 15  # Apartamento
                worksheet.column_dimensions['B'].width = 20  # Residente
                worksheet.column_dimensions['C'].width = 20  # CPF/CNPJ
                worksheet.column_dimensions['D'].width = 30  # Email
                worksheet.column_dimensions['E'].width = 20  # Telefone
                worksheet.column_dimensions['F'].width = 20  # Data Início Contrato
                worksheet.column_dimensions['G'].width = 20  # Data Fim Contrato
                worksheet.column_dimensions['H'].width = 20  # Prorrogação
                worksheet.column_dimensions['I'].width = 20  # Número Cadastro
                worksheet.column_dimensions['J'].width = 20  # Valor Aluguel
                worksheet.column_dimensions['K'].width = 20  # Valor Condomínio
                worksheet.column_dimensions['L'].width = 20  # Outros Valores
                worksheet.column_dimensions['M'].width = 20  # Valor Gás
                worksheet.column_dimensions['N'].width = 20  # Data Vencimento Boleto
                worksheet.column_dimensions['O'].width = 30  # Unidade Consumidora
                worksheet.column_dimensions['P'].width = 20  # Total Boleto

                # Formatação do cabeçalho
                header_font = Font(bold=True, color="FFFFFF")
                header_alignment = Alignment(horizontal='center', vertical='center')  # Centralizar cabeçalhos
                header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                
                for cell in worksheet["2:2"]:  # A linha do cabeçalho após o título
                    cell.font = header_font
                    cell.alignment = header_alignment
                    cell.fill = header_fill
                
                # Bordas para as células
                thin_border = Border(left=Side(style='thin'),
                                     right=Side(style='thin'),
                                     top=Side(style='thin'),
                                     bottom=Side(style='thin'))

                for row in worksheet.iter_rows(min_row=2):  # Aplicar bordas a partir da segunda linha
                    for cell in row:
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='center')  # Centralizar o conteúdo das células

    # Obter data atual para nomear o arquivo
    now = datetime.datetime.now()
    nome_mes = format_datetime(now, "MMMM", locale='pt_BR')  # Nome do mês em português
    ano = now.year  # Ano atual

    # Configurar a resposta HTTP com o conteúdo do buffer
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Planilhas - Blocos | {nome_mes} de {ano}.xlsx"'
    
    return response