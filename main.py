import json # Remover
import time
import requests
import openpyxl
from openpyxl import Workbook
'''
def carregar_dados_ncms(caminho_arquivo_ncms_validar):
    with open(caminho_arquivo_ncms_validar, 'r', encoding='utf-8') as file:
        return json.load(file)
'''
def carregar_dados_ncms(url):
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro para respostas inválidas
    return response.json()

def otimizar_ncm_data(ncms_data):
    codigos_ncm = {}
    for item in ncms_data['Nomenclaturas']:
        if "Codigo" in item and "Descricao" in item:
            codigo_sem_pontos = item["Codigo"].replace('.', '').strip()
            if len(codigo_sem_pontos) == 8:
                codigos_ncm[codigo_sem_pontos] = item["Descricao"]
    return codigos_ncm

def validar_ncm(ncm, codigos_ncm):
    ncm_sem_pontos = ncm.replace('.', '').strip()
    if ncm_sem_pontos in codigos_ncm:
        return True, codigos_ncm[ncm_sem_pontos]
    else:
        return False, None

# Carregando base de NCMs da API do Siscomex para validação / Acessa o endereço da url e baixa um json
url_base_validacao = 'https://portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json'
ncms_data = carregar_dados_ncms(url_base_validacao)

# Carregando NCMs do Usuario
import os
relative_path = os.path.join(os.path.dirname(__file__), 'ncms_para_validar.txt')
arquivo_ncms_validar = open(relative_path)

# Medir o tempo de otimização dos dados
start_time = time.time()
codigos_ncm_otimizado = otimizar_ncm_data(ncms_data)
print(f"Tempo de otimização: {time.time() - start_time:.6f} segundos")

# Cria um novo workbook (arquivo Excel)
wb = Workbook()
# Seleciona a planilha ativa (por padrão, a primeira planilha)
planilha = wb.active

# Montando Cabeçalho
planilha['A1'] = 'NCM'
planilha['B1'] = 'DESCRIÇÃO'

# Medir o tempo de validação do NCM
start_time = time.time()

for ncm_para_validar in arquivo_ncms_validar.readlines():
    
    valido, descricao = validar_ncm(ncm_para_validar, codigos_ncm_otimizado)

    if len(ncm_para_validar.strip().replace('.', '')) > 0:
        if valido:
            dados_ncm = (ncm_para_validar.strip(), 'Consta na lista do Siscomex')
            planilha.append(dados_ncm)
        elif len(ncm_para_validar.strip().replace('.', '')) < 8 and len(ncm_para_validar.strip().replace('.', '')) > 0:
            dados_ncm = (ncm_para_validar.strip(), 'Não possui a quantidade minima de caracteres')
            planilha.append(dados_ncm)
        else:
            dados_ncm = (ncm_para_validar.strip(), 'Não consta na lista do Siscomex')
            planilha.append(dados_ncm)

print(f"Tempo de validação: {time.time() - start_time:.6f} segundos")

# Medir o tempo para gerar a planilha
start_time = time.time()
wb.save('planilha_exemplo.xlsx')
print(f"Tempo para gerar a Planilha: {time.time() - start_time:.6f} segundos")

if 'Data_Ultima_Atualizacao_NCM' in ncms_data:
    print(f"Vigencia da base de NCMs utilizada para validação: {ncms_data['Data_Ultima_Atualizacao_NCM']}")
else:
    print("A chave 'Data_Ultima_Atualizacao_NCM' não foi encontrada nos dados NCM.")