# ab-test-significance — calculadora grátis e de código aberto de significância de teste A/B

`ab-test-significance` é uma calculadora gratuita e de código aberto de
significância estatística de um teste A/B de duas proporções (teste z),
com p-valor, intervalo de confiança da diferença e o aviso de amostra
insuficiente — pensada para quem testa página de serviço com tráfego
baixo, onde "deu 3 conversões a mais" não quer dizer nada sozinho.

## O problema que ela resolve

Site de prestador de serviço raramente tem o volume de tráfego de um
e-commerce grande. Com poucas centenas de visitantes por variante, uma
diferença de conversão que parece grande pode não passar de ruído
estatístico. `ab-test-significance` calcula se a diferença observada é
estatisticamente significativa e, principalmente, avisa quando a amostra
atual é pequena demais para confiar no resultado — o erro mais comum de
quem interpreta teste A/B de olho.

## Como usar, passo a passo

**1. Instale.** Só biblioteca padrão do Python (3.9 ou mais recente, usa
`math`), sem dependência externa — não precisa de `scipy`:

```bash
git clone https://github.com/lucasferrazseo/ab-test-significance.git
cd ab-test-significance
```

**2. Rode com os números do seu teste**, visitantes e conversões de cada
variante:

```bash
python ab_test_significance.py --controle-visitantes 1000 --controle-conversoes 40 \
                                 --teste-visitantes 1000 --teste-conversoes 65
```

**3. Leia o resultado.** Exemplo real de saída:

```
=== ab-test-significance ===

Controle: 40/1000 = 4.00%
Teste:    65/1000 = 6.50%
Diferença (teste - controle): +2.50 pontos percentuais
Alfa: 0.05 | Intervalo de confiança 95%: [+0.55%, +4.45%]
z = 2.506 | p-valor = 0.0122
Resultado: ESTATISTICAMENTE SIGNIFICATIVO ao nível de 0.05

Amostra mínima recomendada por variante para detectar esta diferença com 80% de poder: ~1250 visitante(s)
ATENÇÃO: a amostra atual está abaixo da mínima recomendada — o resultado pode ser ruído, mesmo que pareça significativo.
```

Repare: mesmo com resultado "estatisticamente significativo" ao nível de
5%, a ferramenta avisou que a amostra está abaixo da mínima recomendada
para aquele tamanho de efeito — os dois números juntos é que dão o
diagnóstico completo, não um sozinho.

**4. Ajuste o nível de significância**, se seu critério não for o padrão
de 5%:

```bash
python ab_test_significance.py --controle-visitantes 200 --controle-conversoes 8 \
                                 --teste-visitantes 210 --teste-conversoes 12 --alfa 0.10
```

## Perguntas frequentes

**ab-test-significance é realmente grátis?**
Sim, código aberto sob licença MIT.

**O que significa "estatisticamente significativo"?**
Significa que a diferença observada é improvável de ter surgido só por
acaso, ao nível de confiança escolhido. Não significa necessariamente que
o efeito é grande ou que vale a pena — combine com o intervalo de
confiança e o contexto de negócio antes de decidir.

**Posso ficar checando o resultado todo dia até dar significativo?**
Não é recomendado — ver Limitações abaixo. "Peeking" (checar repetidas
vezes antes do fim do teste planejado) infla a chance de falso positivo,
mesmo que cada checagem individual pareça correta.

**Preciso de scipy ou outra biblioteca de estatística?**
Não. A ferramenta implementa o teste z e a função de distribuição normal
usando só o módulo `math` da biblioteca padrão.

## Limitações

O teste z de proporções é uma aproximação (assume distribuição
aproximadamente normal); com amostra muito pequena ou taxa de conversão
muito próxima de 0% ou 100%, um teste exato (Fisher) é mais correto. Não
corrige para múltiplas comparações — testar várias métricas ao mesmo
tempo aumenta a chance de falso positivo — nem para "peeking".

## Autor

[Lucas Ferraz](https://lucasferraz.com) — especialista em SEO, criação de
sites e SEO para IA, fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT — ver [LICENSE](LICENSE).
