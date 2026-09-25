#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ab-test-significance — calcula significância estatística de um teste A/B de
duas proporções (teste z), com p-valor, intervalo de confiança da
diferença e o aviso de amostra insuficiente — pensado para quem testa
página de serviço com tráfego baixo, onde "deu 3 conversões a mais" não
quer dizer nada sozinho.

O QUE FAZ
    Recebe visitantes e conversões de duas variantes (controle e teste) e
    calcula:

    1. Taxa de conversão de cada variante.
    2. Teste z de duas proporções (aproximação normal, pooled variance) e o
       p-valor associado.
    3. Intervalo de confiança (padrão 95%) da diferença entre as taxas.
    4. Amostra mínima recomendada para detectar a diferença observada com
       80% de poder, ao nível de significância escolhido — para avisar
       quando o teste simplesmente não tem visitante suficiente para
       confiar no resultado.

USO
    python ab_test_significance.py --controle-visitantes 1000 --controle-conversoes 40 \\
                                     --teste-visitantes 1000 --teste-conversoes 55
    python ab_test_significance.py --controle-visitantes 200 --controle-conversoes 8 \\
                                     --teste-visitantes 210 --teste-conversoes 12 --alfa 0.10

LIMITAÇÕES
    Teste z de proporções é uma aproximação (assume distribuição
    aproximadamente normal); com amostra muito pequena ou taxa de conversão
    muito próxima de 0% ou 100%, um teste exato (Fisher) é mais correto.
    Não corrige para múltiplas comparações (testar várias métricas ao mesmo
    tempo aumenta a chance de falso positivo) nem para "peeking" (checar o
    resultado repetidas vezes antes do fim do teste planejado).

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão (math).
Licença: MIT.
"""
from __future__ import annotations

import argparse
import math

Z_ALFA = {0.01: 2.5758, 0.05: 1.9600, 0.10: 1.6449}
Z_PODER_80 = 0.8416


def cdf_normal(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def p_valor_bicaudal(z: float) -> float:
    return 2 * (1 - cdf_normal(abs(z)))


def z_alfa(alfa: float) -> float:
    if alfa in Z_ALFA:
        return Z_ALFA[alfa]
    # aproximação por busca binária na normal padrão para alfa fora da tabela
    lo, hi = 0.0, 6.0
    alvo = 1 - alfa / 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if cdf_normal(mid) < alvo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Significância estatística de teste A/B de duas proporções (teste z)."
    )
    ap.add_argument("--controle-visitantes", type=int, required=True)
    ap.add_argument("--controle-conversoes", type=int, required=True)
    ap.add_argument("--teste-visitantes", type=int, required=True)
    ap.add_argument("--teste-conversoes", type=int, required=True)
    ap.add_argument("--alfa", type=float, default=0.05, help="nível de significância (padrão 0.05)")
    args = ap.parse_args()

    n1, x1 = args.controle_visitantes, args.controle_conversoes
    n2, x2 = args.teste_visitantes, args.teste_conversoes
    if x1 > n1 or x2 > n2 or n1 <= 0 or n2 <= 0:
        ap.error("conversões não podem exceder visitantes, e visitantes precisam ser positivos")

    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    erro_padrao_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / erro_padrao_pool if erro_padrao_pool > 0 else 0.0
    p_valor = p_valor_bicaudal(z)

    erro_padrao_diff = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_ic = z_alfa(args.alfa)
    diff = p2 - p1
    ic_baixo, ic_alto = diff - z_ic * erro_padrao_diff, diff + z_ic * erro_padrao_diff

    # amostra mínima por braço para detectar a diferença observada com 80% de poder
    if p1 not in (0, 1) and abs(diff) > 0:
        p_media = (p1 + p2) / 2
        numerador = (z_ic + Z_PODER_80) ** 2 * 2 * p_media * (1 - p_media)
        amostra_min = math.ceil(numerador / (diff ** 2))
    else:
        amostra_min = None

    significativo = p_valor < args.alfa

    print("\n=== ab-test-significance ===\n")
    print(f"Controle: {x1}/{n1} = {p1*100:.2f}%")
    print(f"Teste:    {x2}/{n2} = {p2*100:.2f}%")
    print(f"Diferença (teste - controle): {diff*100:+.2f} pontos percentuais")
    print(f"Alfa: {args.alfa} | Intervalo de confiança {int((1-args.alfa)*100)}%: "
          f"[{ic_baixo*100:+.2f}%, {ic_alto*100:+.2f}%]")
    print(f"z = {z:.3f} | p-valor = {p_valor:.4f}")
    print(f"Resultado: {'ESTATISTICAMENTE SIGNIFICATIVO' if significativo else 'não significativo'} "
          f"ao nível de {args.alfa}")

    if amostra_min:
        print(f"\nAmostra mínima recomendada por variante para detectar esta diferença "
              f"com 80% de poder: ~{amostra_min} visitante(s)")
        if n1 < amostra_min or n2 < amostra_min:
            print("ATENÇÃO: a amostra atual está abaixo da mínima recomendada — "
                  "o resultado pode ser ruído, mesmo que pareça significativo.")

    print("\n(Teste z de proporções, aproximação normal. Não corrige para múltiplas "
          "comparações nem para checagem repetida do resultado durante o teste.)")


if __name__ == "__main__":
    main()
