import fdb
from colors import colors

def carregar_dados_firebird(host, database, user, password):
    try:
        # Conectar ao banco de dados
        connection = fdb.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print(f"{colors["verde"]}Conexão bem-sucedida!{colors["branco"]}")
    except fdb.Error as e:
        print(f"{colors["vermelho"]}Erro ao conectar ao banco de dados: {e}{colors["branco"]}")
        exit(1)
    except Exception as e:
        print(f"\n\n{colors["vermelho"]}Erro desconhecido ao conectar ao banco de dados: {e}{colors["branco"]}")
        exit(1)

    # Criar um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Executar uma consulta 
    cursor.execute("select DISTINCT P.NCM from ESTOQUE_PRODUTO P")

    #Fechar conexão com BD
    ncms = cursor.fetchall()
    cursor.close()
    connection.close()
    print(f"{colors["amarelo"]}Conexão encerrada.{colors["branco"]}\n")

    return ncms
