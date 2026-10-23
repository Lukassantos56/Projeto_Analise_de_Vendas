# Conclusões da análise

Base simulada com 400 pedidos entre janeiro e junho de 2026, gerada de forma reprodutível (`scripts/gerar_dados.py`) e validada rodando todas as consultas de `sql/analises.sql` (`scripts/testar_consultas.py`).

## KPIs gerais

| Indicador | Valor |
|---|---|
| Faturamento total | R$ 1.395.783,50 (≈ R$ 1,40 Mi) |
| Pedidos | 400 |
| Unidades vendidas | 807 |
| Ticket médio | R$ 3.489,46 |
| Clientes ativos | 59 (de 60 cadastrados) |

## Faturamento por mês

| Mês | Faturamento | Variação vs. mês anterior |
|---|---|---|
| 2026-01 | R$ 162.723,00 | — |
| 2026-02 | R$ 237.036,00 | +45,7% |
| 2026-03 | R$ 262.452,50 | +10,7% |
| 2026-04 | R$ 272.969,50 | +4,0% |
| 2026-05 | R$ 201.691,50 | −26,1% |
| 2026-06 | R$ 258.911,00 | +28,4% |

Abril foi o mês de maior faturamento. Maio registrou a queda mais acentuada do período (−26,1% sobre abril), com recuperação de 28,4% em junho. Janeiro teve a menor receita do período (R$ 162.723,00).

## Faturamento por categoria

| Categoria | Faturamento | Unidades |
|---|---|---|
| Eletrônicos | R$ 1.259.961,00 | 497 |
| Móveis | R$ 77.047,50 | 92 |
| Acessórios | R$ 46.503,00 | 193 |
| Componentes | R$ 12.272,00 | 25 |

Eletrônicos concentra ~90% do faturamento total, um ponto de atenção para dependência de categoria. Como a base é simulada, essa concentração reflete os pesos de produto usados na geração dos dados (`scripts/gerar_dados.py`), e não um comportamento de mercado.

## Top 5 produtos

| Produto | Faturamento |
|---|---|
| Notebook Pro 14 | R$ 768.390,00 |
| Smartphone X | R$ 355.250,00 |
| Monitor 24 | R$ 123.145,00 |
| Cadeira Office | R$ 49.162,50 |
| Mesa Compacta | R$ 27.885,00 |

## Faturamento por região

| Região | Faturamento | Pedidos |
|---|---|---|
| Sudeste | R$ 625.574,00 | 168 |
| Sul | R$ 284.762,50 | 78 |
| Nordeste | R$ 248.493,50 | 68 |
| Centro-Oeste | R$ 159.467,50 | 60 |
| Norte | R$ 77.486,00 | 26 |

O Sudeste responde por ~45% do faturamento, com 40% dos clientes cadastrados na região.

## Performance de vendedores

| Vendedor(a) | Faturamento | Pedidos | Ticket médio |
|---|---|---|---|
| Aline Barros | R$ 252.305,00 | 63 | R$ 4.004,84 |
| Andre Luz | R$ 198.320,50 | 58 | R$ 3.419,32 |
| Carlos Mendes | R$ 195.771,50 | 50 | R$ 3.915,43 |
| Rogerio Dias | R$ 190.750,00 | 49 | R$ 3.892,86 |
| Beatriz Rocha | R$ 174.691,00 | 49 | R$ 3.565,12 |
| Priscila Nunes | R$ 163.370,50 | 47 | R$ 3.475,97 |
| Felipe Nogueira | R$ 115.499,00 | 43 | R$ 2.686,02 |
| Camila Teixeira | R$ 105.076,00 | 41 | R$ 2.562,83 |

Aline Barros lidera tanto em faturamento quanto em ticket médio. Numa base real, o próximo passo seria investigar se isso vem do mix de produtos vendidos ou de poucos pedidos de valor alto.

> Observação: a base é simulada e serve para fins educacionais e de portfólio. As conclusões demonstram o método de análise e não representam uma empresa real.
