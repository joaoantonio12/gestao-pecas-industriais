# ============================================================
# Sistema de Gestao de Pecas Industriais
# Desafio de Automacao Digital - Qualidade e Armazenamento
# ============================================================

from datetime import datetime

# ---------- Dados globais ----------
pecas_aprovadas = []      # Lista de dicts com dados das pecas aprovadas
pecas_reprovadas = []     # Lista de dicts com dados das pecas reprovadas e motivos
caixa_atual = []          # Lista de IDs das pecas na caixa aberta
caixas_fechadas = []      # Lista de dicts com info das caixas ja fechadas
numero_caixa = 1          # Contador de caixas


def avaliar_peca(peso, cor, comprimento):
    """
    Avalia uma peca com base nos criterios de qualidade.
    Retorna uma tupla (aprovada, motivos) onde:
      - aprovada: True se passou em todos os criterios
      - motivos: lista com os motivos de reprovacao (vazia se aprovada)
    """
    motivos = []

    # Criterio 1: peso entre 95g e 105g
    if peso < 95 or peso > 105:
        motivos.append("Peso fora do intervalo (95g a 105g)")

    # Criterio 2: cor deve ser azul ou verde
    if cor.lower() not in ("azul", "verde"):
        motivos.append("Cor invalida (deve ser azul ou verde)")

    # Criterio 3: comprimento entre 10cm e 20cm
    if comprimento < 10 or comprimento > 20:
        motivos.append("Comprimento fora do intervalo (10cm a 20cm)")

    aprovada = len(motivos) == 0
    return aprovada, motivos


