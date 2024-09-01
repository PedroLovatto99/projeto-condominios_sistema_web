from django.shortcuts import render
from .models import *
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from io import BytesIO
import openpyxl

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
        
        
        paginator = Paginator(apartamentos, 6)
        page = self.request.GET.get('page')
        
        try:
            apartamentos_paginados = paginator.page(page)
        except PageNotAnInteger:
            apartamentos_paginados = paginator.page(1)
        except EmptyPage:
            apartamentos_paginados = paginator.page(paginator.num_pages)

        context['apartamentos'] = apartamentos_paginados
        context['residentes'] = Residente.objects.filter(apartamento__in=apartamentos_paginados)

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
                entry = {
                    'Apartamento': apartamento.numero,
                    'Residente': residente.nome,
                    'Email': residente.email,
                }
                if request.user.is_superuser:
                    entry['CPF'] = residente.cpf
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
        worksheet.merge_cells('A1:D1')  # Mesclar células para o título
        worksheet['A1'] = f'Bloco {bloco.numero}'
        worksheet['A1'].font = Font(bold=True, size=16, color="000000")  # Negrito, tamanho 16, cor preta
        worksheet['A1'].alignment = Alignment(horizontal='center', vertical='center')
        worksheet['A1'].fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")  # Cor de fundo

        # Ajustar a largura das colunas
        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 20
        worksheet.column_dimensions['C'].width = 30  # Ajuste conforme necessário
        if 'CPF' in df.columns:
            worksheet.column_dimensions['D'].width = 20
        worksheet.column_dimensions['E'].width = 30

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