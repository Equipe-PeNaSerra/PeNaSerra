def solicitar_reserva(id_trilha, id_participante, dict_memoria):
    
    # transforma os IDs em texto porque as chaves dos dicionários usados
    # no sistema são sempre strings, então evita erro de comparação
    id_trilha_str = str(id_trilha)
    id_part_str = str(id_participante)

    # essa função so serve de ponte pra a função adicionar_participante, que já
    # cuida de toda a validação e da lógica de inscrição
    mensagem_resultado = adicionar_participante(id_trilha_str, id_part_str, dict_memoria)
    
    return mensagem_resultado


def adicionar_participante(id_trilha, id_participante, dict_memoria):
    
    trilhas = dict_memoria["trilhas"]
    participantes = dict_memoria.get("participantes", {})

    # antes de fazer qualquer coisa, precisa garantir que a trilha e o participante
    # realmente existem no sistema, senão não tem como continuar
    if id_trilha not in trilhas:
        return "ERRO: Trilha não encontrada no sistema."
    if id_participante not in participantes:
        return "ERRO: Participante não encontrado na base de dados."

    # pega o dicionário completo com as informações necessárias da trilha e do participante pelo ID,
    # evitando buscar de novo mais adiante
    trilha_alvo = trilhas[id_trilha]
    participante_global = participantes[id_participante]

    # percorre a lista de inscritos da trilha pra ver se essa pessoa já tá lá dentro,
    # já que não faz sentido a mesma pessoa se inscrever duas vezes
    for inscrito in trilha_alvo["inscritos"]:
        if str(inscrito["id_participante"]) == id_participante:
            return "AVISO: Este participante já possui uma inscrição ativa nesta trilha."

    # conta quantas vagas já foram ocupadas e compara com a capacidade máxima da trilha
    vagas_ocupadas = len(trilha_alvo["inscritos"])
    if vagas_ocupadas >= trilha_alvo["capacidade"]:
        trilha_alvo["status"] = "Lotada"
        return "ERRO: Trilha lotada. Não é possível adicionar o participante."

    # cria o registro de inscrição usando os dados que já existem do participante,
    # começando o check-in como falso porque ele ainda não confirmou presença
    novo_inscrito = {
        "id_participante": int(id_participante),
        "nome_trilheiro": participante_global["nome_trilheiro"],
        "status_checkin": False
    }

    trilha_alvo["inscritos"].append(novo_inscrito)

    # depois de adicionar, confere de novo se essa foi a última vaga disponível,
    # e se foi, já atualiza o status da trilha pra lotada
    if len(trilha_alvo["inscritos"]) >= trilha_alvo["capacidade"]:
        trilha_alvo["status"] = "Lotada"

    return "Participante adicionado com sucesso!"



def gerar_relatorio_geral(dict_memoria):
    
    trilhas = dict_memoria.get("trilhas", {})
    
    # se não tiver nenhuma trilha cadastrada, não tem relatório pra gerar,
    # então já para a função aqui e avisa o usuário
    if not trilhas:
        print("AVISO: Nenhuma trilha cadastrada para gerar relatório.")
        return False

    lucro_total = 0.0

    print("\n=== RELATÓRIO FINANCEIRO E DE OCUPAÇÃO GERAL ===")
    
    # passa por cada trilha cadastrada pra calcular a ocupação e o faturamento dela
    for id_trilha, trilha in trilhas.items():
        
        inscritos = trilha.get("inscritos", [])
        vagas_ocupadas = len(inscritos)
        capacidade = trilha.get("capacidade", 1)
        preco = float(trilha.get("preco", 0.0))
        
        # calcula a porcentagem de ocupação, mas só se a capacidade for maior que zero,
        # senão daria erro de divisão por zero
        if capacidade > 0:
            ocupacao_percentual = (vagas_ocupadas / capacidade) * 100
        else:
            ocupacao_percentual = 0.0

        # multiplica as vagas ocupadas pelo preço da trilha pra saber o faturamento dela,
        # e vai somando no total geral
        faturamento = vagas_ocupadas * preco
        lucro_total += faturamento

        # troca o ponto por vírgula, para ficar no padrão do real
        faturamento_br = f"{faturamento:.2f}".replace(".", ",")
        
        nome = trilha.get("nome_trilha", "Desconhecida")
        
        print(f"- {nome}: {ocupacao_percentual:.1f}% ocupada | Faturamento: R$ {faturamento_br}")

    # depois de passar por todas as trilhas, mostra o faturamento total somado
    lucro_br = f"{lucro_total:.2f}".replace(".", ",")
    print("-" * 55)
    print(f"Faturamento Total Previsto: R$ {lucro_br}")
    
    return True



