# Phase 5: Narrativa e Slides - Research

**Researched:** 2026-03-01
**Domain:** Documentacao, comunicacao de resultados e narrativa de apresentacao
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Ferramenta de slides**
- Google Slides (nao PowerPoint, nao Marp)
- Facilita colaboracao e compartilhamento de link para a apresentacao
- Figuras de `reports/figures/` sao inseridas como imagens estaticas nos slides

**Publico-alvo do deck**
- Misto: gestores de negocio + time tecnico
- Estrutura: narrativa principal dos dois atos (acessivel para gestores) + apendice tecnico (metricas detalhadas, metodologia, trade-offs)
- Slides principais = linguagem de negocio + impacto operacional
- Apendice = PR-AUC, curva PR, SHAP beeswarm, parâmetros do modelo

**Relatorio escrito (PRES-06)**
- Dois artefatos: relatorio tecnico completo (5-8 paginas) E README atualizado do projeto
- Relatorio tecnico: `docs/report.md` — metodologia, metricas detalhadas, limitacoes, proximos passos, recomendacoes operacionais em linguagem de negocio
- README: atualizado com secao de resultados e conclusoes — guia de reproducao + achados principais
- Ambos em Markdown (versionaveis no git)

**Documentacao dos notebooks (PRES-02)**
- Headers de secao + docstrings Markdown explicando o "porque" de cada bloco (nao apenas o "o que")
- Exemplo de padrao: celula Markdown antes de cada bloco de codigo explicando a decisao metodologica
- Outputs limpos via nbstripout (ja configurado no .gitattributes da Phase 1)
- Sem paths hardcoded — usar caminhos relativos a raiz do projeto em todos os notebooks
- Abrange: notebooks de data foundation (Phase 2), EDA (Phase 3) e ML (Phase 4)

**Claude's Discretion**
- Template visual dos slides (cores, fontes) — escolher esquema limpo e profissional
- Numero exato de slides por ato — otimizar para apresentacao de ~20 minutos
- Estrutura interna do relatorio tecnico — seguir convencao cientifica (introducao, dados, metodologia, resultados, conclusoes, recomendacoes)
- Quais outputs do notebook manter vs. limpar — manter outputs de metricas finais, limpar outputs intermediarios verbosos

### Deferred Ideas (OUT OF SCOPE)

Nenhuma ideia fora do escopo surgiu — discussao ficou dentro da fronteira da fase.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PRES-01 | Slide deck com narrativa em dois atos (Problema -> Motor de risco -> Acoes/impacto esperado) | Estrutura de slides documentada: Ato 1 (Phase 3 figures) + Ato 2 (Phase 4 metrics/SHAP) + apendice tecnico. Conteudo de cada slide especificado. |
| PRES-02 | Notebooks documentados por area (data foundation, EDA, ML) com outputs limpos no git | Padrao de celula Markdown documentado; nbstripout ja configurado via .gitattributes; checklist de paths hardcoded. |
| PRES-06 | Relatorio escrito com achados tecnicos e recomendacoes operacionais em linguagem de negocio | Estrutura de docs/report.md definida (convencao cientifica); secao README definida; frases-ancora documentadas. |

</phase_requirements>

---

## Summary

Phase 5 e uma fase de comunicacao pura — nenhum codigo de analise novo, nenhuma feature nova de modelo. O trabalho e transformar artefatos existentes (PNGs em `reports/figures/`, `.joblib` em `models/`, metricas em `FASE4-P4-ml-pipeline.ipynb`) em narrativa comunicavel para dois publicos distintos: gestores de negocio (deck de slides) e revisores tecnicos (notebooks auditaveis + relatorio escrito).

A fase tem tres entregaveis distintos: (1) deck Google Slides com narrativa dois atos, (2) notebooks de Phase 2/3/4 documentados e com outputs limpos, e (3) dois documentos Markdown — `docs/report.md` (5-8 paginas tecnico-negocio) e README atualizado. O risco principal nao e tecnico — e de coerencia narrativa: garantir que a historia contada nos slides corresponda exatamente as metricas citadas no relatorio e aos outputs presentes nos notebooks.

