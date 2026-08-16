from usuarios import classificar_nivel_trilheiro

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


# Função para calcular faturamento dos guias
def gerar_relatorio_geral(lista_trilhas):
    lucro_total = 0

    print("=== Relatório Geral de Trilhas ===")
    for id_trilha in lista_trilhas:
        trilha = lista_trilhas[id_trilha]

        # Calcula ocupação em porcentagem
        vagas_ocupadas = len(trilha["inscritos"])
        capacidade = trilha["capacidade"]
        ocupacao_percentual = (vagas_ocupadas / capacidade) * 100

        # Chama a função calcular_faturamento_trilha
        faturamento = calcular_faturamento_trilha(id_trilha)
        lucro_total += faturamento

        print(f"{trilha['nome']}: {ocupacao_percentual:.1f}% ocupada | Faturamento: R${faturamento:.2f}")

    print(f"\nLucro total do guia: R${lucro_total:.2f}")

# Calcula o faturamento da trilha com base nos participantes que concluíram o check-in.
def calcular_faturamento_trilha(id_trilha):
    concluidos = 0

    for participante in trilhas[id_trilha]["inscritos"]:
        if participante["status_checkin"] == "Concluído":
            concluidos += 1

    faturamento = concluidos * trilhas[id_trilha]["preco"]

    return faturamento

    # Registra o check-in do participante e atualiza seu histórico, quantidade de trilhas concluídas e nível.
def registrar_checkin(id_trilha, id_participante):

    for participante in trilhas[id_trilha]["inscritos"]:

        # Verifica se o participante informado está inscrito na trilha
        if id_participante == participante["id_participante"]:

            if participante["status_checkin"] == "Pendente":
                participante["status_checkin"] = "Concluído"

                participantes[str(id_participante)]["historico_trilhas"].append(id_trilha)
                participantes[str(id_participante)]["trilhas_concluidas"] += 1

                # Recalcula o nível após aumentar a quantidade de trilhas concluídas
                novo_nivel = classificar_nivel_trilheiro(
                    participantes[str(id_participante)]["trilhas_concluidas"]
                )

                participantes[str(id_participante)]["nivel"] = novo_nivel

                return True

            else:
                print("Check-in já concluído")
                return False

    # Se o laço terminar sem retornar, o participante não foi encontrado
    print("Participante não encontrado")
    return False

    # Remove um participante da trilha e atualiza sua disponibilidade caso uma vaga seja liberada.
def remover_participante(id_trilha, id_participante):

    for participante in trilhas[id_trilha]["inscritos"]:

        # Localiza o participante informado e o remove da lista de inscritos
        if id_participante == participante["id_participante"]:
            trilhas[id_trilha]["inscritos"].remove(participante)

            # Se a trilha estava lotada, a remoção faz com que volte a ter vaga
            if trilhas[id_trilha]["status"] == "Lotada":
                trilhas[id_trilha]["status"] = "Disponível"

            return True

    # O laço só chega ao fim se nenhum participante com o ID informado for encontrado
    print("Participante não encontrado")
    return False
