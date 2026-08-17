def cadastrar_participante(nome, telefone):
#1. Gera um ID único: Percorre os IDs e acha o maior, depois soma 1
    if participantes:
        maior_id = 0
        for id_participante in participante.keys():
            if int(id_participante) > maior_id:
                maior_id = int(id_participante)
        novo_id = maior_id + 1
    else:
        novo_id = 501

#2. Monta o dicionário do novo participante, com métricas zeradas
    novo_participante = {
        "id_participante": novo_id,
        "nome_trilheiro": nome,
        "telefone": telefone,
        "trilhas concluídas": 0,
        "nível de trilheiro:": "Iniciante",
        "histórico de trilhas": [],

    }

#3. Registra na estrutura global de "participantes"
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

