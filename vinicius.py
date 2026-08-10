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
