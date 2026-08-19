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
    


def cadastrar_trilha(nome_trilha, id_guia, local, dificuldade, capacidade, preco, dict_memoria):

    # Previne o cadastro se os campos de texto estiverem vazios
    if not nome_trilha.strip() or not local.strip() or not dificuldade.strip():
        return "ERRO: Os campos de nome, local e dificuldade não podem estar vazios."

    # Garante a integridade referencial: o guia responsável precisa existir na base
    if str(id_guia) not in dict_memoria["guias"]:
        return f"ERRO: Guia responsável (ID {id_guia}) não encontrado no sistema."

    # Aplica a tipagem correta aos atributos matemáticos para não quebrar relatórios futuros
    try:
        capacidade = int(capacidade)
        # Converte para string antes do replace para evitar AttributeError e garante o float
        preco = float(str(preco).replace(",", "."))
    except ValueError:
        return "ERRO: A capacidade deve ser um número inteiro e o preço um valor numérico."

    trilhas = dict_memoria["trilhas"]

    # Descobre o próximo ID disponível varrendo o histórico (base 100)
    if trilhas:
        maior_id = max(int(id_trilha) for id_trilha in trilhas.keys())
        novo_id = maior_id + 1
    else:
        novo_id = 101

    # Monta o dicionário estrutural aplicando formatação visual nos textos
    nova_trilha = {
        "id_trilha": novo_id,
        "nome_trilha": nome_trilha.strip().title(),
        "id_guia_responsavel": int(id_guia),
        "local": local.strip().title(),
        "dificuldade": dificuldade.strip().capitalize(),
        "capacidade": capacidade,
        "preco": preco,
        "status": "Disponível",
        "inscritos": []
    }

    # Insere no dicionário principal forçando a chave para string
    trilhas[str(novo_id)] = nova_trilha

    return f"Trilha cadastrada com sucesso! ID: {novo_id}"



def excluir_trilha(id_trilha, dict_memoria):

    # Garante a tipagem correta para buscar a chave no dicionário JSON
    id_str = str(id_trilha)
    trilhas = dict_memoria["trilhas"]

    # Valida a existência da trilha na base antes de qualquer operação
    if id_str not in trilhas:
        return f"ERRO: Trilha (ID {id_trilha}) não encontrada no sistema."

    trilha_alvo = trilhas[id_str]

    # Regra de negócio: bloqueia a deleção se houver clientes com reserva ativa
    # Em Python, listas com itens são 'True' e listas vazias são 'False'
    if trilha_alvo["inscritos"]:
        nome = trilha_alvo["nome_trilha"]
        qtd_inscritos = len(trilha_alvo["inscritos"])
        return f"ERRO: A trilha '{nome}' não pode ser excluída pois possui {qtd_inscritos} participante(s) inscrito(s)."

    # Armazena o nome temporariamente para o log de sucesso
    nome_trilha = trilha_alvo["nome_trilha"]

    # Remove o nó completo do dicionário em memória
    del trilhas[id_str]

    return f"Trilha '{nome_trilha}' (ID: {id_trilha}) foi excluída com sucesso."



def listar_trilhas_admin(dict_memoria):
    print("\n--- PAINEL DO ADMIN: TODAS AS TRILHAS ---")

    # Extrai o bloco de trilhas de forma segura
    trilhas = dict_memoria.get("trilhas", {})

    # Validação rápida de dicionário vazio
    if not trilhas:
        print("AVISO: Nenhuma trilha cadastrada no sistema até o momento.")
        return False

    # Itera simultaneamente sobre a chave (ID) e o dicionário interno (dados)
    for id_trilha, dados in trilhas.items():

        # O uso do .get() previne crashes caso a chave 'inscritos' não exista em registros antigos
        qtd_inscritos = len(dados.get("inscritos", []))

        # Formata com duas casas decimais e substitui o separador americano pelo brasileiro
        preco_br = f"{dados.get('preco', 0):.2f}".replace(".", ",")

        # A quebra de linha visual dentro do print respeita o limite de colunas da PEP 8
        print(
            f"ID: {id_trilha} | Nome: {dados.get('nome_trilha')} | "
            f"Local: {dados.get('local')} | Dificuldade: {dados.get('dificuldade')} | "
            f"Preço: R$ {preco_br} | Guia Resp: {dados.get('id_guia_responsavel')} | "
            f"Status: {dados.get('status')} | Inscritos: {qtd_inscritos}/{dados.get('capacidade'):.2%}"
        )

    return True



def listar_trilhas_disponiveis(dict_memoria):
    print("\n--- VISÃO DO TRILHEIRO: TRILHAS DISPONÍVEIS ---")

    # Extração segura do bloco de trilhas para prevenir KeyError
    banco_trilhas = dict_memoria.get("trilhas", {})
    encontrou_disponivel = False

    # Bloqueio inicial se o banco de dados principal estiver vazio
    if not banco_trilhas:
        print("AVISO: Nenhuma trilha cadastrada no sistema até o momento.")
        return False

    # Itera sobre o dicionário filtrando o conteúdo para o cliente final
    for id_trilha, dados in banco_trilhas.items():

        # Extrai o status de forma segura, removendo espaços fantasmas e case-sensitive
        status_atual = str(dados.get("status", "")).strip().lower()

        if status_atual == "disponível":
            encontrou_disponivel = True

            # Formata a exibição do preço com padrão brasileiro de vírgula
            preco_br = f"{dados.get('preco', 0):.2f}".replace(".", ",")

            # Quebra de string em múltiplas linhas (PEP 8) para facilitar a leitura no editor
            print(
                f"ID: {id_trilha} | Nome: {dados.get('nome_trilha')} | "
                f"Local: {dados.get('local')} | Dificuldade: {dados.get('dificuldade')} | "
                f"Preço: R$ {preco_br}"
            )

    # Feedback visual para o usuário se o laço terminar sem achar vagas
    if not encontrou_disponivel:
        print("AVISO: Não há trilhas com vagas disponíveis no momento.")
        return False

    return True


def buscar_por_dificuldade(nivel_desejado, dict_memoria):
    
    trilhas = dict_memoria.get("trilhas", {})
    encontradas = []
    
    # Padroniza a string de busca para evitar que "Fácil" e "fácil" sejam tratadas diferentes
    nivel_formatado = str(nivel_desejado).strip().lower()

    for id_trilha, dados_trilha in trilhas.items():
        # Extrai a dificuldade da trilha atual de forma segura e padronizada
        dificuldade_atual = str(dados_trilha.get("dificuldade", "")).strip().lower()
        
        # Filtra e adiciona na lista de retorno
        if dificuldade_atual == nivel_formatado:
            encontradas.append(dados_trilha.get("nome_trilha", "Desconhecida"))
            
    return encontradas
