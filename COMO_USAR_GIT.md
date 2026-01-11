# 🎓 Guia Básico de Git para o TCC

Este guia vai te ajudar a trabalhar com o Git e GitHub sem medo! Pense no Git como um "o jogo salvo" do nosso trabalho. A gente pode salvar o progresso, voltar atrás se der erro e juntar o que eu fiz com o que você fez.

O nosso repositório online é: `https://github.com/Costenar0/TCC_leo.git`

---

## 🚀 1. Primeira vez (Baixando o projeto)

Se você ainda não tem a pasta do projeto no seu computador, você precisa "clonar" (baixar) ela.

1. **Abra o Terminal na pasta certa:**
    * **Método Ninja (Windows):** Abra a pasta onde você quer baixar o projeto (ex: Documents). Segure a tecla `SHIFT` do teclado, clique com o **botão direito** do mouse em um espaço vazio da pasta e escolha **"Abrir janela do PowerShell aqui"** ou **"Abrir no Terminal"**.
    * *Assim você não precisa usar comandos de navegação como `cd`.*

2. **Baixe o repositório:**
    Cole este comando no terminal e aperte Enter:

    ```bash
    git clone https://github.com/Costenar0/TCC_leo.git
    ```

3. **Entre na pasta criada:**
    Agora entre na nova pasta `TCC_leo` que apareceu, clique com botão direito nela e abra o terminal ali novamente para começar a trabalhar.

---

## 🔄 2. Rotina de Trabalho (Dia a dia)

Sempre que for começar a trabalhar, siga essa ordem sagrada para evitar problemas:

### Passo 1: Atualize sua pasta (Pull)

Antes de escrever qualquer código, baixe as mudanças que eu fiz.

```bash
git pull origin main
```

*Tradução: "Git, puxe (pull) do servidor (origin) as novidades da linha principal (main)."*

### Passo 2: Trabalhe

Faça suas alterações, edite o código, crie arquivos, etc.

### Passo 3: Verifique o que mudou (Status)

Veja quais arquivos você mexeu.

```bash
git status
```

*Os arquivos vermelhos são os que você mudou mas ainda não preparou para salvar.*

### Passo 4: Prepare o salvamento (Add)

Diga ao Git quais arquivos você quer incluir no "pacote" de salvamento.

```bash
git add .
```

*O ponto `.` significa "todos os arquivos modificados". Se quiser só um específico, troque o ponto pelo nome do arquivo.*

### Passo 5: Salve com uma mensagem (Commit)

Crie o "ponto de salvamento" com uma mensagem explicando o que você fez.

```bash
git commit -m "Explique aqui o que você fez"
```

*Exemplo: `git commit -m "Adicionei comentários no gráfico"`*

### Passo 6: Envie para a nuvem (Push)

Envie suas alterações para o GitHub para que eu possa ver.

```bash
git push origin main
```

*Tradução: "Git, empurre (push) para o servidor (origin) na linha principal (main)."*

---

## 🌳 3. Trabalhando com Branches (Ramos) - Nível Avançado

Isso aqui é o segredo para não quebrarmos o código um do outro.

### O que é uma Branch?

Imagine que a branch `main` é o nosso **Trabalho Oficial Impecável**. Se a gente mexer direto nele e der erro, o projeto para.
Uma **Branch** é como criar um **universo paralelo** idêntico ao oficial. Você entra nesse universo, faz bagunça, testa, erra, conserta.

* Se ficar ruim: A gente apaga o universo paralelo e nada aconteceu no oficial.
* Se ficar bom: A gente **funde** (Merge) o universo paralelo com o oficial.

### Como usar?

1. **Crie sua branch** (seu universo):

    ```bash
    git checkout -b nova-analise-financeira
    ```

    *Cria e entra numa branch chamada `nova-analise-financeira`.*

2. **Trabalhe normalmente**:
    (Código, `git add .`, `git commit`...)

3. **Envie sua branch**:
    Como essa branch não existe lá na internet ainda, o comando muda um pouco na primeira vez:

    ```bash
    git push origin nova-analise-financeira
    ```

4. **Juntando tudo**:
    Depois que você enviou, você me avisa. Eu vou entrar no GitHub e fazer um "Pull Request" (Pedido para puxar) e aceitar suas mudanças, misturando sua branch com a `main`.

---

## ⚠️ Dicas de Ouro

1. **Faça commits pequenos:** Não espere terminar o TCC inteiro para salvar. Fez uma função? Commit. Arrumou um erro? Commit.
2. **Deu erro no Push?** Provavelmente eu fiz alguma alteração e enviei antes de você. O Git vai pedir para você fazer um `git pull` antes. Faça o pull, o Git vai tentar misturar os arquivos automaticamente. Se der certo, faça o push de novo.

---

## 🆘 Resumo dos Comandos

| Comando | O que faz? |
| :--- | :--- |
| `git clone [link]` | Baixa o projeto pela primeira vez. |
| `git pull` | **Atualiza** seu PC com as novidades da nuvem. |
| `git status` | Mostra o que você mudou. |
| `git add .` | Prepara tudo para salvar. |
| `git commit -m "..."` | **Salva** o progresso no seu PC. |
| `git push` | **Envia** seu progresso para a nuvem. |
| `git checkout -b [nome]` | Cria uma nova branch (universo paralelo). |

---

## 🏆 Por que aprender isso? (Dica de Amigo)

Pode parecer chato digitar esses comandos nessa "tela preta", mas o Git é **obrigatório** no mercado de trabalho.
Google, Amazon, bancos, startups... **todo mundo usa Git**.
Aprender isso agora para o TCC vai te colocar **anos-luz na frente** da maioria dos iniciantes. É uma super habilidade para colocar no currículo! 🚀
