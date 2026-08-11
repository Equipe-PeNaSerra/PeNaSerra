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
        "inscritos": []
    },

    "102": {
        "id_trilha": 102,
        "nome": "Trilha B",
        "local": "Barbalha - CE",
        "dificuldade": "Média",
        "capacidade": 15,
        "preco": 70.00,
        "status": "Disponível",
        "inscritos": []
    },

    "103": {
        "id_trilha": 103,
        "nome": "Trilha C",
        "local": "Juazeiro do Norte - CE",
        "dificuldade": "Difícil",
        "capacidade": 8,
        "preco": 90.00,
        "status": "Disponível",
        "inscritos": []
    },

    "104": {
        "id_trilha": 104,
        "nome": "Trilha D",
        "local": "Crato - CE",
        "dificuldade": "Fácil",
        "capacidade": 20,
        "preco": 40.00,
        "status": "Disponível",
        "inscritos": []
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
    encontradas = []
    for trilha in trilhas:
        if trilhas[trilha]["dificuldade"] == nivel_desejado:
            encontradas.append(trilhas[trilha]["nome"])
    return encontradas


