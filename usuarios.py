def cadastrar_participante(nome, telefone):
#1. Gera um ID único: Percorre os IDs e acha o maior, depois soma 1
    if participantes:
        maior_id = 0
        for id_participante in participante.keys():
            if int(id_participante) > maior_id:
                maior_id = int(id_participante)
        novo_id = maior_id + 1
    else:
        novo_id = 101

#2. Monta o dicionário do novo participante, com métricas zeradas
    novo_participante = {
        "id_participante": novo_id,
        "nome_trilheiro": nome,
        "telefone": telefone,
        "trilhas concluídas": 0,
        "nível de trilheiro:": "Curioso da Trilha",
        "histórico de trilhas": [],

    }

#3. Registra na estrutura global de "participantes"
    participantes[str(novo_id)] = novo_participante

    return f"Participante cadastrado com sucesso! ID: {novo_id}"

#4. Classifica o nível do trilheiro de acordo com a quantidade de trilhas concluídas.
def classificar_nivel_trilheiro(trilhas_concluidas):

    if trilhas_concluidas <= 2:
        return "Curioso da Trilha"

    elif trilhas_concluidas <= 5:
        return "Trilheiro"

    elif trilhas_concluidas <= 10:
        return "Desbravador"

    elif trilhas_concluidas <= 20:
        return "Buscador de Horizontes"

    else:
        return "Lenda das Trilhas"
