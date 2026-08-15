def adicionar_participante (id_trilha, novo_participante):
#1. Verifica se a trilha existe
    if id_trilha not in trilhas:
        return "Trilha não encontrada."
    
#1.1 Verifica se os dados do participante estão completos 
    campo_obrigatorio = ["id_participante", "nome", "status_checkin"]
    for campo in campo_obrigatorio:
        if campo not in novo_participante:
            return f"Dados do participante incompletos: falta '{campo}'"

#1.2 guarda os dados da trilha específica numa variável, pra não repetir trilhas[id_trilha] toda hora
    trilha = trilhas[id_trilha]

#2. Verifica se ainda há vagas
    vagas_ocupadas = len(trilha["inscritos"])
    if vagas_ocupadas >= trilha["capacidade"]:
        trilha["status"] = "Lotada"
        return "Trilha lotada, não é possível adicionar participante"

#3. Adiciona o participante na lista
    trilha["inscritos"].append(novo_participante)

#4. Atualiza o status se acabou de lotar
    if len(trilha["inscritos"]) >= trilha["capacidade"]:
        trilha["status"] = "Lotada"

    return "Participante adicionado com sucesso"

#5. Verifica se o participante já está inscrito na trilha.
    for participante in trilha["inscritos"]:
        if participante["id_participante"] == novo_participante["id_participante"]:
            return "Participante já inscrito na trilha."