A frase-ancora operacional "40% dos pedidos flagrados sao de fato risco real" (precision >= 0.40 no threshold definido na Phase 4) e o fio condutor do Ato 2. Todos os artefatos devem usar essa mesma metrica — slides, relatorio e README — sem divergencia de numeros.

**Primary recommendation:** Executar a documentacao de notebooks primeiro (PRES-02), depois escrever o relatorio tecnico (PRES-06) extraindo metricas dos notebooks documentados, e por ultimo construir o deck (PRES-01) usando os numeros ja revisados no relatorio.

---

## Standard Stack

### Core

| Ferramenta | Versao | Proposito | Por que padrao |
|-----------|--------|-----------|----------------|
| Google Slides | Web (atual) | Deck de apresentacao | Decisao bloqueada; compartilhamento por link |
| Markdown | - | Relatorio e README | Versionavel no git; padrao do projeto (docs/) |
| nbstripout | >=0.7 | Limpar outputs de notebooks no commit | Ja configurado via .gitattributes (Phase 1) |
| Jupyter Notebook | >=1.0 | Ambiente dos notebooks a documentar | Ja no requirements.txt |

### Supporting

| Ferramenta | Versao | Proposito | Quando usar |
|-----------|--------|-----------|-------------|
| Python `pathlib.Path` | stdlib | Caminhos relativos nos notebooks | Substituir qualquer path hardcoded |
| PNG export | - | Imagens de `reports/figures/` | Inserir nos slides e no relatorio |

### Alternatives Considered

| Em vez de | Poderia usar | Tradeoff |
|-----------|-------------|----------|
| Google Slides | Marp (Markdown slides) | Marp e versionavel mas requer toolchain extra e nao foi aprovado pelo usuario |
| Google Slides | PowerPoint | PowerPoint nao aprovado pelo usuario |
| docs/report.md | PDF | PDF nao e versionavel no git; Markdown e preferido para o projeto |

**Instalacao:** Nenhuma dependencia nova — tudo ja esta em requirements.txt.

---

## Architecture Patterns

### Estrutura de arquivos desta fase

```
notebooks/
├── FASE2-P2-data-foundation.ipynb    # documentar headers + porque de cada bloco
├── FASE3-P3-eda.ipynb                # documentar headers + porque de cada bloco
└── FASE4-P4-ml-pipeline.ipynb        # documentar headers + porque de cada bloco

docs/
├── feature_contract.md               # ja existe (Phase 1) — apenas referenciado
├── metrics_agreement.md              # ja existe (Phase 1) — apenas referenciado
├── kickoff.md                        # ja existe (Phase 1) — apenas referenciado
└── report.md                         # NOVO — relatorio tecnico 5-8 paginas

reports/figures/                      # ja existem — apenas consumidos
├── [EDA Phase 3 PNGs]
├── shap_beeswarm.png
└── pr_curve.png

README.md                             # atualizar secao de resultados
```

### Padrao 1: Celula Markdown de contexto antes de cada bloco de codigo

**O que e:** Cada secao de notebook comeca com uma celula Markdown que explica a decisao metodologica (o "porque"), nao apenas o que o codigo faz.

**Quando usar:** Todo bloco de codigo que implementa uma escolha de modelagem, limpeza ou visualizacao nao-trivial.

**Exemplo (notebook ML):**

```markdown
## 3. XGBoost com Balanceamento de Classes

**Por que XGBoost?** O baseline logistico estabeleceu o patamar minimo. XGBoost captura
interacoes nao-lineares entre features (ex.: distancia alta + prazo estimado alto) que
a regressao logistica trata como independentes. Usamos `class_weight='balanced'` em vez
de SMOTE para evitar dados sinteticos em um sprint de 1 semana.

**Decisao de hiperparametros:** Sem GridSearchCV — defaults razoaveis para garantir
entrega no prazo. O ganho marginal de tuning nao justifica o risco de prazo.
```

**Exemplo (notebook EDA):**

