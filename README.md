# Sistema Pé na Serra

Olá! Bem-vindo(a) ao repositório do **Pé na Serra**.

Este projeto foi desenvolvido em equipe como avaliação parcial da disciplina de **Introdução à Programação**. Trata-se de um sistema de linha de comando (CLI), construído inteiramente em Python, que propõe uma solução conceitual para o ecoturismo, atuando como uma plataforma de conexão e gestão de atividades entre Guias e Trilheiros.

Nosso objetivo foi além dos requisitos da disciplina: priorizamos boas práticas de Engenharia de Software desde o início para construir um código **limpo, bem estruturado e resistente a falhas**.

## O que o sistema faz?

O sistema possui duas frentes de acesso principais:

**Para os Guias (Administradores):**

* Cadastro, edição e exclusão de novas trilhas.
* Controle de capacidade (se a trilha lotar, o sistema avisa).
* Realização de check-in automático dos participantes no dia do evento.
* Geração de relatórios financeiros e de ocupação das trilhas.

**Para os Trilheiros (Clientes):**

* Busca inteligente de trilhas por nível de dificuldade (Fácil, Média, Difícil).
* Sistema de reservas "Self-Service".
* **Gamificação:** Quanto mais trilhas o usuário conclui, maior fica o seu "nível" no sistema (de Iniciante até Lenda das Trilhas).

Se o usuário tentar fazer login e não tiver um ID, o próprio sistema o convida para fazer um cadastro rápido na hora!

## Nossos maiores aprendizados neste projeto

Como estudantes de Engenharia de Software, usamos esse trabalho em grupo para colocar em prática vários conceitos importantes que vão além do básico da programação:

* **Persistência de dados (JSON):** O sistema não perde os dados quando é fechado. Implementamos uma rotina que cria e atualiza um arquivo `banco_de_dados.json` automaticamente (Auto-Save).
* **Prevenção de bugs e tratamento de erros:** Usamos blocos `try/except` para garantir que o programa não trave se o usuário digitar uma letra no lugar de um número, por exemplo. Também implementamos proteções matemáticas (como evitar divisão por zero nos relatórios).
* **Princípio DRY (Don't Repeat Yourself):** Organizamos o projeto em vários arquivos separados (modularização) para facilitar o trabalho em equipe e não repetir as mesmas validações várias vezes. O `main.py` cuida só dos menus da interface, enquanto os outros arquivos lidam com as regras de negócio.
* **Single Source of Truth (Ponto Único da Verdade):** Garantimos que informações cruciais (como os IDs numéricos e o nome do arquivo do banco de dados) fossem tratadas através de constantes ou de buscas diretas na memória global, evitando conflitos de dados.

## Rodando o projeto!

É super simples testar o nosso sistema na sua máquina. Você só precisa ter o **Python 3** instalado! Não é necessário configurar nenhum banco de dados pesado.

1. Clone este repositório:
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



**Dica para o primeiro acesso:** O sistema vai criar o arquivo de dados sozinho na primeira vez que você rodar. Quando pedir o Login, digite qualquer número (ex: `123`) para ser direcionado ao menu de criação de conta e divirta-se!

---

*Projeto feito com dedicação, trabalho em equipe e MUITO esforço por:*

* **Danilo Nunes Santos**
* **Diêgo Ferreira de Carvalho**
* **Tiago Pereira da Silva**
* **Vinícius Gabriel Oliveira Santos**

*Alunos de Engenharia de Software - [Universidade Federal do Cariri - UFCA]*

---
