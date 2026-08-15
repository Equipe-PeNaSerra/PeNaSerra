def autenticar_usuario(id_usuario, dict_memoria):
    # Converte o ID numérico para string para buscar nas chaves do JSON
    id_usuario = str(id_usuario)
    
    # Verifica em qual base o ID se encontra e retorna o perfil correspondente
    if id_usuario in dict_memoria["participantes"]:
        return "Trilheiro"
    elif id_usuario in dict_memoria["guias"]:
        return "Guia"
    else:
        return None


def receber_usuario():
    # Mantém o usuário preso no loop até que digite um ID válido
    while True:
        try:
            # Tenta converter a entrada direto para inteiro
            id_usuario = int(input("Digite seu ID de usuário: "))
            break
        except ValueError:
            # Disparado se a conversão falhar (ex: letras ou símbolos digitados)
            print("ERRO: Formato de ID inválido. O ID é composto somente por números!")
            
    return id_usuario