# Ownership de Notebooks — Sprint Olist

## Convencao de Nomes

`FASE{N}-P{N}-descricao.ipynb`

- `FASE{N}`: Numero da fase (2, 3, 4...)
- `P{N}`: Numero da pessoa (P1, P2, P3...)
- `descricao`: nome descritivo em kebab-case

Exemplos validos:
- FASE2-P1-data-foundation.ipynb
- FASE3-P2-geo-analysis.ipynb
- FASE3-P3-eda.ipynb
- FASE4-P4-ml-pipeline.ipynb

## Mapa de Ownership

| Pessoa | Area | Notebook(s) | Fase |
|--------|------|-------------|------|
| P1 — Data Lead | Data Foundation | FASE2-P1-data-foundation.ipynb | 2 |
| P2 — Geo/Logistica | Analise Geografica | FASE3-P2-geo-analysis.ipynb | 3 |
| P3 — EDA & Metricas | EDA | FASE3-P3-eda.ipynb | 3 |
| P4 — ML Lead | ML Pipeline | FASE4-P4-ml-pipeline.ipynb | 4 |
| P5 — NLP/Reviews | Reviews NLP | FASE3-P5-nlp-reviews.ipynb (opcional) | 3 |
| P6 — Storytelling | Apresentacao | Coordena deck em docs/ e app/ | 5-6 |

## Regras de Git para Notebooks

1. **Nunca commitar outputs** — rodar `nbstripout --install --attributes .gitattributes` uma vez apos clonar
2. **Verificar antes do commit**: `nbstripout --status` deve mostrar filtro ativo
3. **Sem paths hardcoded** — usar sempre `pathlib.Path` relativo ao `PROJECT_ROOT`
4. **Cada pessoa so edita seus proprios notebooks** — conflitos em .ipynb sao muito dificeis de resolver
5. **Nao renomear notebooks apos criados** — o nome e o owner

## Como Verificar que nbstripout Esta Funcionando

```bash
# Instalar (uma vez por maquina, apos clonar)
pip install nbstripout
nbstripout --install --attributes .gitattributes

# Verificar
nbstripout --status
# Deve mostrar: nbstripout is installed in repository ...
```

Se `nbstripout --status` mostrar "not installed", rodar o install novamente.

## Sinal de Alerta

Se `git diff` em um arquivo .ipynb mostrar linhas como `"output_type": "display_data"`,
os outputs NAO foram removidos. Verificar nbstripout e rodar `nbstripout <arquivo.ipynb>` manualmente antes do commit.

---
*Criado na Phase 1 (Kickoff). Referencia: README.md (setup) | docs/feature_contract.md (features)*
