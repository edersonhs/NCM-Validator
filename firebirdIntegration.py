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
        print(f"{colors["verde"]}Conexão ao banco de dados bem-sucedida!{colors["branco"]}")
    except fdb.Error as e:
        print(f"{colors["vermelho"]}Erro ao conectar ao banco de dados: {e}{colors["branco"]}")
        exit(1)
    except Exception as e:
        print(f"\n\n{colors["vermelho"]}Erro desconhecido ao conectar ao banco de dados: {e}{colors["branco"]}")
        exit(1)

    # Criar um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Executar uma consulta 
    cursor.execute("SELECT DISTINCT P.NCM FROM ESTOQUE_PRODUTO P WHERE P.ATIVO = 'S' AND P.NCM IS NOT NULL")

    #Fechar conexão com BD
    ncms = cursor.fetchall()
    cursor.close()
    connection.close()
    print(f"{colors["vermelho"]}Conexão ao banco de dados encerrada.{colors["branco"]}\n")

    return ncms
