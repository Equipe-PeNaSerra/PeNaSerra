def cadastrar_participante(nome, telefone, dict_memoria):
    
    # Previne o cadastro se o usuário enviar strings vazias ou só com espaços
    if not nome.strip() or not telefone.strip():
        return "ERRO: O nome e o telefone são obrigatórios e não podem estar vazios."

    # Acessa o banco de participantes
    participantes = dict_memoria["participantes"]

    # Descobre o próximo ID disponível varrendo o histórico (base 500)
    if participantes:
        maior_id = max(int(id_participante) for id_participante in participantes.keys())
        novo_id = maior_id + 1
    else:
        novo_id = 501

    # Monta o dicionário com chaves padronizadas (sem espaços ou acentos) e métricas zeradas
    novo_participante = {
        "id_participante": novo_id,
        "nome_trilheiro": nome.strip().title(),
        "telefone": telefone.strip(),
        "trilhas_concluidas": 0,
        "nivel_trilheiro": "Iniciante",
        "historico_trilhas": []
    }

    # Insere no dicionário principal forçando a chave para string (padrão JSON)
    participantes[str(novo_id)] = novo_participante

    return f"Participante cadastrado com sucesso! ID: {novo_id}"

def cadastrar_guia(nome_guia, telefone, especialidade, dict_memoria):

    # Previne o cadastro se o menu enviar strings vazias ou só com espaços
    if not nome_guia.strip() or not telefone.strip() or not especialidade.strip():
        return "ERRO: Todos os campos são obrigatórios e não podem estar vazios."

    guias = dict_memoria["guias"]

    # Descobre o próximo ID disponível varrendo o histórico (base 300)
    if guias:
        maior_id = max(int(id_guia) for id_guia in guias.keys())
        novo_id = maior_id + 1
    else:
        novo_id = 301

    # Monta o dicionário estrutural do novo guia aplicando formatação de texto
    novo_guia = {
        "id_guia": novo_id,
        "nome_guia": nome_guia.strip().title(),
        "telefone": telefone.strip(),
        "especialidade": especialidade.strip().capitalize(),
        "trilhas_guiadas": []
    }

    # Insere no dicionário principal forçando a chave para string (padrão JSON)
    guias[str(novo_id)] = novo_guia

    return f"Guia cadastrado com sucesso! ID: {novo_id}"

def classificar_nivel_trilheiro(trilhas_concluidas):
    
    # Previne bugs caso o contador seja acidentalmente negativo
    if trilhas_concluidas < 0:
        trilhas_concluidas = 0

    if trilhas_concluidas <= 2:
        return "Iniciante"  # Ajustado para combinar com o cadastro base
    elif trilhas_concluidas <= 5:
        return "Trilheiro"
    elif trilhas_concluidas <= 10:
        return "Desbravador"
    elif trilhas_concluidas <= 20:
        return "Buscador de Horizontes"
    else:
        return "Lenda das Trilhas"
