import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.loaders import list_eda_figures
from utils.ui import page_header

page_header("Painel de EDA", icon="📊")

st.markdown(
    "Gráficos exportados da Phase 3 que provam o impacto logístico nas avaliações. "
    "Use o seletor abaixo para navegar entre as análises."
)

# Carregar lista de figuras via loader (cacheado em loaders.py)
figures = list_eda_figures()

if not figures:
    st.warning(
        "Nenhuma figura encontrada em reports/figures/. "
        "Execute a Phase 3 (EDA — Ato 1) para gerar os graficos."
    )
    st.info(
        "Figuras esperadas: boxplot atraso vs nota, scatter frete vs nota, "
        "choropleth UF, heatmap rotas origem-destino."
    )
    st.stop()

# Criar labels legiveis a partir do stem do arquivo
def make_label(path: Path) -> str:
    """Converte nome de arquivo em label humanizado para o selectbox."""
    stem = path.stem
    # Remover prefixos numericos tipo "01_", "02_"
    if stem[:3].replace("_", "").isdigit():
        stem = stem[3:]
    
    label = stem.replace("_", " ").replace("-", " ").title()
    
    # Traducoes pontuais para o menu de leitura
    label = label.replace("Bad Reviews", "Notas Baixas")
    label = label.replace("Bad Review", "Nota Baixa")
    label = label.replace("Uf", "UF")
    label = label.replace("Eda", "EDA")
    label = label.replace("Ratio", "Relativo")
    label = label.replace("Freight", "Frete")
    label = label.replace("Delay", "Atraso")
    label = label.replace("Orders", "Pedidos")
    
    return label

fig_labels = [make_label(f) for f in figures]
fig_map = dict(zip(fig_labels, figures))

# Selectbox de navegacao
col_select, col_info = st.columns([3, 1])
with col_select:
    selected_label = st.selectbox(
        "Selecione o Gráfico",
        options=fig_labels,
        help=f"{len(figures)} gráficos disponíveis",
    )
with col_info:
    st.metric("Gráficos Disponíveis", len(figures))

selected_path = fig_map[selected_label]

# Exibir figura selecionada
st.subheader(selected_label)
st.image(str(selected_path), use_container_width=True)

# Contexto narrativo por grafico
CONTEXT_MAP = {
    # Mapeamento parcial — adicionar conforme Phase 3 define nomes
    "atraso": "Dias de atraso vs nota de avaliacao: atrasos acima de 5 dias correlacionam fortemente com avaliacoes 1-2 estrelas.",
    "frete": "Frete alto relativo ao valor do pedido aumenta insatisfacao — especialmente em categorias de baixo ticket.",
    "choropleth": "Concentracao geografica de avaliacoes ruins por UF — Norte e Nordeste apresentam maiores taxas.",
    "heatmap": "Rotas com maior concentracao de atrasos: pares de UF origem-destino mais criticos.",
    "rota": "Corredores logisticos criticos — pares origem-destino com maior risco de atraso.",
}

# Buscar contexto relevante pelo nome do arquivo
label_lower = selected_label.lower()
context_text = None
for keyword, text in CONTEXT_MAP.items():
    if keyword in label_lower:
        context_text = text
        break

if context_text:
    st.caption(f"Interpretação: {context_text}")

# Navegacao rapida com botoes prev/next
st.divider()
col_prev, col_idx, col_next = st.columns([1, 2, 1])
current_idx = fig_labels.index(selected_label)

with col_prev:
    if current_idx > 0:
        if st.button("← Anterior", use_container_width=True):
            st.session_state["eda_selected"] = fig_labels[current_idx - 1]
            st.rerun()
with col_idx:
    st.caption(f"Gráfico {current_idx + 1} de {len(figures)}")
with col_next:
    if current_idx < len(figures) - 1:
        if st.button("Próximo →", use_container_width=True):
            st.session_state["eda_selected"] = fig_labels[current_idx + 1]
            st.rerun()
