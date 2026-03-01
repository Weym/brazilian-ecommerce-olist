# Decisão: Métrica do Heatmap de Rotas Logísticas (EDA-05)

**Fase:** 03 — EDA Ato 1
**Data:** 2026-03-01
**Status:** ✅ Decidido — Opção A implementada

---

## Contexto

O heatmap de rotas (vendedor → cliente por UF) precisa de uma métrica para colorir as células.
Duas opções foram avaliadas. Os dados relevantes para a decisão:

- **92% das entregas chegam antes do prazo** (mediana: -13.7 dias)
- Apenas **6 de 355 células** do pivot têm atraso positivo real (> 0 dias)
- Correlação entre atraso médio e `bad_review_rate` por corredor: **r = 0.39** (moderada)
- Os corredores com maior insatisfação real (ex: PR→CE 28.6%, SP→AL 24.1%) chegam *antes* do prazo — portanto "atraso" não captura o problema diretamente

---

## Opção A — `bad_review_rate` por corredor ✅ Escolhida

Colorir as células pela taxa de avaliações ruins (1–2 ★) em cada corredor origem → destino.

**Pros:**
- Métrica diretamente ligada ao objetivo do projeto (prever avaliações ruins)
- Intuitivo para qualquer audiência: vermelho = clientes insatisfeitos nesse corredor
- Consistente com o choropleth por UF (EDA-03), que também usa taxa de bad_review
- Não exige contexto extra — a cor reflete um problema real, não relativo

**Contras:**
- Perde a dimensão logística explícita (não mostra *por que* o corredor é ruim)
- Pode ter viés de volume: corredor com 30 pedidos e 10 ruins (33%) aparece mais vermelho que SP→RJ com 20% e 8k pedidos — mitigável com filtro de volume mínimo

**Quando usar:** slides, apresentações, comunicação para stakeholders não técnicos.

---

## Opção B — `dias_atraso` centralizado na mediana nacional

Colorir pelas células por atraso médio, mas com `center` na mediana nacional (-13.7 dias) em vez de 0.
Vermelho = corredor com menos folga que a média; verde = corredor mais antecipado que a média.

**Pros:**
- Mantém a dimensão logística explícita no visual
- Mais honesto que `center=0`: vermelho significa "pior que a média", não "atrasado em absoluto"
- Conecta diretamente com os gráficos EDA-01 e EDA-02 (atraso como variável explicativa)

**Contras:**
- Exige explicação no título/legenda — não é imediato sem contexto
- A correlação atraso→bad_review por corredor é r = 0.39: o visual sugere causalidade que o dado sustenta apenas parcialmente
- Todos os corredores chegam cedo; o espectro de cor representa diferença relativa, não magnitude absoluta de problema

**Quando usar:** análise técnica interna, EDA aprofundada, explicar mecanismo logístico para o time de dados.

---

## Por que Opção A vence no contexto deste projeto

O heatmap de rotas serve ao **Ato 1 da narrativa**: provar que logística degrada satisfação.
A audiência final são stakeholders que precisam de uma conclusão imediata e acionável.

`bad_review_rate` entrega essa conclusão diretamente. `dias_atraso` exige um passo intermediário
("esse corredor chega menos cedo → isso correlaciona com mais insatisfação") que aumenta a carga
cognitiva sem acrescentar clareza para quem decide.

---

## Referência: Abordagem para EDA Técnica Aprofundada

Para uma análise mais granular (ex.: relatório interno, Phase 4 feature engineering), o heatmap ideal combinaria as duas dimensões:

```python
# Pivot duplo: atraso médio como cor, bad_review_rate como anotação
pivot_atraso = route_df.pivot_table(values="dias_atraso", index="seller_state",
                                     columns="customer_state", aggfunc="mean")
pivot_bad    = route_df.pivot_table(values="bad_review",   index="seller_state",
                                     columns="customer_state", aggfunc="mean")

# Heatmap com cor = atraso (center na mediana), anotação = bad_rate em %
annot_labels = pivot_bad.applymap(lambda x: f"{x:.0%}" if pd.notna(x) else "")

sns.heatmap(pivot_atraso, center=-13.7, cmap="RdYlGn",
            annot=annot_labels, fmt="", annot_kws={"size": 7})
```

Isso permite ler: "esse corredor chega X dias antes da média **e** tem Y% de clientes insatisfeitos" —
útil para identificar corredores onde o atraso *não* explica a insatisfação (outros fatores: frete, produto, atendimento).

---

## Dados de suporte

| Corredor | bad_review_rate | dias_atraso médio | volume |
|----------|----------------|-------------------|--------|
| PR → CE  | 28.6%          | -9.3 dias         | 63     |
| SP → AL  | 24.1%          | -8.0 dias         | 253    |
| RJ → CE  | 24.1%          | -6.4 dias         | 54     |
| SP → MA  | 22.2%          | -9.3 dias         | 486    |
| SP → RJ  | 20.2%          | -13.1 dias        | 8.066  |
| PR → RJ  | 20.0%          | —                 | 950    |
