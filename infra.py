import json


def carregar_dados_sistema(nome_arquivo_json):
    try:
        # Abre o arquivo JSON para leitura com codificação utf-8
        with open(nome_arquivo_json, "r", encoding="utf-8") as banco_de_dados:
            # Converte e retorna o JSON como um dicionário Python
            return json.load(banco_de_dados)

    except FileNotFoundError:
        # Retorna a estrutura base caso seja a primeira execução do sistema
        print("Aviso: Banco de dados não encontrado. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}

    except json.JSONDecodeError:
        # Retorna a estrutura base se o arquivo existir, mas estiver corrompido
        print("ERRO CRÍTICO: O arquivo do banco de dados está corrompido!")
        print("Iniciando um sistema vazio por segurança. Verifique o arquivo .json.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}

    except Exception as erro:
        # Fallback para evitar que o programa quebre por erros de leitura imprevistos
        print(f"Erro ao carregar os dados: {erro}. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}


def salvar_dados_sistema(nome_arquivo_json, dict_memoria):
    try:
        # Abre o arquivo para escrita (sobrescreve o atual ou cria um novo se não existir)
        with open(nome_arquivo_json, "w", encoding="utf-8") as banco_de_dados:
            # Salva o dicionário formatado e preservando a acentuação
            json.dump(dict_memoria, banco_de_dados, indent=4, ensure_ascii=False)

    except PermissionError:
        print("ERRO CRÍTICO: Permissão negada ao tentar salvar o arquivo.")
        print("Verifique se o arquivo .json não está aberto em outro programa ou bloqueado pelo sistema.")

    except TypeError:
        print("ERRO DE DADOS: O sistema tentou salvar um tipo de dado incompatível com JSON.")
        print("Verifique se não há objetos não suportados (como datas ou sets) armazenados na memória.")

    except Exception as erro:
        # Captura outras exceções para não interromper a execução do programa
        print(f"Erro ao salvar os dados: {erro}")