def calcular_faturamento_trilha(id_trilha, dict_memoria):
    
    trilhas = dict_memoria.get("trilhas", {})
    id_str = str(id_trilha)
    
    # Validação de existência da trilha
    if id_str not in trilhas:
        return 0.0

    trilha_alvo = trilhas[id_str]
    concluidos = 0

    # O uso do .get() retorna uma lista vazia caso a trilha não tenha a chave 'inscritos'
    for participante in trilha_alvo.get("inscritos", []):
        
        # Só fatura participantes que efetivamente concluíram a trilha
        # A validação em boolean (True) substitui o texto "Concluído" exigido pela nova arquitetura
        if participante.get("status_checkin") is True:
            concluidos += 1

    # Garante que o preço seja tratado como float para evitar erro matemático
    preco = float(trilha_alvo.get("preco", 0.0))
    faturamento = concluidos * preco

    return faturamento


def registrar_checkin(id_trilha, id_participante, dict_memoria):
    
    id_trilha_str = str(id_trilha)
    id_part_str = str(id_participante)
    
    trilhas = dict_memoria.get("trilhas", {})
    participantes = dict_memoria.get("participantes", {})

    # Validações estruturais de existência
    if id_trilha_str not in trilhas:
        print("ERRO: Trilha não encontrada no sistema.")
        return False
        
    if id_part_str not in participantes:
        print("ERRO: Participante não encontrado no banco global.")
        return False

    trilha_alvo = trilhas[id_trilha_str]
    participante_global = participantes[id_part_str]

    # Laço for para encontrar o micro-dicionário de inscrição dentro da trilha
    for inscrito in trilha_alvo.get("inscritos", []):
        
        if str(inscrito.get("id_participante")) == id_part_str:
            
            # Só realiza o check-in se ele estiver como False (Pendente)
            if inscrito.get("status_checkin") is False:
                
                # 1. Atualiza o status local na trilha
                inscrito["status_checkin"] = True
                
                # 2. Adiciona o ID da trilha no histórico global do participante
                # Protege contra KeyError usando list.append de forma segura
                historico = participante_global.setdefault("historico_trilhas", [])
                historico.append(id_trilha_str)
                
                # 3. Incrementa o contador de trilhas globais
                participante_global["trilhas_concluidas"] = participante_global.get("trilhas_concluidas", 0) + 1
                
                # 4. Atualiza o Nível/Patente
                novo_nivel = classificar_nivel_trilheiro(participante_global["trilhas_concluidas"])
                participante_global["nivel_trilheiro"] = novo_nivel

                print(f"Check-in concluído! {inscrito.get('nome_trilheiro')} agora é: {novo_nivel}")
                return True
                
            else:
                print("AVISO: Check-in deste participante já estava concluído.")
                return False

    # O laço iterou por todos os inscritos e não encontrou o ID
    print("ERRO: Este participante não está inscrito nesta trilha.")
    return False



def remover_participante(id_trilha, id_participante, dict_memoria):
    
    id_trilha_str = str(id_trilha)
    id_part_str = str(id_participante)
    trilhas = dict_memoria.get("trilhas", {})

    if id_trilha_str not in trilhas:
        print("ERRO: Trilha não encontrada.")
        return False

    trilha_alvo = trilhas[id_trilha_str]
    inscritos_lista = trilha_alvo.get("inscritos", [])

    # Itera para encontrar o participante
    for inscrito in inscritos_lista:
        
        if str(inscrito.get("id_participante")) == id_part_str:
            
            # Remove o dicionário do participante da lista
            inscritos_lista.remove(inscrito)

            # Regra de Negócio: Se a trilha estava lotada, a remoção libera 1 vaga
            if trilha_alvo.get("status") == "Lotada":
                trilha_alvo["status"] = "Disponível"

            print("Cancelamento de inscrição realizado com sucesso.")
            return True

    print("ERRO: O participante não foi encontrado na lista de inscritos desta trilha.")
    return False