```markdown
## 2. Analise de Atraso vs. Nota de Avaliacao

**Por que Mann-Whitney e nao t-test?** As notas (1-5 estrelas) nao seguem distribuicao
normal — sao ordinais e fortemente enviesadas para 5 estrelas. Mann-Whitney e o teste
nao-parametrico correto para comparar medianas entre grupos de tamanhos diferentes sem
assumir normalidade.
```

### Padrao 2: Caminhos relativos com pathlib

**O que e:** Todos os notebooks usam `pathlib.Path` com caminhos relativos a raiz do projeto, nunca paths absolutos hardcoded.

**Quando usar:** Em toda celula que le ou escreve arquivos.

**Exemplo:**

```python
# CORRETO — caminho relativo portavel
from pathlib import Path
ROOT = Path(__file__).parent.parent if "__file__" in dir() else Path.cwd()
# Em notebooks usar:
ROOT = Path.cwd()  # assume execucao da raiz do projeto
gold_path = ROOT / "data" / "gold" / "olist_gold.parquet"
fig_path = ROOT / "reports" / "figures" / "shap_beeswarm.png"

# ERRADO — path hardcoded
gold_path = "C:/Users/Wey/Desktop/Alpha/Projetos/python/data/gold/olist_gold.parquet"
```

**Verificacao:** Procurar por strings contendo `C:/`, `C:\\`, `/home/`, `/Users/` nos notebooks.

### Padrao 3: Estrutura do relatorio tecnico (convencao cientifica)

**O que e:** `docs/report.md` segue estrutura cientifica adaptada para negocio.

**Estrutura recomendada:**

```markdown
# Risco Pre-Entrega em E-commerce: Uma Analise do Dataset Olist

## 1. Contexto e Problema de Negocio
## 2. Dados
## 3. Metodologia
   ### 3.1 Ato 1 — Analise Exploratoria
   ### 3.2 Ato 2 — Modelo de Risco Pre-Entrega
## 4. Resultados
   ### 4.1 Achados do Ato 1 (EDA)
   ### 4.2 Desempenho do Modelo (Ato 2)
## 5. Recomendacoes Operacionais
## 6. Limitacoes e Proximos Passos
## Referencias e Artefatos
```

### Padrao 4: Estrutura do deck Google Slides (dois atos + apendice)

**Cronograma de slides para ~20 minutos:**

```
INTRODUCAO (2 slides)
  01. Titulo + contexto (quem somos, dataset Olist)
  02. Pergunta de negocio: "Como agir antes da entrega ruim acontecer?"

ATO 1 — A DOR: Logistica degrada satisfacao (6-7 slides)
  03. Headline: "Atraso causa insatisfacao — aqui esta a evidencia"
  04. Scatter + boxplot atraso vs nota [reports/figures/EDA Phase 3]
  05. Frete vs nota: o segundo fator mais importante
  06. Mapa geografico: onde estao as avaliacoes ruins por UF [choropleth]
  07. Rotas criticas: heatmap origem x destino com maior concentracao de atrasos
  08. Categorias problematicas: top categorias com mais reviews 1-2 estrelas
  09. Ato 1 — Conclusao: "Sabemos onde e quando o problema acontece"

ATO 2 — A SOLUCAO: Motor de risco pre-entrega (6-7 slides)
  10. Transicao: "Podemos prever ANTES da entrega?"
  11. Abordagem: features pre-entrega, baseline logistico, XGBoost
  12. Curva PR + threshold: baseline vs XGBoost [pr_curve.png]
  13. Resultado operacional: "40% dos pedidos flagrados sao risco real" — X pedidos/semana
  14. SHAP — o que o modelo aprendeu: top features [shap_beeswarm.png]
  15. Vendedores de maior risco: tabela top-20 (acionavel para operacoes)
  16. Ato 2 — Conclusao: "Temos um motor de alerta precoce funcional"

CONCLUSAO E PROXIMOS PASSOS (2 slides)
  17. Recomendacoes operacionais em linguagem de negocio
  18. Proximos passos / roadmap tecnico

APENDICE TECNICO (nao apresentado — disponivel para perguntas)
  A1. PR-AUC detalhado: baseline X.XX vs XGBoost X.XX
  A2. Metodologia completa: divisao treino/test, balanceamento de classes
  A3. SHAP beeswarm completo (versao ampliada)
  A4. Parametros do modelo XGBoost
  A5. Limitacoes e riscos do modelo
```

