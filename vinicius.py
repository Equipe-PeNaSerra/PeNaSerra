

# Função responsável por classificar o nível do trilheiro
# com base na quantidade de trilhas que ele já concluiu.
def classificar_nivel_trilheiro(trilhas_concluidas):

    # Se o usuário concluiu até 2 trilhas,
    # ele recebe o primeiro nível.
    if trilhas_concluidas <= 2:
        return "Curioso da Trilha"

    # Se chegou aqui, significa que já concluiu mais de 2 trilhas.
    # Portanto, de 3 até 5 trilhas, ele será classificado como Trilheiro.
    elif trilhas_concluidas <= 5:
        return "Trilheiro"

    # De 6 até 10 trilhas concluídas,
    # o usuário recebe o nível Desbravador.
    elif trilhas_concluidas <= 10:
        return "Desbravador"

    # De 11 até 20 trilhas concluídas,
    # o usuário recebe o nível Buscador de Horizontes.
    elif trilhas_concluidas <= 20:
        return "Buscador de Horizontes"

    # Se nenhuma das condições anteriores for verdadeira,
    # significa que o usuário concluiu mais de 20 trilhas.
    else:
        return "Lenda das Trilhas"

# função para mostrar na tela as listas que ele deseja por nível de dificuldade
def buscar_por_dificuldade(nivel_desejado):
    # Primeiramente cria-se uma lista vazia
    encontradas = []
    # Usa um laço em for para buscar essas trilhas
    for trilha in trilhas:
        # Usa o if para justamente filtrar pela dificuldade escolhida
        if trilhas[trilha]["dificuldade"] == nivel_desejado:
            # Adiciona a função append para adicionar essa trilha conforme o nível filtrado
            encontradas.append(trilhas[trilha]["nome"])
            # Retorna essa lista de trilhas filtradas
    return encontradas

# Função responsável por calcular o faturamento de uma trilha
# considerando apenas os participantes que concluíram a atividade.
def calcular_faturamento_trilha(id_trilha):

    # Inicia o contador de participantes que concluíram a trilha.
    concluidos = 0

    # Percorre a lista de participantes inscritos na trilha escolhida.
    for participante in trilhas[id_trilha]["inscritos"]:

        # Verifica se o participante está com o check-in concluído.
        if participante["status_checkin"] == "Concluído":

            # Se estiver concluído, acrescenta 1 ao contador.
            concluidos += 1

    # Calcula o faturamento multiplicando o número de participantes
    # que concluíram a trilha pelo preço individual da atividade.
    faturamento = concluidos * trilhas[id_trilha]["preco"]

    # Retorna o valor total do faturamento da trilha.
    return faturamento


# id_trilha será dado em string e id_participante em int
def registrar_checkin(id_trilha,id_participante):
#Laço for para acessar os participantes no dicionário inscritos que está dentro do dicionário id_trilha(string) que está dentro do dicionário trilhas
    for participante in trilhas[id_trilha]["inscritos"]:
        # Verifica se encontrou o participante informado pelo guia
        if id_participante == participante["id_participante"]:
            # Só realiza o check-in se ele ainda estiver pendente
            if participante["status_checkin"] == "Pendente":
                # muda o status checkin para concluído
                participante["status_checkin"] = "Concluído"
                # adicionar o id da trilha na lista do histórico dentro do dicionário de participantes
                participantes[str(id_participante)]["historico_trilhas"].append(id_trilha)
                # adiciona uma trilha nas trilhas concluídas
                participantes[str(id_participante)]["trilhas_concluidas"] += 1
                # Chamando minha função classificar trilheiro e atribuindo a uma nova variável para classificar o novo nível do trilheiro
                novo_nivel = classificar_nivel_trilheiro(participantes[str(id_participante)]["trilhas_concluidas"])
                # atribuindo o novo nível na chave nível dentro do dicionário participante
                participantes[str(id_participante)]["nivel"] = novo_nivel

                return True 
                    # Caso encontre o participante, mas o check-in já esteja concluído
            else:
                print("Check-in já concluído")
                return False

    # Caso o for termine sem encontrar o participante
    print("Participante não encontrado")
    return False

    # id_trilha será dado em string e id_participante em int
def remover_participante(id_trilha, id_participante):

    # Laço for para acessar os participantes no dicionário inscritos
    for participante in trilhas[id_trilha]["inscritos"]:

        # Verifica se encontrou o participante informado pelo guia
        if id_participante == participante["id_participante"]:
            trilhas[id_trilha]["inscritos"].remove(participante)

            # Verificar se a trilha está lotada
            if trilhas[id_trilha]["status"] == "Lotada":
                trilhas[id_trilha]["status"] = "Disponível"

            return True

    # O for terminou e não encontrou o participante
    print("Participante não encontrado")
    return False



