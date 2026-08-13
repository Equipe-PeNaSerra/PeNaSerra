import json

def carregar_dados_sistema(nome_arquivo_json):
    try:
        # Abre o arquivo em modo leitura ("r") com suporte a acentos (utf-8).
        with open(nome_arquivo_json, "r", encoding="utf-8") as banco_de_dados:
            # Lê o conteúdo do arquivo e retorna um dicionário mapeado.
            return json.load(banco_de_dados)
            
    except FileNotFoundError:
        # Cria e retorna um dicionário base estrutural vazio caso o arquivo não exista.
        print("Aviso: Banco de dados não encontrado. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}


    except json.JSONDecodeError:
        # Cria e retorna um dicionário base estrutural vazio caso o arquivo exista, mas possua o conteúdo corrompido ou escrito
        # de uma forma que não é um JSON válido.
        print("ERRO CRÍTICO: O arquivo do banco de dados está corrompido!")
        print("Iniciando um sistema vazio por segurança. Verifique o arquivo .json.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}
        