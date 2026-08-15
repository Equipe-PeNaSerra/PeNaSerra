def solicitar_reserva(id_trilha, id_participante):
    #1. Verifica se o participante existe no cadastro global
    if str(id_participante) not in participantes:
        return "Participante não cadastrado. Por favor, cadastre o participante antes de solicitar a reserva."

    #2. Busca os dados do participante no cadastro global
    dados_participante = participantes[str(id_participante)]

    #3 Monta o dicionário no formato que a função adicionar_participante espera
    novo_participante = {
        "id_participante": dados_participante["id_participante"],
        "nome_trilheiro": dados_participante["nome_trilheiro"],
        "status_checkin": "Pendente"
    }

    #4 Chama a função adicionar_participante
    return adicionar_participante(id_trilha, novo_participante)