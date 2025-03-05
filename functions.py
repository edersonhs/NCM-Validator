import requests
from time import time
from colors import colors

def carregar_dados_ncms(url):
    print(f"{colors["branco"]}Carregando dados da API do Siscomex...")
    start_time = time()
    response = requests.get(url)
    print(f"{colors["branco"]}Os dados foram carregados em  {time() - start_time:.6f} segundos\n")
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

def ler_arquivo(arquivo_config):
    try:
        with open(arquivo_config, 'r') as file:
            path = file.readline().strip() # .strip(): Remove espaços e quebras de linha

            if path.count(':') == 1: # path para acesso em rede local
                return 'localhost', path
            elif path.count(':') == 2: # path para acesso em rede
                # Extrai o host (tudo antes do primeiro ':')
                host = path[:path.find(':')]
                # Extrai o resto do path (tudo após o primeiro ':')
                path_bd = path[path.find(':') + 1:]
                 
                return host, path_bd
            else:
                print(f"{colors["vermelho"]}Erro ao carregar o arquivo de configuração. Verifique se o arquivo Sistema_Dir.cfg está correto.{colors["branco"]}")
                input(f"\n{colors['azulCiano']}Pressione Enter para sair...")
                exit(1)       
    except Exception as e:
            print(f"{colors["vermelho"]}Erro ao ler arquivo de configuração: {e}{colors["branco"]}")
            exit(1)
