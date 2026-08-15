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


def autenticar_usuario(id_usuario, dict_memoria):
    # Converte o ID numérico para string para buscar nas chaves do JSON
    id_usuario = str(id_usuario)
    
    # Verifica em qual base o ID se encontra e retorna o perfil correspondente
    if id_usuario in dict_memoria["participantes"]:
        return "Trilheiro"
    elif id_usuario in dict_memoria["guias"]:
        return "Guia"
    else:
        return None


def receber_usuario():
    # Mantém o usuário preso no loop até que digite um ID válido
    while True:
        try:
            # Tenta converter a entrada direto para inteiro
            id_usuario = int(input("Digite seu ID de usuário: "))
            break
        except ValueError:
            # Disparado se a conversão falhar (ex: letras ou símbolos digitados)
            print("ERRO: Formato de ID inválido. O ID é composto somente por números!")
            
    return id_usuario

def editar_trilha(id_trilha, campo, novo_valor, dict_memoria):

    # Garante que o ID seja string para bater com o padrão de chaves do JSON
    id_trilha = str(id_trilha)
    
    # Sanitiza o input: converte para string, troca espaços por underscore e força minúsculas
    campo = str(campo).replace(" ", "_").lower()

    # Trata variação ortográfica comum para alinhar com a chave oficial
    if campo == "preço":
        campo = "preco"
    
    # Define as chaves estruturais e de relacionamento que não permitem edição manual
    campos_protegidos = ["id_trilha", "id_guia_responsavel" , "status" , "inscritos"]

    # Valida a existência da trilha na base antes de qualquer operação
    if id_trilha in dict_memoria["trilhas"]:
        
        # Bloqueia a edição se o campo alvo for restrito
        if campo in campos_protegidos:
            print(f"ERRO: O campo '{campo}' é gerado automaticamente e não pode ser editado.")
            return False

        # Previne a criação de chaves fantasmas se o campo não existir no modelo original
        if campo not in dict_memoria["trilhas"][id_trilha]:
            print(f"ERRO: O campo '{campo}' não existe no cadastro de trilhas.")
            return False
        
        try:
            # Aplica a tipagem correta para campos matemáticos ou de controle
            if campo == "capacidade":
                novo_valor = int(novo_valor)
            if campo == "preco":
                # Converte para string antes do replace para evitar AttributeError em números puros
                novo_valor = float(str(novo_valor).replace(",", "."))
                
        except ValueError:
            # Captura a falha se o usuário enviar letras para campos numéricos
            print(f"ERRO: Valor inválido. O campo '{campo}' exige um formato numérico.")
            return False    

        # Aplica o novo valor diretamente no dicionário em memória
        dict_memoria["trilhas"][id_trilha][campo] = novo_valor
        return True

    else:
        # Fallback caso a chave principal (ID) não seja encontrada
        print("ERRO: Trilha não encontrada no sistema.")
        return False