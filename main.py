import time
from openpyxl import Workbook
from firebirdIntegration import carregar_dados_firebird
from functions import carregar_dados_ncms, otimizar_ncm_data, validar_ncm, ler_arquivo
from colors import colors

# Carregando base de NCMs da API do Siscomex para validação
url_base_validacao = 'https://portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json'
ncms_data = carregar_dados_ncms(url_base_validacao)

path_bd = ler_arquivo('Config\\Sistema_Dir.cfg')
ncms = carregar_dados_firebird('localhost', path_bd, 'sysdba', 'masterkey')

ncms_bd_validar = []

for ncm in ncms:
    if ncm[0] is not None:
        ncms_bd_validar.append(f"{ncm[0].strip()}")  # Remove espaços em branco

# Medir o tempo de otimização dos dados da API
start_time = time.time()
codigos_ncm_otimizado = otimizar_ncm_data(ncms_data)
print(f"Tempo de otimização:          {time.time() - start_time:10.6f} segundos")

# Cria um novo workbook (arquivo Excel)
wb = Workbook()
# Seleciona a planilha ativa (por padrão, a primeira planilha)
planilha = wb.active
# Montando Cabeçalho
planilha['A1'] = 'NCM'
planilha['B1'] = 'DESCRIÇÃO'

# Medir o tempo de validação do NCM
start_time = time.time()
# Inicia Validação
for ncm_para_validar in ncms_bd_validar:
    
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

print(f"Tempo de validação:           {time.time() - start_time:10.6f} segundos")

# Medir o tempo para gerar a planilha
start_time = time.time()
wb.save('planilha_exemplo.xlsx')
print(f"Tempo para gerar a Planilha:  {time.time() - start_time:10.6f} segundos")

if 'Data_Ultima_Atualizacao_NCM' in ncms_data:
    print(f"\n{colors["roxo"]}Vigencia da base de NCMs utilizada para validação: {ncms_data['Data_Ultima_Atualizacao_NCM']}{colors["branco"]}")
else:
    print(f"{colors["vermelho"]}A chave 'Data_Ultima_Atualizacao_NCM' não foi encontrada.{colors["branco"]}")

input(f"\n{colors["azulCiano"]}Pressione Enter para sair...")
