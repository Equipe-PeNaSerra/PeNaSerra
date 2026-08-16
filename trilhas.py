def editar_trilha(id_trilha, campo, novo_valor, dict_memoria):

    # Garante que o ID seja string para bater com o padrão de chaves do JSON
    id_trilha = str(id_trilha)
    
    # Sanitiza o input: converte para string, troca espaços por underscore e força minúsculas
    campo = str(campo).replace(" ", "_").lower()

    # Trata variação ortográfica comum para alinhar com a chave oficial
    if campo == "preço":
        campo = "preco"
    
    # Define as chaves estruturais e de relacionamento que não permitem edição manual
    campos_protegidos = ["id_trilha", "id_guia_responsavel" , "status" , "inscritos"]

    # Valida a existência da trilha na base antes de qualquer operação
    if id_trilha in dict_memoria["trilhas"]:
        
        # Bloqueia a edição se o campo alvo for restrito
        if campo in campos_protegidos:
            print(f"ERRO: O campo '{campo}' é gerado automaticamente e não pode ser editado.")
            return False

        # Previne a criação de chaves fantasmas se o campo não existir no modelo original
        if campo not in dict_memoria["trilhas"][id_trilha]:
            print(f"ERRO: O campo '{campo}' não existe no cadastro de trilhas.")
            return False
        
        try:
            # Aplica a tipagem correta para campos matemáticos ou de controle
            if campo == "capacidade":
                novo_valor = int(novo_valor)
            if campo == "preco":
                # Converte para string antes do replace para evitar AttributeError em números puros
                novo_valor = float(str(novo_valor).replace(",", "."))
                
        except ValueError:
            # Captura a falha se o usuário enviar letras para campos numéricos
            print(f"ERRO: Valor inválido. O campo '{campo}' exige um formato numérico.")
            return False    

        # Aplica o novo valor diretamente no dicionário em memória
        dict_memoria["trilhas"][id_trilha][campo] = novo_valor
        return True

    else:
        # Fallback caso a chave principal (ID) não seja encontrada
        print("ERRO: Trilha não encontrada no sistema.")
        return False