def fechar_caixa():
    """
    Fecha a caixa atual: salva seus dados nas caixas_fechadas
    e inicia uma nova caixa vazia.
    """
    global caixa_atual, numero_caixa

    caixa = {
        "numero": numero_caixa,
        "pecas": list(caixa_atual),
        "quantidade": len(caixa_atual),
        "fechamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    caixas_fechadas.append(caixa)

    print(f"\n>>> Caixa {numero_caixa} FECHADA com {len(caixa_atual)} pecas! <<<")
    print(f"    Data/hora: {caixa['fechamento']}")

    caixa_atual = []
    numero_caixa += 1
    print(f">>> Nova caixa {numero_caixa} aberta. <<<")


def cadastrar_peca():
    """
    Solicita os dados de uma nova peca ao usuario, valida as entradas,
    avalia a qualidade e armazena na lista correta (aprovadas ou reprovadas).
    Se a caixa atual atingir 10 pecas, fecha automaticamente.
    """
    global caixa_atual

    print("\n" + "=" * 50)
    print("       CADASTRO DE NOVA PECA")
    print("=" * 50)

    # Solicitar ID
    id_peca = input("ID da peca: ").strip()
    if not id_peca:
        print("[ERRO] O ID nao pode ser vazio.")
        return

    # Verificar se ID ja existe
    for p in pecas_aprovadas:
        if p["id"] == id_peca:
            print(f"[ERRO] Ja existe uma peca com o ID '{id_peca}'.")
            return
    for p in pecas_reprovadas:
        if p["id"] == id_peca:
            print(f"[ERRO] Ja existe uma peca com o ID '{id_peca}'.")
            return

    # Solicitar peso com validacao
    try:
        peso = float(input("Peso (em gramas): "))
    except ValueError:
        print("[ERRO] Peso invalido. Informe um numero.")
        return

    # Solicitar cor
    cor = input("Cor: ").strip()
    if not cor:
        print("[ERRO] A cor nao pode ser vazia.")
        return

    # Solicitar comprimento com validacao
    try:
        comprimento = float(input("Comprimento (em cm): "))
    except ValueError:
        print("[ERRO] Comprimento invalido. Informe um numero.")
        return

    # Avaliar a peca
    aprovada, motivos = avaliar_peca(peso, cor, comprimento)

    print("-" * 50)

    if aprovada:
        peca = {
            "id": id_peca,
            "peso": peso,
            "cor": cor,
            "comprimento": comprimento,
            "caixa": numero_caixa
        }
        pecas_aprovadas.append(peca)
        caixa_atual.append(id_peca)

        print(f"RESULTADO: APROVADA")
        print(f"  Peca '{id_peca}' adicionada a Caixa {numero_caixa}.")
        print(f"  Pecas na caixa atual: {len(caixa_atual)}/10")

        # Verificar se a caixa atingiu a capacidade maxima
        if len(caixa_atual) == 10:
            fechar_caixa()
    else:
        peca = {
            "id": id_peca,
            "peso": peso,
            "cor": cor,
            "comprimento": comprimento,
            "motivos": motivos
        }
        pecas_reprovadas.append(peca)

        print(f"RESULTADO: REPROVADA")
        print(f"  Motivo(s):")
        for m in motivos:
            print(f"    - {m}")

    print("-" * 50)


def listar_pecas():
    """
    Lista todas as pecas cadastradas, separando aprovadas e reprovadas.
    Mostra o numero da caixa para aprovadas e os motivos para reprovadas.
    """
    print("\n" + "=" * 50)
    print("       LISTAGEM DE PECAS")
    print("=" * 50)

    # Pecas aprovadas
    print("\n--- PECAS APROVADAS ---")
    if not pecas_aprovadas:
        print("  Nenhuma peca aprovada.")
    else:
        for p in pecas_aprovadas:
            print(f"  ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | "
                  f"Comprimento: {p['comprimento']}cm | Caixa: {p['caixa']}")

    # Pecas reprovadas
    print("\n--- PECAS REPROVADAS ---")
    if not pecas_reprovadas:
        print("  Nenhuma peca reprovada.")
    else:
        for p in pecas_reprovadas:
            motivos_str = ", ".join(p["motivos"])
            print(f"  ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | "
                  f"Comprimento: {p['comprimento']}cm")
            print(f"    Motivo(s): {motivos_str}")

    print("=" * 50)


def remover_peca():
    """
    Remove uma peca pelo ID, buscando tanto nas aprovadas quanto nas reprovadas.
    Se a peca estava aprovada e na caixa atual, reorganiza a caixa.
    """
    global caixa_atual

    print("\n" + "=" * 50)
    print("       REMOVER PECA")
    print("=" * 50)

    id_peca = input("Informe o ID da peca a remover: ").strip()

    # Buscar nas aprovadas
    for i, p in enumerate(pecas_aprovadas):
        if p["id"] == id_peca:
            pecas_aprovadas.pop(i)

            # Remover da caixa atual se estiver la
            if id_peca in caixa_atual:
                caixa_atual.remove(id_peca)
                print(f"  Peca '{id_peca}' removida da caixa atual.")
            else:
                print(f"  Peca '{id_peca}' estava em uma caixa ja fechada.")
                # Remover da caixa fechada correspondente
                for caixa in caixas_fechadas:
                    if id_peca in caixa["pecas"]:
                        caixa["pecas"].remove(id_peca)
                        caixa["quantidade"] -= 1
                        print(f"  Removida da Caixa {caixa['numero']}.")
                        break

            print(f"  Peca aprovada '{id_peca}' removida com sucesso!")
            return

    # Buscar nas reprovadas
    for i, p in enumerate(pecas_reprovadas):
        if p["id"] == id_peca:
            pecas_reprovadas.pop(i)
            print(f"  Peca reprovada '{id_peca}' removida com sucesso!")
            return

    print(f"  [ERRO] Peca com ID '{id_peca}' nao encontrada.")


def listar_caixas():
    """
    Lista todas as caixas fechadas com suas informacoes:
    numero, quantidade de pecas, lista de IDs e data/hora de fechamento.
    """
    print("\n" + "=" * 50)
    print("       CAIXAS FECHADAS")
    print("=" * 50)

    if not caixas_fechadas:
        print("  Nenhuma caixa foi fechada ainda.")
    else:
        for caixa in caixas_fechadas:
            print(f"\n  Caixa {caixa['numero']}:")
            print(f"    Quantidade de pecas: {caixa['quantidade']}")
            print(f"    IDs das pecas: {', '.join(caixa['pecas'])}")
            print(f"    Fechamento: {caixa['fechamento']}")

    # Mostrar caixa atual
    print(f"\n  --- Caixa atual (Caixa {numero_caixa}): "
          f"{len(caixa_atual)}/10 pecas ---")
    if caixa_atual:
        print(f"    IDs: {', '.join(caixa_atual)}")

    print("=" * 50)


def gerar_relatorio():
    """
    Gera um relatorio consolidado com:
    - Total de pecas cadastradas (aprovadas + reprovadas)
    - Total de aprovadas e reprovadas
    - Detalhamento dos motivos de reprovacao
    - Quantidade de caixas fechadas e estado da caixa atual
    """
    print("\n" + "=" * 50)
    print("       RELATORIO FINAL")
    print("=" * 50)

    total_aprovadas = len(pecas_aprovadas)
    total_reprovadas = len(pecas_reprovadas)
    total = total_aprovadas + total_reprovadas

    print(f"\n  Total de pecas cadastradas: {total}")
    print(f"  Total de pecas aprovadas:   {total_aprovadas}")
    print(f"  Total de pecas reprovadas:  {total_reprovadas}")

    # Detalhamento dos motivos de reprovacao
    print("\n  --- Detalhamento dos motivos de reprovacao ---")
    if not pecas_reprovadas:
        print("  Nenhuma peca reprovada.")
    else:
        contagem_motivos = {}
        for p in pecas_reprovadas:
            for m in p["motivos"]:
                if m in contagem_motivos:
                    contagem_motivos[m] += 1
                else:
                    contagem_motivos[m] = 1

        for motivo, quantidade in contagem_motivos.items():
            print(f"    - {motivo}: {quantidade} peca(s)")

    # Informacoes sobre caixas
    print("\n  --- Informacoes sobre caixas ---")
    print(f"  Caixas fechadas: {len(caixas_fechadas)}")

    if caixa_atual:
        print(f"  Caixa atual (Caixa {numero_caixa}): "
              f"{len(caixa_atual)} peca(s)")
    else:
        print(f"  Caixa atual (Caixa {numero_caixa}): vazia")

    print("=" * 50)


def exibir_menu():
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 50)
    print("  SISTEMA DE GESTAO DE PECAS INDUSTRIAIS")
    print("=" * 50)
    print("  1. Cadastrar nova peca")
    print("  2. Listar pecas aprovadas/reprovadas")
    print("  3. Remover peca cadastrada")
    print("  4. Listar caixas fechadas")
    print("  5. Gerar relatorio final")
    print("  0. Sair")
    print("=" * 50)


def main():
    """Funcao principal que controla o loop do menu interativo."""
    while True:
        exibir_menu()
        opcao = input("  Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_peca()
        elif opcao == "2":
            listar_pecas()
        elif opcao == "3":
            remover_peca()
        elif opcao == "4":
            listar_caixas()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "0":
            print("\n  Encerrando o sistema. Ate logo!")
            break
        else:
            print("\n  [ERRO] Opcao invalida. Tente novamente.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
