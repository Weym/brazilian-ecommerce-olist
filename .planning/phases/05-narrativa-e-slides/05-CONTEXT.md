# Phase 5: Narrativa e Slides - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Camada de comunicação dos resultados das Phases 3 e 4: deck de apresentação com dois atos, notebooks documentados e reproduzíveis, e relatório escrito. Nenhum código de análise novo — esta fase transforma artefatos existentes (figuras, métricas, .joblib) em narrativa comunicável para gestores e técnicos.

</domain>

<decisions>
## Implementation Decisions

### Ferramenta de slides
- Google Slides (não PowerPoint, não Marp)
- Facilita colaboração e compartilhamento de link para a apresentação
- Figuras de `reports/figures/` são inseridas como imagens estáticas nos slides

### Público-alvo do deck
- Misto: gestores de negócio + time técnico
- Estrutura: narrativa principal dos dois atos (acessível para gestores) + apêndice técnico (métricas detalhadas, metodologia, trade-offs)
- Slides principais = linguagem de negócio + impacto operacional
- Apêndice = PR-AUC, curva PR, SHAP beeswarm, parâmetros do modelo

### Relatório escrito (PRES-06)
- **Dois artefatos:** relatório técnico completo (5-8 páginas) **e** README atualizado do projeto
- Relatório técnico: `docs/report.md` — metodologia, métricas detalhadas, limitações, próximos passos, recomendações operacionais em linguagem de negócio
- README: atualizado com seção de resultados e conclusões — guia de reprodução + achados principais
- Ambos em Markdown (versionáveis no git)

### Documentação dos notebooks (PRES-02)
- Headers de seção + docstrings Markdown explicando o **"porquê"** de cada bloco (não apenas o "o quê")
- Exemplo de padrão: célula Markdown antes de cada bloco de código explicando a decisão metodológica
- Outputs limpos via nbstripout (já configurado no .gitattributes da Phase 1)
- Sem paths hardcoded — usar caminhos relativos à raiz do projeto em todos os notebooks
- Abrange: notebooks de data foundation (Phase 2), EDA (Phase 3) e ML (Phase 4)

### Claude's Discretion
- Template visual dos slides (cores, fontes) — escolher esquema limpo e profissional
- Número exato de slides por ato — otimizar para apresentação de ~20 minutos
- Estrutura interna do relatório técnico — seguir convenção científica (introdução, dados, metodologia, resultados, conclusões, recomendações)
- Quais outputs do notebook manter vs. limpar — manter outputs de métricas finais, limpar outputs intermediários verbosos

</decisions>

<specifics>
## Specific Ideas

- Ato 1 do deck deve usar os gráficos de `reports/figures/` (Phase 3): scatter atraso vs nota, boxplot, choropleth UF, heatmap rotas
- Ato 2 do deck deve usar: `shap_beeswarm.png`, `pr_curve.png` (Phase 4), tabela de vendedores top-20
- O relatório técnico deve incluir a frase-âncora operacional definida no CONTEXT.md da Phase 4: "40% dos pedidos flagrados são de fato risco real"
- README deve ter seção "Resultados" com as métricas finais do modelo (PR-AUC baseline vs XGBoost) sem precisar abrir notebooks

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `reports/figures/`: figuras PNG prontas da Phase 3 (EDA) e Phase 4 (SHAP, curva PR) — inserir diretamente nos slides
- `models/baseline_logreg.joblib` + `models/final_pipeline.joblib`: artefatos ML da Phase 4 — métricas citadas no relatório
- `docs/feature_contract.md` + `docs/metrics_agreement.md` + `docs/kickoff.md`: documentação da Phase 1 — referenciada no relatório técnico como base metodológica
- `.gitattributes`: nbstripout já configurado — notebooks são limpos automaticamente no commit

### Established Patterns
- Todos os documentos em Markdown (`.md`) em `docs/` — manter padrão
- Caminhos relativos à raiz: `data/gold/olist_gold.parquet`, `models/final_pipeline.joblib`, etc.
- Convenção de nomes de notebooks: `FASE{N}-P{N}-descricao.ipynb`

### Integration Points
- Figuras de `reports/figures/` → inserir nos slides do Google Slides e no relatório técnico
- Métricas do notebook ML (`FASE4-P4-ml-pipeline.ipynb`) → citadas em `docs/report.md` e no README
- `docs/report.md` → Phase 6 não consome diretamente, mas o README atualizado serve de entrada para qualquer revisor

</code_context>

<deferred>
## Deferred Ideas

- Nenhuma ideia fora do escopo surgiu — discussão ficou dentro da fronteira da fase

</deferred>

---

*Phase: 05-narrativa-e-slides*
*Context gathered: 2026-03-01*
