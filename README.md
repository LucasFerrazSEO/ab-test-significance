**English** · [Português (Brasil)](README.pt-BR.md)

# ab-test-significance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`ab-test-significance` is a free, open source calculator for the
statistical significance of a two-proportion A/B test (z-test). It reports
the p-value, the confidence interval of the difference and a warning when
the sample is too small. It is built for people testing service pages with
low traffic, where "3 more conversions" means nothing on its own. It runs
locally with the Python standard library only.

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

Service provider websites rarely get the traffic of a large e-commerce
store. With a few hundred visitors per variant, a conversion difference
that looks large can be nothing more than statistical noise.
`ab-test-significance` calculates whether the observed difference is
statistically significant and, above all, warns you when the current
sample is too small to trust the result. That is the most common mistake
when people read an A/B test by eye.

## Installation

Python 3.9 or newer, standard library only (it uses `math`). No external
dependencies, `scipy` is not needed.

```bash
git clone https://github.com/LucasFerrazSEO/ab-test-significance.git
cd ab-test-significance
```

## Usage

**1. Run it with your test numbers**, visitors and conversions for each
variant:

```bash
python ab_test_significance.py --controle-visitantes 1000 --controle-conversoes 40 \
                                 --teste-visitantes 1000 --teste-conversoes 65
```

**2. Read the result.** Real output sample. The tool prints its report in
Brazilian Portuguese.

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

(Teste z de proporções, aproximação normal. Não corrige para múltiplas comparações nem para checagem repetida do resultado durante o teste.)
```

Note that even with a result that is "statistically significant" at the
5% level, the tool warns that the sample is below the recommended minimum
for that effect size. The two numbers together give the full diagnosis,
not either one alone.

**3. Change the significance level** if your threshold is not the default
5%:

```bash
python ab_test_significance.py --controle-visitantes 200 --controle-conversoes 8 \
                                 --teste-visitantes 210 --teste-conversoes 12 --alfa 0.10
```

## FAQ

**Is ab-test-significance really free?**
Yes. It is open source under the MIT license.

**What does "statistically significant" mean?**
It means the observed difference is unlikely to have happened by chance
alone, at the chosen confidence level. It does not necessarily mean the
effect is large or worth acting on. Combine it with the confidence
interval and the business context before you decide.

**Can I check the result every day until it becomes significant?**
It is not recommended (see Limitations below). "Peeking", checking
repeatedly before the planned end of the test, inflates the chance of a
false positive, even if each individual check looks correct.

**Do I need scipy or another statistics library?**
No. The tool implements the z-test and the normal distribution function
using only the `math` module from the standard library.

## Limitations

The two-proportion z-test is an approximation (it assumes a roughly normal
distribution). With a very small sample, or a conversion rate very close
to 0% or 100%, an exact test (Fisher) is more accurate. It does not
correct for multiple comparisons (testing several metrics at once raises
the chance of a false positive) or for peeking.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/ab-test-significance/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