### Anti-Patterns a Evitar

- **Numeros inconsistentes entre artefatos:** Se o relatorio diz "PR-AUC 0.72" e o slide diz "PR-AUC 0.71", cria duvida em apresentacoes. Extrair sempre do mesmo notebook documentado.
- **Paths hardcoded nos notebooks:** Quebra reproducibilidade em qualquer outra maquina. Usar sempre `pathlib.Path` relativo.
- **Outputs verbosos de treinamento:** Logs de XGBoost iteracao-por-iteracao devem ser limpos — apenas a celula de metricas finais com output visivel.
- **Celulas Markdown que descrevem apenas o "o que":** "Aqui calculamos o PR-AUC" nao agrega valor. "Usamos PR-AUC porque o dataset tem ~15% de classe positiva e accuracy seria enganosa" sim.
- **Apendice tecnico ausente dos slides:** Apresentadores precisam de slides de backup para perguntas tecnicas. Apendice garante que o presenter nao trave se perguntado sobre hiperparametros.

---

## Don't Hand-Roll

| Problema | Nao construir | Usar em vez | Por que |
|----------|--------------|-------------|---------|
| Limpeza de outputs de notebook | Script customizado de limpeza | nbstripout (ja configurado) | Ja integrado ao git via .gitattributes — roda automaticamente no commit |
| Conversao de notebook para PDF/HTML | nbconvert customizado | Nao necessario — revisores abrem .ipynb | Fora do escopo da phase; notebooks sao auditados ao vivo |
| Geracao automatica de slides | python-pptx, reveal.js | Google Slides manual | Decisao bloqueada; qualidade visual manual e superior para apresentacao |
| Template de relatorio | Ferramenta de geracao de docs | Markdown puro em docs/report.md | Mais simples, versionavel, padrao do projeto |

**Key insight:** Esta fase e manual por design — a qualidade narrativa vem da revisao humana, nao de automacao. O unico automatismo e o nbstripout (ja configurado). O trabalho e escrever, revisar e inserir imagens.

---

## Common Pitfalls

### Pitfall 1: Numeros divergentes entre artefatos

**O que vai errado:** O relatorio diz "Recall 0.63", o slide diz "Recall 65%", o notebook mostra "recall: 0.618". Auditores notam divergencias.

**Por que acontece:** Metricas extraidas de memoria ou de drafts intermediarios, nao do notebook documentado final.

**Como evitar:** Ordem de execucao correta — primeiro documentar notebooks (PRES-02), depois escrever relatorio com metricas extraidas do notebook, depois fazer slides com numeros do relatorio. Nunca inverter essa ordem.

**Sinais de alerta:** Qualquer numero no relatorio ou slide que nao pode ser tracado de volta a uma celula especifica do notebook.

### Pitfall 2: Paths hardcoded nos notebooks

**O que vai errado:** `pd.read_parquet("C:/Users/Wey/Desktop/...")` funciona na maquina do autor mas quebra para qualquer outro revisor ou em qualquer outro ambiente.

**Por que acontece:** Desenvolvimento local com caminhos absolutos copiados do explorador de arquivos.

**Como evitar:** Padrao `Path.cwd() / "data" / "gold" / "olist_gold.parquet"` em toda celula de I/O. Verificar com grep antes de commitar.

**Sinais de alerta:** Qualquer string contendo `C:/`, `C:\\`, `/home/`, `/Users/`, ou `\\` (backslash duplo Windows).

### Pitfall 3: Outputs intermediarios verbosos deixados no notebook

**O que vai errado:** Notebook com 200 linhas de log de treinamento XGBoost, warnings de deprecacao e tabelas intermediarias. Revisor nao consegue encontrar os resultados finais.

**Por que acontece:** Outputs gerados durante desenvolvimento nao foram curados antes de documentar.

