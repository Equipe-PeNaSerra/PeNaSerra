def solicitar_reserva(id_trilha, id_participante, dict_memoria):
    
    # Sanitização básica de entrada para garantir que o backend receba o tipo correto
    id_trilha_str = str(id_trilha)
    id_part_str = str(id_participante)

    # Como o padrão 'Single Source of Truth' foi aplicado na adicionar_participante,
    # não precisamos buscar o usuário ou montar o dicionário de status do check-in aqui.
    # Delega-se a operação completa de validação e escrita para o módulo de operações.
    mensagem_resultado = adicionar_participante(id_trilha_str, id_part_str, dict_memoria)
    
    # Repassa a mensagem de sucesso ou erro (ex: "Trilha Lotada") de volta para o menu
    return mensagem_resultado


def adicionar_participante(id_trilha, id_participante, dict_memoria):
    
    # Padroniza os IDs para busca nas chaves do dicionário (que são sempre strings)
    id_trilha_str = str(id_trilha)
    id_part_str = str(id_participante)
    
    trilhas = dict_memoria["trilhas"]
    participantes = dict_memoria.get("participantes", {})

    # Verifica se a trilha e o participante existem no sistema global
    if id_trilha_str not in trilhas:
        return "ERRO: Trilha não encontrada no sistema."
        
    if id_part_str not in participantes:
        return "ERRO: Participante não encontrado na base de dados."

    # Guarda os dados em variáveis locais para evitar repetição de busca no dicionário
    trilha_alvo = trilhas[id_trilha_str]
    participante_global = participantes[id_part_str]

    # Verifica se o participante já está inscrito (movido para antes do processamento)
    for inscrito in trilha_alvo["inscritos"]:
        if str(inscrito["id_participante"]) == id_part_str:
            return "AVISO: Este participante já possui uma inscrição ativa nesta trilha."

    # Verifica se ainda há vagas
    vagas_ocupadas = len(trilha_alvo["inscritos"])
    if vagas_ocupadas >= trilha_alvo["capacidade"]:
        # Se algum erro anterior não alterou o status, força a correção aqui
        trilha_alvo["status"] = "Lotada"
        return "ERRO: Trilha lotada. Não é possível adicionar o participante."

    # Monta o micro-dicionário de inscrição com dados oficiais da base (Segurança)
    novo_inscrito = {
        "id_participante": int(id_part_str),
        "nome_trilheiro": participante_global["nome_trilheiro"],
        "status_checkin": False
    }

    # Adiciona o participante na lista da trilha
    trilha_alvo["inscritos"].append(novo_inscrito)

    # Atualiza o status automaticamente se esta inscrição preencheu a última vaga
    if len(trilha_alvo["inscritos"]) >= trilha_alvo["capacidade"]:
        trilha_alvo["status"] = "Lotada"

    return "Participante adicionado com sucesso!"



def gerar_relatorio_geral(dict_memoria):
    
    # Extrai o banco de dados de forma segura
    trilhas = dict_memoria.get("trilhas", {})
    
    # Bloqueia a execução se não houver dados para gerar o relatório
    if not trilhas:
        print("AVISO: Nenhuma trilha cadastrada para gerar relatório.")
        return False

    lucro_total = 0.0

    print("\n=== RELATÓRIO FINANCEIRO E DE OCUPAÇÃO GERAL ===")
    
    # O uso de .items() permite extrair ID e Dicionário na mesma linha
    for id_trilha, trilha in trilhas.items():
        
        # Acesso seguro aos dados com prevenção de KeyError
        inscritos = trilha.get("inscritos", [])
        vagas_ocupadas = len(inscritos)
        capacidade = trilha.get("capacidade", 1)
        preco = float(trilha.get("preco", 0.0))
        
        # Programação Defensiva: Impede erro fatal de Divisão por Zero
        if capacidade > 0:
            ocupacao_percentual = (vagas_ocupadas / capacidade) * 100
        else:
            ocupacao_percentual = 0.0

        # Cálculo de faturamento direto no laço economiza processamento
        faturamento = vagas_ocupadas * preco
        lucro_total += faturamento

        # Formatação para o padrão monetário brasileiro
        faturamento_br = f"{faturamento:.2f}".replace(".", ",")
        
        # Resgata o nome com fallback caso a chave não exista
        nome = trilha.get("nome_trilha", "Desconhecida")
        
        print(f"- {nome}: {ocupacao_percentual:.1f}% ocupada | Faturamento: R$ {faturamento_br}")

    # Exibição do consolidado final
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
