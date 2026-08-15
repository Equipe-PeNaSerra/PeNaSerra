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