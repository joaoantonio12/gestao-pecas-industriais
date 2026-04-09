# Sistema de Gestao de Pecas Industriais

## Descricao

Sistema desenvolvido em Python para automatizar o controle de qualidade e armazenamento de pecas industriais em uma linha de montagem. O programa substitui a inspecao manual por um processo digital que avalia, classifica e organiza as pecas de forma automatica, gerando relatorios consolidados.

Projeto desenvolvido como parte da disciplina **Algoritmos e Logica de Programacao** — UniFECAF.

---

## Funcionalidades

| Opcao | Funcionalidade | Descricao |
|-------|---------------|-----------|
| 1 | Cadastrar nova peca | Recebe ID, peso, cor e comprimento. Avalia e classifica como aprovada ou reprovada |
| 2 | Listar pecas | Exibe pecas aprovadas (com caixa) e reprovadas (com motivos) separadamente |
| 3 | Remover peca | Busca por ID e remove de qualquer lista (aprovadas ou reprovadas) |
| 4 | Listar caixas fechadas | Mostra caixas fechadas com numero, IDs, quantidade e data/hora |
| 5 | Gerar relatorio final | Totais, detalhamento de motivos de reprovacao e estado das caixas |
| 0 | Sair | Encerra o sistema |

---

## Regras de Qualidade

Uma peca e **aprovada** somente se atender a **todos** os criterios abaixo:

| Criterio | Condicao |
|----------|----------|
| Peso | Entre 95g e 105g |
| Cor | Azul ou Verde (case-insensitive) |
| Comprimento | Entre 10cm e 20cm |

Se a peca falhar em **qualquer** criterio, ela e **reprovada** e os motivos sao registrados.

### Armazenamento em Caixas

- Pecas aprovadas sao armazenadas em caixas com capacidade de **10 pecas**.
- Quando a caixa atinge 10 pecas, ela e **fechada automaticamente** (com timestamp) e uma nova caixa e aberta.

---

## Como Executar

### Pre-requisitos

- Python 3.6 ou superior instalado. Baixe em: https://www.python.org/downloads/

### Passo a passo

1. **Baixe ou clone o projeto** para uma pasta no seu computador.

2. **Abra o terminal** (Prompt de Comando, PowerShell ou terminal do VS Code).

3. **Navegue ate a pasta do projeto**:
   ```
   cd caminho/para/a/pasta/TRABALHO
   ```

4. **Execute o programa**:
   ```
   python sistema.py
   ```

5. O menu interativo sera exibido. Escolha as opcoes digitando o numero correspondente.

---

## Exemplo de Uso

Abaixo esta uma sequencia de entradas e saidas esperadas para 3 pecas:

### Peca 1 — Aprovada

```
Escolha uma opcao: 1

==================================================
       CADASTRO DE NOVA PECA
==================================================
ID da peca: P001
Peso (em gramas): 100
Cor: azul
Comprimento (em cm): 15
--------------------------------------------------
RESULTADO: APROVADA
  Peca 'P001' adicionada a Caixa 1.
  Pecas na caixa atual: 1/10
--------------------------------------------------
```

### Peca 2 — Reprovada (peso fora do intervalo)

```
Escolha uma opcao: 1

==================================================
       CADASTRO DE NOVA PECA
==================================================
ID da peca: P002
Peso (em gramas): 110
Cor: verde
Comprimento (em cm): 12
--------------------------------------------------
RESULTADO: REPROVADA
  Motivo(s):
    - Peso fora do intervalo (95g a 105g)
--------------------------------------------------
```

### Peca 3 — Reprovada (cor invalida + comprimento fora)

```
Escolha uma opcao: 1

==================================================
       CADASTRO DE NOVA PECA
==================================================
ID da peca: P003
Peso (em gramas): 100
Cor: vermelho
Comprimento (em cm): 25
--------------------------------------------------
RESULTADO: REPROVADA
  Motivo(s):
    - Cor invalida (deve ser azul ou verde)
    - Comprimento fora do intervalo (10cm a 20cm)
--------------------------------------------------
```

### Relatorio final apos as 3 pecas

```
Escolha uma opcao: 5

==================================================
       RELATORIO FINAL
==================================================

  Total de pecas cadastradas: 3
  Total de pecas aprovadas:   1
  Total de pecas reprovadas:  2

  --- Detalhamento dos motivos de reprovacao ---
    - Peso fora do intervalo (95g a 105g): 1 peca(s)
    - Cor invalida (deve ser azul ou verde): 1 peca(s)
    - Comprimento fora do intervalo (10cm a 20cm): 1 peca(s)

  --- Informacoes sobre caixas ---
  Caixas fechadas: 0
  Caixa atual (Caixa 1): 1 peca(s)
==================================================
```

---

## Estrutura do Projeto

```
TRABALHO/
├── sistema.py           # Codigo-fonte principal do sistema
├── README.md            # Documentacao do projeto (este arquivo)
└── parte_teorica.docx   # Documento com analise teorica e reflexao
```

---

## Tecnologias Utilizadas

- **Python 3** — Linguagem de programacao
- **Biblioteca datetime** — Para registrar data/hora de fechamento das caixas
- **Terminal/Console** — Interface interativa via linha de comando
