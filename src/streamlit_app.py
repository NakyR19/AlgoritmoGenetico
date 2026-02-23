"""
main.py - Dashboard Streamlit para o Algoritmo Genético (TSP)

Execute com:  streamlit run main.py
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from src.ga import ga

# configuração da página
st.set_page_config(
    page_title="AG – Caixeiro Viajante",
    page_icon="🧬",
    layout="wide",
)

# funções auxiliares

def gerar_cidades(n, seed=None):
    """Gera coordenadas aleatórias (x, y) para `n` cidades."""
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 100, size=(n, 2))


def matriz_distancias(coords):
    """Retorna a matriz simétrica de distâncias euclidianas."""
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def fig_rota(coords, rota, dist_total):
    """Retorna um plotly Figure com a rota do caixeiro."""
    rota_fechada = list(rota) + [rota[0]]
    xs = coords[rota_fechada, 0]
    ys = coords[rota_fechada, 1]

    fig = go.Figure()

    # linhas da rota
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines",
        line=dict(color="#6366f1", width=2),
        showlegend=False,
    ))

    # todas as cidades
    fig.add_trace(go.Scatter(
        x=coords[:, 0], y=coords[:, 1],
        mode="markers+text",
        marker=dict(size=10, color="#6366f1"),
        text=[str(i) for i in range(len(coords))],
        textposition="top center",
        textfont=dict(size=10, color="#e2e8f0"),
        name="Cidades",
    ))

    # cidade de partida
    fig.add_trace(go.Scatter(
        x=[coords[rota[0], 0]], y=[coords[rota[0], 1]],
        mode="markers",
        marker=dict(size=16, color="#f43f5e", symbol="diamond"),
        name="Partida",
    ))

    fig.update_layout(
        title=dict(text=f"Melhor rota  ·  distância = {dist_total:.2f}", font=dict(size=16)),
        xaxis_title="X", yaxis_title="Y",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", y=-0.12),
    )
    return fig


def fig_convergencia(historico):
    """Retorna um plotly Figure com a curva de convergência."""
    geracoes = list(range(len(historico)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=geracoes, y=historico,
        mode="lines",
        line=dict(color="#f97316", width=2),
        fill="tozeroy",
        fillcolor="rgba(249,115,22,0.12)",
        name="Melhor distância",
    ))
    fig.update_layout(
        title=dict(text="Convergência do Algoritmo Genético", font=dict(size=16)),
        xaxis_title="Geração",
        yaxis_title="Distância",
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def fig_heatmap(mat):
    """Retorna um plotly Figure com o heatmap da matriz de distâncias."""
    fig = go.Figure(data=go.Heatmap(
        z=mat,
        colorscale="Viridis",
        colorbar=dict(title="Dist"),
    ))
    fig.update_layout(
        title=dict(text="Matriz de Distâncias", font=dict(size=16)),
        xaxis_title="Cidade",
        yaxis_title="Cidade",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def fig_rota_mini(coords, rota, gen, dist):
    """Versão compacta do gráfico de rota para a visão de evolução."""
    rota_fechada = list(rota) + [rota[0]]
    xs = coords[rota_fechada, 0]
    ys = coords[rota_fechada, 1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines+markers",
        line=dict(color="#6366f1", width=1.5),
        marker=dict(size=5, color="#6366f1"),
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=[coords[rota[0], 0]], y=[coords[rota[0], 1]],
        mode="markers",
        marker=dict(size=10, color="#f43f5e", symbol="diamond"),
        showlegend=False,
    ))
    fig.update_layout(
        title=dict(text=f"Geração {gen}  ·  dist = {dist:.2f}", font=dict(size=13)),
        template="plotly_dark",
        height=350,
        margin=dict(l=25, r=10, t=40, b=25),
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
    )
    return fig


# sidebar - parâmetros
with st.sidebar:
    st.markdown("## ⚙️ Parâmetros do AG")

    num_cidades = st.slider("Número de cidades", 5, 50, 20)
    tam_pop     = st.slider("Tamanho da população", 20, 500, 150, step=10)
    prob_mut    = st.slider("Probabilidade de mutação", 0.0, 1.0, 0.05, step=0.01)
    num_ger     = st.slider("Número de gerações", 50, 2000, 500, step=50)
    elite       = st.slider("Tamanho da elite", 1, 20, 4)
    seed        = st.number_input("Seed (0 = aleatório)", min_value=0, value=42, step=1)

    rodar = st.button("Executar", use_container_width=True)

# header
st.markdown(
    """
    <h1 style='text-align:center; color:#a5b4fc;'>
        🧬 Algoritmo Genético — Caixeiro Viajante
    </h1>
    <p style='text-align:center; color:#94a3b8; margin-bottom:2rem;'>
        Resolução do <b>TSP</b> utilizando seleção proporcional, cruzamento OX1 e mutação por inversão.
    </p>
    """,
    unsafe_allow_html=True,
)

# execução
if rodar:
    seed_val = None if seed == 0 else int(seed)
    coords = gerar_cidades(num_cidades, seed=seed_val)
    dist_mat = matriz_distancias(coords)

    # calcula as 5 gerações para snapshot: primeira, 3 intermediárias, última
    snap_indices = [0]
    for i in range(1, 4):
        snap_indices.append(round(i * (num_ger - 1) / 4))
    snap_indices.append(num_ger - 1)

    with st.spinner("Executando o algoritmo genético…"):
        algoritmo = ga(
            matriz_distancias=dist_mat,
            tam_pop=tam_pop,
            prob_mutacao=prob_mut,
            num_geracoes=num_ger,
            elite_size=elite,
        )
        melhor_rota, melhor_dist, historico, snapshots = algoritmo.run(
            snapshots_em=snap_indices
        )

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Distância final", f"{melhor_dist:.2f}")
    col2.metric("Cidades", num_cidades)
    col3.metric("Gerações", num_ger)
    col4.metric("Melhoria",
                f"{((historico[0] - melhor_dist) / historico[0] * 100):.1f} %")

    st.divider()

    # gráficos
    tab_rota, tab_evo, tab_conv, tab_heat, tab_dados = st.tabs(
        ["Rota", "Evolução", "Convergência", "Heatmap", "Dados"]
    )

    with tab_rota:
        st.plotly_chart(fig_rota(coords, melhor_rota, melhor_dist),
                        use_container_width=True)

    with tab_evo:
        st.markdown("##### Evolução da melhor rota ao longo das gerações")
        # ordena as gerações capturadas
        gens_ordenadas = sorted(snapshots.keys())
        cols = st.columns(len(gens_ordenadas))
        for col, g in zip(cols, gens_ordenadas):
            rota_g, dist_g = snapshots[g]
            with col:
                st.plotly_chart(fig_rota_mini(coords, rota_g, g + 1, dist_g),
                                use_container_width=True)

    with tab_conv:
        st.plotly_chart(fig_convergencia(historico),
                        use_container_width=True)

    with tab_heat:
        st.plotly_chart(fig_heatmap(dist_mat),
                        use_container_width=True)

    with tab_dados:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Coordenadas das cidades")
            import pandas as pd
            df_coords = pd.DataFrame(coords, columns=["X", "Y"])
            df_coords.index.name = "Cidade"
            st.dataframe(df_coords.style.format("{:.2f}"), use_container_width=True)

        with col_b:
            st.markdown("### Melhor rota (ordem de visita)")
            rota_fechada = melhor_rota + [melhor_rota[0]]
            trechos = []
            for k in range(len(rota_fechada) - 1):
                o, d = rota_fechada[k], rota_fechada[k + 1]
                dist_trecho = np.linalg.norm(coords[o] - coords[d])
                trechos.append({"Origem": o, "Destino": d, "Distância": dist_trecho})
            df_trechos = pd.DataFrame(trechos)
            st.dataframe(df_trechos.style.format({"Distância": "{:.2f}"}),
                         use_container_width=True)

else:
    st.info("Ajuste os parâmetros na barra lateral e clique em **Executar** para rodar o algoritmo.")