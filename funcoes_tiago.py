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

    except Exception as erro:
        # Tratamento genérico para não fechar o programa por erros inesperados.
        print(
            f"Erro ao carregar os dados: {erro}. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}


def salvar_dados_sistema(nome_arquivo_json, dict_memoria):
    # Abre o arquivo em modo escrita ("w") com suporte a acentos (utf-8).
    # Se o arquivo não existir, ele será criado automaticamente.
    try:
        with open(nome_arquivo_json, "w", encoding="utf-8") as banco_de_dados:
            # Converte o dicionário da memória para texto JSON e salva no arquivo.
            # indent=4 propicia a quebra de linhas e adiciona espaços antes de cada chave,
            # garantindo legibilidade e organização no documento.
            # ensure_ascii=False garante a visualização correta da acentuação dentro do documento.
            json.dump(dict_memoria, banco_de_dados,
                      indent=4, ensure_ascii=False)

    except PermissionError:
        print("ERRO CRÍTICO: Permissão negada ao tentar salvar o arquivo.")
        print("Verifique se o arquivo .json não está aberto em outro programa ou bloqueado pelo sistema.")

    except TypeError:
        print(
            "ERRO DE DADOS: O sistema tentou salvar um tipo de dado incompatível com JSON.")
        print("Verifique se não há objetos não suportados (como datas ou sets) armazenados na memória.")

    except Exception as erro:
        # Tratamento genérico para não fechar o programa por erros inesperados.
        print(f"Erro ao salvar os dados: {erro}")
