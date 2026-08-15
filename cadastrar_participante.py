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
        "nível de trilheiro:": "Iniciante",
        "histórico de trilhas": [],

    }

#3. Registra na estrutura global de "participantes"
    participantes[str(novo_id)] = novo_participante

    return f"Participante cadastrado com sucesso! ID: {novo_id}"