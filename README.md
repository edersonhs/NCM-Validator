# Validador de NCM com Integração ao Firebird e API do Siscomex
 
Este projeto é um validador de NCM (Nomenclatura Comum do Mercosul) que verifica a validade dos códigos NCM consultando a API do Siscomex. Inicialmente, o script lia os NCMs de um arquivo, mas agora ele se conecta diretamente a um banco de dados Firebird para buscar os códigos NCM de um sistema empresarial.

## Funcionalidades
- Conexão com a API do Siscomex: Obtém um JSON com todos os NCMs válidos.
- Tratamento do JSON: Extrai os NCMs válidos e os armazena em uma lista.
- Conexão com o Firebird: Realiza uma consulta (SELECT) no banco de dados para obter os NCMs cadastrados.
- Validação de NCMs: Compara os NCMs do banco de dados com a lista de NCMs válidos.

## Tecnologias Utilizadas
- Python
- API do Siscomex
- Firebird (acesso ao banco de dados)
- Bibliotecas de conexão ao Firebird (fdb)
- Bibliotecas para requisições HTTP (requests para acessar a API)
- Bibliotecas para gerar saída em excel (openpyxl)

# Como Funciona
- O script se conecta à API do Siscomex e obtém um JSON com todos os NCMs válidos.
- O JSON é tratado para extrair os NCMs válidos, que são armazenados em uma lista.
- O script se conecta ao banco de dados Firebird e realiza uma consulta (SELECT DISTINCT) para obter os NCMs cadastrados.
- Cada NCM do banco de dados é comparado com a lista de NCMs válidos.
- O resultado da validação é salvo em uma planilha, especificando quais NCMs são validos e quais não constam na lista de NCMs.
- O script não valida a data final de vigencia dos NCMs, apesar de a api retornar esta informação, consideranndo que no momento em que foi desennvolvido, nenhum dos NCMs tinha uma previsão concreta de vencimento.

# Casos de Uso
- Validação de NCMs em sistemas empresariais que utilizam Firebird.
- Automação de processos de verificação de NCMs para evitar erros fiscais.
- Integração com sistemas legados que já utilizam o Firebird.

# Como Contribuir
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests.
