# Importa os módulos isolados para manter a organização e responsabilidade única
from auth import *
from infra import *
from operacoes import *
from trilhas import *
from usuarios import *

# Constante global (Single Source of Truth) para o banco de dados.
# Centraliza o nome do arquivo para facilitar futuras manutenções.
NOME_ARQUIVO = "banco_de_dados.json"


def menu_guia(id_atual, dict_memoria):
    """Controla o painel exclusivo para Guias e Administradores."""

    # Mantém o laço ativo até o usuário escolher a opção de sair
    while True:
        print("\n" + "="*45)
        print("PAINEL DO GUIA / ADMINISTRADOR")
        print("="*45)
        print("1. Registrar Novo Participante")
        print("2. Registrar Nova Trilha")
        print("3. Editar Trilha")
        print("4. Excluir Trilha")
        print("5. Listar Todas as Trilhas")
        print("6. Gerar Relatório Financeiro e Geral")
        print("7. Registrar Check-in de Participante")
        print("0. Encerrar Sessão (Voltar ao Login)")

        # Lê a opção e limpa espaços em branco indesejados
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do Participante: ")
            telefone = input("Telefone: ")
            # Executa o cadastro e já imprime o feedback (sucesso ou erro)
            print(cadastrar_participante(nome, telefone, dict_memoria))

        elif opcao == "2":
            nome = input("Nome da Trilha: ")
            local = input("Local: ")
            dificuldade = input("Dificuldade (Fácil/Média/Difícil): ")
            capacidade = input("Capacidade Máxima: ")
            preco = input("Preço (R$): ")

            # Regra de negócio: O guia logado (id_atual) vira automaticamente o responsável
            print(cadastrar_trilha(nome, id_atual, local,
                  dificuldade, capacidade, preco, dict_memoria))

        elif opcao == "3":
            id_trilha = input("ID da Trilha que deseja editar: ")
            campo = input(
                "Qual campo deseja alterar? (ex: preco, capacidade, local): ")
            novo_valor = input("Digite o novo valor: ")

            # Verifica o retorno booleano para confirmar se a edição passou pelas validações
            sucesso = editar_trilha(id_trilha, campo, novo_valor, dict_memoria)
            if sucesso:
                print("Trilha atualizada com sucesso!")

        elif opcao == "4":
            id_trilha = input("ID da Trilha que deseja excluir: ")
            print(excluir_trilha(id_trilha, dict_memoria))

        elif opcao == "5":
            listar_trilhas_admin(dict_memoria)

        elif opcao == "6":
            gerar_relatorio_geral(dict_memoria)

        elif opcao == "7":
            id_trilha = input("ID da Trilha: ")
            id_part = input("ID do Participante: ")
            registrar_checkin(id_trilha, id_part, dict_memoria)

        elif opcao == "0":
            print("Encerrando sessão do Guia...")
            break

        else:
            print("Opção inválida. Tente novamente.")

        # AUTO-SAVE: Grava os dados na memória física após cada operação, prevenindo perdas
        salvar_dados_sistema(NOME_ARQUIVO, dict_memoria)


def menu_trilheiro(id_atual, dict_memoria):
    """Controla o painel do cliente final, focado em consumo e reservas."""

    while True:
        print("\n" + "="*45)
        print("PAINEL DO TRILHEIRO")
        print("="*45)
        print("1. Ver Trilhas com Vagas Disponíveis")
        print("2. Buscar Trilhas por Dificuldade")
        print("3. Solicitar Reserva em Trilha")
        print("4. Cancelar Reserva")
        print("0. Encerrar Sessão (Voltar ao Login)")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            listar_trilhas_disponiveis(dict_memoria)

        elif opcao == "2":
            nivel = input(
                "Qual a dificuldade desejada? (Fácil/Média/Difícil): ")
            resultados = buscar_por_dificuldade(nivel, dict_memoria)

            # Valida se a busca retornou resultados antes de tentar imprimir
            if resultados:
                print(f"\nTrilhas encontradas ({nivel}):")
                for trilha in resultados:
                    print(f"- {trilha}")
            else:
                print("Nenhuma trilha encontrada com essa dificuldade.")

        elif opcao == "3":
            # Lista as vagas primeiro. Se não houver trilhas, não pede o ID desnecessariamente.
            if listar_trilhas_disponiveis(dict_memoria):
                id_trilha = input(
                    "\nDigite o ID da Trilha que deseja reservar: ")

                # O id_atual é repassado internamente para impedir reservas falsas
                print(solicitar_reserva(id_trilha, id_atual, dict_memoria))

        elif opcao == "4":
            id_trilha = input("Digite o ID da Trilha que deseja cancelar: ")
            remover_participante(id_trilha, id_atual, dict_memoria)

        elif opcao == "0":
            print("Encerrando sessão do Trilheiro...")
            break

        else:
            print("Opção inválida. Tente novamente.")

        # AUTO-SAVE: Garante que reservas e cancelamentos sejam salvos na hora
        salvar_dados_sistema(NOME_ARQUIVO, dict_memoria)


