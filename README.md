# Analisador de Complexidade Ciclomática para Lox

## Integrantes

Letícia Kellen Ramos Paiva — Matrícula: 221037803 — Turma: 18H

## Introdução

Este projeto implementa um analisador estático para a linguagem Lox, com foco em calcular automaticamente:

- **Complexidade ciclomática:** quantos caminhos independentes existem em cada função
- **Profundidade máxima de aninhamento:** quantos níveis de blocos de decisão existem dentro de cada função
- **Código morto:** linhas após um `return` que nunca são executadas

A ferramenta foi construída em Python, empregando expressões regulares para análise léxica e sintática simples, além de lógica para detectar blocos de código e decisões.

O projeto exemplifica, na prática, conceitos centrais da disciplina de Compiladores: análise léxica, análise sintática, análise semântica simplificada e parsing. Além disso, reforça a utilidade de ferramentas automáticas para análise estática de código-fonte de linguagens de programação.

## Exemplos de comandos analisados

A linguagem Lox tem sintaxe similar a C/JavaScript. Exemplo:

```lox
fun buscaMaior(lista) {
    var maior = lista[0];
    for (var i = 1; i < lista.length; i = i + 1) {
        if (lista[i] > maior and lista[i] != 0) {
            maior = lista[i];
        }
    }
    return maior;
    print "código morto!";
}
```

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu_usuario/lox-complexity.git
cd lox-complexity
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Estrutura do Projeto

```text
lox-complexity/
├── exemplos/
│   ├── avancado.lox
│   ├── code_morto.lox
│   ├── edgecases.lox
│   ├── recursivo.lox
│   └── simples.lox
├── img/
│   └── grafico_exemplo.png
├── lox_cyclomatic.py
├── README.md
└── requirements.txt
```

## Como executar

- **Analisar todos os exemplos**

  ```bash
  python lox_cyclomatic.py exemplos/
  ```

- **Gerar gráfico de barras:**

  ```bash
  python lox_cyclomatic.py exemplos/ --grafico
  ```

- **Mostrar o corpo das funções:**

  ```bash
  python lox_cyclomatic.py exemplos/ --corpo
  ```

- **Analisar um arquivo específico:**

  ```bash
  python lox_cyclomatic.py exemplos/simples.lox
  ```

## Exemplos

A pasta `exemplos/` contém arquivos de código Lox com diferentes graus de complexidade, incluindo:

- Função simples (Hello World)
- Decisão (`if`/`else`)
- Estrutura de repetição (`for`, `while`)
- Função recursiva (fatorial)
- Código morto após `return`
- Aninhamento de blocos

Exemplo de código em `exemplos/recursivo.lox`:

```lox
fun fatorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n - 1);
}
```

## Estrutura do código

- **lox_cyclomatic.py:** Script principal do analisador. Contém:
  - Leitura de arquivos/pastas `.lox`
  - Identificação de funções com regex
  - Cálculo de complexidade ciclomática, profundidade máxima de aninhamento e detecção de código morto
  - Geração de relatórios tabulares e gráficos
- **exemplos/**: Pasta com exemplos variados para análise
- **img/**: Pasta para o gráfico gerado automaticamente
- **requirements.txt:** Lista das dependências (`matplotlib`)

## Etapas de compilação implementadas

- **Análise léxica:** Identificação de tokens e comandos usando expressões regulares
- **Análise sintática:** Reconhecimento de blocos de funções e estruturas de decisão (`if`, `for`, `while`)
- **Análise semântica:** Detecção simples de código morto (linhas após return)

## Bugs, limitações e problemas conhecidos

- O parser é simplificado, não detecta funções aninhadas ou blocos muito complexos
- A detecção de código morto só funciona para o caso direto de linhas após `return`
- A contagem de aninhamento é feita apenas para blocos do tipo `if`, `for`, `while`
- Não há parsing sintático completo da linguagem Lox

## Referências

- Thomas J. McCabe, *A Complexity Measure*, IEEE Transactions on Software Engineering, 1976
- Crafting Interpreters (Bob Nystrom)
- Documentação do Python (regex, matplotlib)


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Hppw7Zh2)

