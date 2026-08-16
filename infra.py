import json
from pathlib import Path


def carregar_dados_sistema(nome_arquivo_json):
    # Cria o objeto Path a partir do nome do arquivo
    arquivo = Path(nome_arquivo_json)
    
    try:
        # read_text() abre, lê todo o conteúdo como string e fecha o arquivo automaticamente
        conteudo = arquivo.read_text(encoding="utf-8")
        
        # json.loads (load string) converte o texto lido para o dicionário Python
        return json.loads(conteudo)

    except FileNotFoundError:
        print("Aviso: Banco de dados não encontrado. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}

    except json.JSONDecodeError:
        print("ERRO CRÍTICO: O arquivo do banco de dados está corrompido!")
        print("Iniciando um sistema vazio por segurança. Verifique o arquivo .json.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}

    except Exception as erro:
        print(f"Erro ao carregar os dados: {erro}. Iniciando um novo sistema vazio.")
        return {"trilhas": {}, "participantes": {}, "guias": {}}


def salvar_dados_sistema(nome_arquivo_json, dict_memoria):
    # Cria o objeto Path a partir do nome do arquivo
    arquivo = Path(nome_arquivo_json)
    
    try:
        # json.dumps (dump string) converte o dicionário para uma string formatada
        texto_json = json.dumps(dict_memoria, indent=4, ensure_ascii=False)
        
        # write_text() abre, escreve a string e fecha o arquivo automaticamente
        arquivo.write_text(texto_json, encoding="utf-8")

    except PermissionError:
        print("ERRO CRÍTICO: Permissão negada ao tentar salvar o arquivo.")
        print("Verifique se o arquivo .json não está aberto em outro programa ou bloqueado pelo sistema.")

    except TypeError:
        print("ERRO DE DADOS: O sistema tentou salvar um tipo de dado incompatível com JSON.")
        print("Verifique se não há objetos não suportados (como datas ou sets) armazenados na memória.")

    except Exception as erro:
        print(f"Erro ao salvar os dados: {erro}")