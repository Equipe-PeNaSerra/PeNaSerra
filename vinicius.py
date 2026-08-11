# Banco de dados provisório para testar as funções

trilhas = {
    "101": {
        "id_trilha": 101,
        "nome": "Trilha A",
        "local": "Crato - CE",
        "dificuldade": "Fácil",
        "capacidade": 10,
        "preco": 50.00,
        "status": "Disponível",
        "inscritos": [
            {
                "id_participante": 501,
                "nome": "João",
                "status_checkin": "Concluído"
            },
            {
                "id_participante": 502,
                "nome": "Maria",
                "status_checkin": "Concluído"
            },
            {
                "id_participante": 503,
                "nome": "Pedro",
                "status_checkin": "Pendente"
            }
        ]
    },

    "102": {
        "id_trilha": 102,
        "nome": "Trilha B",
        "local": "Barbalha - CE",
        "dificuldade": "Média",
        "capacidade": 15,
        "preco": 70.00,
        "status": "Disponível",
        "inscritos": [
            {
                "id_participante": 504,
                "nome": "Ana",
                "status_checkin": "Concluído"
            },
            {
                "id_participante": 505,
                "nome": "Lucas",
                "status_checkin": "Pendente"
            }
        ]
    },

    "103": {
        "id_trilha": 103,
        "nome": "Trilha C",
        "local": "Juazeiro do Norte - CE",
        "dificuldade": "Difícil",
        "capacidade": 8,
        "preco": 90.00,
        "status": "Disponível",
        "inscritos": [
            {
                "id_participante": 506,
                "nome": "Carlos",
                "status_checkin": "Concluído"
            },
            {
                "id_participante": 507,
                "nome": "Fernanda",
                "status_checkin": "Concluído"
            },
            {
                "id_participante": 508,
                "nome": "Rafael",
                "status_checkin": "Pendente"
            }
        ]
    },

    "104": {
        "id_trilha": 104,
        "nome": "Trilha D",
        "local": "Crato - CE",
        "dificuldade": "Fácil",
        "capacidade": 20,
        "preco": 40.00,
        "status": "Disponível",
        "inscritos": [
            {
                "id_participante": 509,
                "nome": "Beatriz",
                "status_checkin": "Pendente"
            }
        ]
    },

    "105": {
        "id_trilha": 105,
        "nome": "Trilha E",
        "local": "Barbalha - CE",
        "dificuldade": "Difícil",
        "capacidade": 12,
        "preco": 100.00,
        "status": "Disponível",
        "inscritos": []
    }
}

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

print(calcular_faturamento_trilha("101"))