**Como evitar:** Estrategia de outputs: manter apenas metricas finais (classification report, PR-AUC, tabela de vendedores), limpar tudo intermediario. Nbstripout remove TODOS os outputs no commit — portanto outputs finais importantes devem ser mantidos no texto Markdown de celulas, nao apenas como outputs de celulas.

**Sinais de alerta:** Celula com mais de 50 linhas de output de treinamento visivel.

### Pitfall 4: Deck sem apendice tecnico

**O que vai errado:** Apresentador e perguntado sobre PR-AUC, hiperparametros ou metodologia e nao tem slide para mostrar. Perde credibilidade.

**Por que acontece:** Foco excessivo nos slides principais para gestores, apendice esquecido.

**Como evitar:** Criar apendice de pelo menos 5 slides (ver estrutura no Padrao 4 acima) mesmo que nunca apresentado. Inserir apos o slide de proximos passos.

**Sinais de alerta:** Deck sem secao de Apendice identificada.

### Pitfall 5: Celulas Markdown sem decisao metodologica

**O que vai errado:** Notebook tem headers mas celulas Markdown apenas descrevem o codigo: "# Treinamento do XGBoost" sem explicar por que XGBoost, por que esses parametros, por que esse threshold.

**Por que acontece:** Documentacao escrita como comentario de codigo, nao como narrativa de decisoes.

**Como evitar:** Para cada bloco de codigo nao-trivial, a celula Markdown deve responder: "Por que esta abordagem foi escolhida?" e "Quais alternativas foram descartadas?"

---

## Code Examples

### Caminho relativo portavel em notebook

```python
# Celula 1 de qualquer notebook — sempre na primeira celula de imports
from pathlib import Path

# Notebooks sao executados a partir da raiz do projeto.
# Se executar de dentro de notebooks/, usar: ROOT = Path.cwd().parent
ROOT = Path.cwd()

# Verificacao: deve mostrar a raiz do projeto
print(f"ROOT: {ROOT}")
assert (ROOT / "data" / "gold").exists(), f"Execute o notebook a partir da raiz do projeto. ROOT atual: {ROOT}"
```

### Exemplo de celula Markdown de decisao metodologica

```markdown
## 5. Definicao do Threshold de Decisao

**Criterio primario:** Precision >= 0.40 no threshold escolhido.
**Criterio secundario:** Recall >= 0.60 no mesmo ponto.

**Por que Precision como criterio primario?** O custo operacional de intervir em um pedido
(contato com vendedor, monitoramento extra) e nao trivial. Um modelo que flaga 90% dos
pedidos como "risco" e inutil — equipe operacional nao tem capacidade para agir em todos.
Com Precision >= 0.40, garantimos que 40% dos pedidos flagrados sao de fato risco real
— a frase-ancora operacional desta analise.

**Por que Recall >= 0.60 como secundario?** Nao queremos um modelo que flaga apenas os
casos mais obvios. Recall 0.60 significa capturar 60% dos pedidos que iriam gerar
avaliacao ruim — suficiente para impacto operacional mensuravel.
```

### Estrutura de secao README (secao Resultados)

```markdown
## Resultados

### Modelo de Risco Pre-Entrega

| Metrica | Baseline (LogReg) | XGBoost |
|---------|------------------|---------|
| PR-AUC  | X.XX             | X.XX    |
| Recall  | X.XX             | X.XX    |
| Precision no threshold | - | 0.40+ |

**Frase-ancora operacional:** "40% dos pedidos flagrados pelo modelo sao de fato
pedidos de alto risco de avaliacao ruim — permitindo intervencao preventiva antes da entrega."

**Impacto estimado:** ~X pedidos flagrados por semana com o threshold escolhido.

Para reproducir os resultados: execute os notebooks na ordem
`FASE2 -> FASE3 -> FASE4` a partir da raiz do projeto.
```

### Verificacao de paths hardcoded nos notebooks

```bash
# Executar a partir da raiz do projeto antes de commitar
grep -rn "C:\\\\" notebooks/ || echo "OK: sem paths Windows hardcoded"
grep -rn "/home/" notebooks/ || echo "OK: sem paths Unix hardcoded"
grep -rn "/Users/" notebooks/ || echo "OK: sem paths macOS hardcoded"
```

