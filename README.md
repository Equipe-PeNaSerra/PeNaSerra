# Sistema Pé na Serra

Olá! Bem-vindo(a) ao repositório do **Pé na Serra**.

Este projeto foi desenvolvido em equipe como avaliação parcial da disciplina de **Introdução à Programação**, no curso de Engenharia de Software na Universidade Federal do Cariri (UFCA). Trata-se de um sistema de linha de comando (CLI), construído inteiramente em Python, que atua como uma plataforma de conexão e gestão de atividades entre Guias e Trilheiros.

Nosso objetivo foi além dos requisitos da disciplina: priorizamos boas práticas de Engenharia de Software desde o início para construir um código **limpo, bem estruturado e resistente a falhas**.

## Problema que o projeto busca resolver

Atualmente, muitas agências de ecoturismo e guias independentes gerenciam suas excursões, vagas e clientes de forma manual (usando planilhas ou cadernos), o que gera confusão, lotação excedida e perda de dados. Por outro lado, os trilheiros têm dificuldade em encontrar rotas adequadas ao seu nível de experiência.

O **Pé na Serra** resolve esse problema centralizando a gestão em uma única plataforma digital. Ele automatiza o controle de vagas, a busca de rotas por dificuldade, o cálculo de faturamento para os guias e gamifica a experiência do usuário (trilheiro), tornando o ecoturismo mais organizado e seguro para ambas as partes.

## Descrição do projeto

O sistema manipula dicionários e armazena os dados em arquivos JSON. Ele possui duas frentes de acesso principais:

**Para os Guias (Administradores):**

* Cadastro, edição e exclusão de novas trilhas.
* Controle de capacidade (se a trilha lotar, o sistema avisa bloqueando novas reservas).
* Realização de check-in automático dos participantes no dia do evento.
* Geração de relatórios financeiros e de ocupação das trilhas.

**Para os Trilheiros (Clientes):**

* Busca inteligente de trilhas por nível de dificuldade (Fácil, Média, Difícil).
* Sistema de reservas "Self-Service".
* **Gamificação:** Quanto mais trilhas o usuário conclui, maior fica a sua patente no sistema (de Iniciante até Lenda das Trilhas).

## Instruções de execução

É super simples testar o nosso sistema na sua máquina. Você só precisa ter o **Python 3** instalado! Não é necessário configurar nenhum banco de dados pesado.

1. Clone este repositório para a sua máquina:

```bash
git clone https://github.com/Equipe-PeNaSerra/PeNaSerra.git

```

2. Entre na pasta do projeto:

```bash
cd PeNaSerra

```

3. Execute o arquivo principal:

```bash
python main.py

```

## Exemplos de uso

Aqui estão alguns fluxos de como você pode interagir com o sistema logo no primeiro acesso:

* **Criando uma conta (Primeiro Acesso):** Ao rodar o `main.py`, o sistema pedirá um ID de Login. Como o banco de dados estará vazio, digite um número qualquer (ex: `123`). O sistema informará que o ID não existe e perguntará se deseja criar uma conta. Escolha se deseja ser "Guia" ou "Trilheiro", preencha seu nome e pronto!
* **Ação do Guia (Cadastrar Trilha):** Logado como Guia, escolha a opção de "Registrar Nova Trilha". Informe o nome (ex: *Trilha do Pico da Bandeira*), local, nível de dificuldade, capacidade máxima de pessoas e o preço. A trilha será salva no sistema e você será automaticamente o guia responsável por ela.
* **Ação do Trilheiro (Fazer Reserva):** Logado como Trilheiro, escolha "Ver Trilhas com Vagas Disponíveis". Veja o ID da trilha cadastrada pelo guia no passo anterior, selecione a opção "Solicitar Reserva" e digite o ID da trilha. Sua vaga será garantida automaticamente.

## Divisão de tarefas entre os integrantes

A arquitetura do projeto foi modularizada e o escopo foi dividido entre os membros da equipe para o desenvolvimento das funções:

* **Tiago Pereira da Silva**: Responsável pelas funções de autenticação e manipulação de arquivos JSON (`autenticar_usuario`, `carregar_dados_sistema`, `salvar_dados_sistema`) e pela função `editar_trilha`.


* **Danilo Nunes Santos**: Responsável pela gestão de clientes e reservas, desenvolvendo as funções `cadastrar_participante`, `adicionar_participante`, `solicitar_reserva` e `gerar_relatorio_geral`.


* **Diêgo Ferreira de Carvalho**: Encarregado do CRUD dos profissionais e das trilhas, desenvolvendo as funções `cadastrar_guia`, `cadastrar_trilha`, `excluir_trilha`, `listar_trilhas_admin` e `listar_trilhas_disponiveis`.


* **Vinícius Gabriel Oliveira Santos**: Responsável pelas operações de conclusão e fluxos matemáticos, implementando as funções `registrar_checkin`, `remover_participante`, `calcular_faturamento`, `classificar_nivel` e `buscar_por_dificuldade`.



---

### Nossos maiores aprendizados neste projeto:

Como estudantes, implementamos conceitos como **Persistência de Dados (JSON)** com *Auto-Save*, **Prevenção de Bugs** com *try/except*, **Princípio DRY** (separando o código em módulos) e **Single Source of Truth**, provando que é possível fazer um projeto acadêmico com visão de mercado.