def main():
    """Ponto de entrada do sistema. Gerencia inicialização, autenticação e rotas."""
    print("Iniciando o Sistema Pé na Serra...")

    # Carrega o JSON para a memória RAM uma única vez, deixando o sistema rápido
    memoria_global = carregar_dados_sistema(NOME_ARQUIVO)

    while True:
        print("\n" + "*"*45)
        print(" BEM-VINDO AO PÉ NA SERRA - TELA DE ACESSO")
        print("*"*45)
        print("1. Fazer Login (Trilheiros e Guias)")
        print("0. Desligar Sistema")

        escolha_inicial = input("\nEscolha uma opção: ").strip()

        # Encerramento seguro com salvamento final preventivo
        if escolha_inicial == "0":
            print("Salvando dados de segurança e encerrando o sistema. Até breve!")
            salvar_dados_sistema(NOME_ARQUIVO, memoria_global)
            break

        elif escolha_inicial == "1":
            # Prende o usuário no laço de input até ele digitar um ID numérico válido
            id_inserido = receber_usuario()
            perfil = autenticar_usuario(id_inserido, memoria_global)

            # Rota de autenticação bem-sucedida
            if perfil == "Guia":
                print("\nAutenticação bem-sucedida! Entrando como GUIA...")
                menu_guia(id_inserido, memoria_global)

            elif perfil == "Trilheiro":
                print("\nAutenticação bem-sucedida! Entrando como TRILHEIRO...")
                menu_trilheiro(id_inserido, memoria_global)

            # Rota de cadastro: se o ID não existe, convida o usuário a se cadastrar
            else:
                print(
                    f"\nERRO: O ID {id_inserido} não está cadastrado em nossa base.")
                print("Deseja criar uma nova conta agora? (S/N)")
                fazer_cadastro = input("-> ").strip().upper()

                if fazer_cadastro == "S":
                    print("\n--- PORTAL DE CADASTRO ---")
                    print("1. Quero me cadastrar como Trilheiro")
                    print("2. Quero me cadastrar como Guia")
                    tipo_conta = input("Escolha o tipo de conta: ").strip()

                    if tipo_conta == "1":
                        nome = input("Digite seu Nome: ")
                        telefone = input("Digite seu Telefone: ")
                        print(cadastrar_participante(
                            nome, telefone, memoria_global))
                        salvar_dados_sistema(NOME_ARQUIVO, memoria_global)

                    elif tipo_conta == "2":
                        nome = input("Digite seu Nome: ")
                        telefone = input("Digite seu Telefone: ")
                        especialidade = input(
                            "Qual sua especialidade? (Ex: Montanhismo, Botânica): ")
                        print(cadastrar_guia(nome, telefone,
                              especialidade, memoria_global))
                        salvar_dados_sistema(NOME_ARQUIVO, memoria_global)

                    else:
                        print("Opção inválida. Cadastro cancelado.")

                else:
                    print("Retornando à tela inicial...")

        else:
            print("Opção inválida. Digite 1 ou 0.")


# Impede que os menus executem sozinhos caso o arquivo seja importado por outra interface no futuro.
if __name__ == "__main__":
    main()