---

## State of the Art

| Abordagem antiga | Abordagem atual | Quando mudou | Impacto |
|-----------------|----------------|-------------|---------|
| Outputs de notebook no git (commits pesados) | nbstripout remove outputs antes do commit | Padrao moderno (>2018) | Commits leves, diffs legiveis, sem conflitos de merge em notebooks |
| Paths absolutos hardcoded em notebooks | pathlib.Path com caminhos relativos | Padrao moderno Python 3.4+ | Notebooks reproduziveis em qualquer maquina |
| Relatorio em PDF gerado por nbconvert | Markdown versionavel em docs/ | Padrao de projetos ML modernos | Diffable no git, editavel sem ferramentas especiais |

**Deprecated/outdated:**
- `os.path.join` para caminhos: substituido por `pathlib.Path` (mais legivel, orientado a objeto)
- Outputs hardcoded em notebooks versionados: nbstripout e o padrao correto

---

## Open Questions

1. **Metricas exatas do modelo (PR-AUC, Recall, pedidos flagrados/semana)**
   - O que sabemos: threshold escolhido com Precision >= 0.40 e Recall >= 0.60 (decisao Phase 4)
   - O que esta incerto: os valores numericos exatos — dependem da execucao da Phase 4
   - Recomendacao: o planner deve incluir uma task de "extrair metricas do notebook FASE4-P4-ml-pipeline.ipynb" como primeiro passo antes de escrever relatorio e slides. Todos os numeros nos artefatos desta fase devem vir desta extracao.

2. **Nomes exatos dos arquivos PNG em reports/figures/**
   - O que sabemos: `shap_beeswarm.png` e `pr_curve.png` (definidos em Phase 4 CONTEXT.md)
   - O que esta incerto: nomes das figuras EDA da Phase 3 — dependem de como o notebook exportou
   - Recomendacao: incluir task de inventario de `reports/figures/` antes de construir slides.

3. **Nomes exatos dos notebooks das Phases 2, 3 e 4**
   - O que sabemos: convencao e `FASE{N}-P{N}-descricao.ipynb`; notebook ML e `FASE4-P4-ml-pipeline.ipynb`
   - O que esta incerto: nomes exatos dos notebooks de Phase 2 e Phase 3 (dependem da execucao)
   - Recomendacao: task de inventario de `notebooks/` antes de documentar.

---

## Sources

### Primary (HIGH confidence)

- `05-CONTEXT.md` — Decisoes bloqueadas do usuario para esta phase (ferramenta, publico, artefatos)
- `04-CONTEXT.md` — Metricas e threshold da Phase 4; frase-ancora "40% dos pedidos flagrados"
- `01-01-PLAN.md` — Estrutura de pastas e convencoes do repositorio
- `01-02-PLAN.md` — Spec completa de PRE_DELIVERY_FEATURES e convencao src/features.py
- `REQUIREMENTS.md` — Definicao oficial de PRES-01, PRES-02, PRES-06
- `ROADMAP.md` — Success criteria de Phase 5

### Secondary (MEDIUM confidence)

- Convencao de nomes de notebooks `FASE{N}-P{N}-descricao.ipynb` — definida em Phase 1 CONTEXT.md, aplicada aqui
- Padrao nbstripout em modo git filter (nao hook) — documentado em 01-01-PLAN.md

### Tertiary (LOW confidence)

- Nenhum finding de baixa confianca — todos os requisitos desta fase sao de documentacao e comunicacao, sem dependencias de bibliotecas externas novas.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Google Slides (decisao bloqueada), Markdown, nbstripout (ja no projeto)
- Architecture: HIGH — estrutura de slides e relatorio derivada diretamente do CONTEXT.md e dos artefatos existentes das phases anteriores
- Pitfalls: HIGH — problemas classicos de reproducibilidade de notebooks e coerencia de narrativa, bem documentados na literatura e nas decisoes do projeto

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (fase de documentacao/comunicacao — nao depende de versoes de bibliotecas)
