import os
import io
import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from PIL import Image

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "olist_order_items_dataset.csv")

st.set_page_config(
    page_title="E-commerce Analytics — Olist",
    layout="wide",
    page_icon="🛒"
)

# ── DADOS ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["price"]               = pd.to_numeric(df["price"], errors="coerce")
    df["freight_value"]       = pd.to_numeric(df["freight_value"], errors="coerce")
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["year_month"]          = df["shipping_limit_date"].dt.to_period("M").astype(str)
    df["gmv"]                 = df["price"].fillna(0) + df["freight_value"].fillna(0)
    return df

df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.title("🛒 Olist Analytics")
st.sidebar.caption("E-commerce Order Items Dataset")
aba = st.sidebar.radio(
    "Navegação",
    ["Visão Geral", "Análise por Seller", "Similaridade de Produtos", "Gerador de Apresentação"]
)

# ═════════════════════════════════════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ═════════════════════════════════════════════════════════════════════════════
if aba == "Visão Geral":
    st.title("Visão Geral — Olist E-commerce")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Itens",     f"{len(df):,}")
    col2.metric("Receita Total (R$)", f"{df['price'].sum():,.2f}")
    col3.metric("Sellers Únicos",     f"{df['seller_id'].nunique():,}")
    col4.metric("Produtos Únicos",    f"{df['product_id'].nunique():,}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Evolução mensal de vendas")
        serie = df.groupby("year_month", as_index=False)["price"].sum()
        fig = px.line(
            serie, x="year_month", y="price", markers=True,
            labels={"price": "Receita (R$)", "year_month": "Mês"}
        )
        fig.update_layout(margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Distribuição de preços")
        p99 = df["price"].quantile(0.99)
        fig = px.histogram(
            df[df["price"] < p99], x="price", nbins=60,
            labels={"price": "Preço (R$)", "count": "Frequência"}
        )
        fig.update_layout(margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Top 10 Sellers por Receita")
        top_sellers = (
            df.groupby("seller_id", as_index=False)["price"]
            .sum()
            .sort_values("price", ascending=False)
            .head(10)
        )
        top_sellers["seller_short"] = top_sellers["seller_id"].str[:10] + "…"
        fig = px.bar(
            top_sellers, x="seller_short", y="price", color="price",
            color_continuous_scale="Blues",
            labels={"price": "Receita (R$)", "seller_short": "Seller"}
        )
        fig.update_layout(margin=dict(t=10), showlegend=False,
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.subheader("Preço vs Frete (amostra 2 000 itens)")
        p99_frete = df["freight_value"].quantile(0.99)
        sample = (
            df[(df["price"] < p99) & (df["freight_value"] < p99_frete)]
            .sample(min(2000, len(df)), random_state=42)
        )
        fig = px.scatter(
            sample, x="price", y="freight_value", opacity=0.35,
            labels={"price": "Preço (R$)", "freight_value": "Frete (R$)"},
            trendline="ols"
        )
        fig.update_layout(margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# ABA 2 — ANÁLISE POR SELLER
# ═════════════════════════════════════════════════════════════════════════════
elif aba == "Análise por Seller":
    st.title("Análise por Seller")

    seller_list = sorted(df["seller_id"].dropna().unique().tolist())
    seller_sel  = st.sidebar.selectbox("Seller ID", seller_list)
    periodos    = sorted(df["year_month"].dropna().unique().tolist())
    periodos_sel = st.sidebar.multiselect("Período", periodos, default=periodos)

    df_sel = df[
        (df["seller_id"] == seller_sel) &
        (df["year_month"].isin(periodos_sel))
    ].copy()

    avg_freight = df_sel["freight_value"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Total (R$)", f"{df_sel['price'].sum():,.2f}")
    col2.metric("Frete Médio (R$)",   f"{avg_freight:.2f}" if len(df_sel) > 0 else "—")
    col3.metric("Pedidos",            f"{df_sel['order_id'].nunique():,}")
    col4.metric("Itens",              f"{len(df_sel):,}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Evolução temporal do seller")
        serie = df_sel.groupby("year_month", as_index=False)["price"].sum()
        if not serie.empty:
            fig = px.line(
                serie, x="year_month", y="price", markers=True,
                labels={"price": "Receita (R$)", "year_month": "Mês"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Sem dados para o período selecionado.")

    with col_b:
        st.subheader("Seller vs Média geral")
        media_receita = df.groupby("seller_id")["price"].sum().mean()
        comparacao = pd.DataFrame({
            "Categoria": ["Este Seller", "Média dos Sellers"],
            "Receita (R$)": [df_sel["price"].sum(), media_receita]
        })
        fig = px.bar(
            comparacao, x="Categoria", y="Receita (R$)", color="Categoria",
            color_discrete_map={
                "Este Seller": "#1f3a93",
                "Média dos Sellers": "#aab7d4"
            }
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top produtos do seller")
    top_prod = (
        df_sel.groupby("product_id", as_index=False)
        .agg(
            total_itens=("product_id", "count"),
            receita=("price", "sum"),
            frete_medio=("freight_value", "mean")
        )
        .sort_values("receita", ascending=False)
        .head(10)
    )
    top_prod["product_id"] = top_prod["product_id"].str[:14] + "…"
    st.dataframe(top_prod, use_container_width=True)

    with st.expander("Ver dados detalhados"):
        st.dataframe(
            df_sel[[
                "order_id", "order_item_id", "product_id",
                "shipping_limit_date", "price", "freight_value", "gmv"
            ]].sort_values("shipping_limit_date", ascending=False),
            use_container_width=True
        )


# ═════════════════════════════════════════════════════════════════════════════
# ABA 3 — SIMILARIDADE DE PRODUTOS
# ═════════════════════════════════════════════════════════════════════════════
elif aba == "Similaridade de Produtos":
    st.title("Similaridade entre Produtos")
    st.markdown(
        "Cada produto é representado como um vetor de features "
        "(**preço médio**, **frete médio**, **volume de pedidos**). "
        "Produtos próximos no espaço de features têm comportamento similar "
        "de precificação e logística."
    )

    top_n = st.sidebar.slider("Top N produtos (por volume)", 20, 150, 60)

    prod_features = (
        df.groupby("product_id", as_index=False)
        .agg(
            avg_price   =("price",        "mean"),
            avg_freight =("freight_value", "mean"),
            total_orders=("order_id",      "nunique")
        )
        .sort_values("total_orders", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # ── Scatter: avg_price × avg_freight ─────────────────────────────────
    st.subheader("Preço médio × Frete médio (por volume de pedidos)")
    fig = px.scatter(
        prod_features,
        x="avg_price", y="avg_freight",
        size="total_orders", size_max=35,
        color="total_orders", color_continuous_scale="Viridis",
        hover_data={"product_id": True, "total_orders": True,
                    "avg_price": ":.2f", "avg_freight": ":.2f"},
        labels={
            "avg_price":    "Preço médio (R$)",
            "avg_freight":  "Frete médio (R$)",
            "total_orders": "Pedidos"
        }
    )
    fig.update_layout(margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Cosine Similarity Heatmap ─────────────────────────────────────────
    n_heat = st.sidebar.slider("Produtos no heatmap de similaridade", 10, 30, 20)
    prod_heat = prod_features.head(n_heat).copy()

    scaler  = MinMaxScaler()
    matrix  = scaler.fit_transform(prod_heat[["avg_price", "avg_freight", "total_orders"]])
    sim_mat = cosine_similarity(matrix)

    labels = [pid[:10] + "…" for pid in prod_heat["product_id"]]

    st.subheader(f"Mapa de similaridade cosine — Top {n_heat} produtos")
    fig_heat = go.Figure(go.Heatmap(
        z=sim_mat, x=labels, y=labels,
        colorscale="Blues", zmin=0, zmax=1,
        hovertemplate=(
            "Produto A: %{y}<br>"
            "Produto B: %{x}<br>"
            "Similaridade: %{z:.3f}<extra></extra>"
        )
    ))
    fig_heat.update_layout(
        height=600,
        margin=dict(t=10, l=100, b=100),
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9))
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption(
        "Similaridade calculada via cosine similarity sobre features normalizadas "
        "(MinMaxScaler): preço médio, frete médio e volume de pedidos."
    )


# ═════════════════════════════════════════════════════════════════════════════
# ABA 4 — GERADOR DE APRESENTAÇÃO (GenAI + DALL-E)
# ═════════════════════════════════════════════════════════════════════════════
elif aba == "Gerador de Apresentação":
    st.title("🎯 Gerador de Apresentação de Produto")
    st.markdown(
        "Selecione um produto do dataset, preencha as informações de venda "
        "e gere uma imagem comercial com **DALL-E 3** para compor a apresentação."
    )

    # ── Selecionar produto ────────────────────────────────────────────────
    top_produtos = (
        df.groupby("product_id")
        .agg(
            receita      =("price",         "sum"),
            pedidos      =("order_id",       "nunique"),
            preco_medio  =("price",          "mean"),
            frete_medio  =("freight_value",  "mean"),
            total_itens  =("order_item_id",  "count"),
        )
        .sort_values("receita", ascending=False)
        .head(50)
    )

    produto_id  = st.selectbox(
        "Produto (top 50 por receita)",
        top_produtos.index,
        format_func=lambda x: f"{x[:20]}… | R$ {top_produtos.loc[x,'receita']:,.0f}"
    )
    stats = top_produtos.loc[produto_id]

    st.divider()

    col_stats, col_form = st.columns([1, 1])

    with col_stats:
        st.subheader("Dados do produto no marketplace")
        st.metric("Receita total (R$)",  f"{stats['receita']:,.2f}")
        st.metric("Pedidos realizados",  f"{int(stats['pedidos']):,}")
        st.metric("Preço médio (R$)",    f"{stats['preco_medio']:.2f}")
        st.metric("Frete médio (R$)",    f"{stats['frete_medio']:.2f}")
        st.metric("Total de itens",      f"{int(stats['total_itens']):,}")

    with col_form:
        st.subheader("Configure a apresentação")
        nome_produto = st.text_input("Nome do produto",    placeholder="Ex: Fone de Ouvido Bluetooth Premium")
        categoria    = st.text_input("Categoria",          placeholder="Ex: Eletrônicos")
        publico      = st.text_input("Público-alvo",       placeholder="Ex: Jovens adultos, amantes de música")
        diferenciais = st.text_area(
            "Principais diferenciais (um por linha)",
            placeholder="Cancelamento de ruído\nBateria 30h\nConexão multiponto",
            height=100
        )
        estilo_img = st.selectbox("Estilo da imagem gerada", [
            "foto comercial profissional, fundo branco, iluminação de estúdio",
            "lifestyle moderno, ambiente clean e minimalista",
            "flat lay elegante sobre superfície de mármore",
            "renderização 3D realista, fundo gradiente",
        ])

    gerar = st.button("✨ Gerar Apresentação com DALL-E", type="primary", use_container_width=True)

    if gerar:
        if not nome_produto:
            st.warning("Preencha o nome do produto antes de gerar.")
        else:
            prompt = (
                f"Professional e-commerce product image: {nome_produto}, {categoria}. "
                f"{estilo_img}. "
                f"High quality, commercial photography style, suitable for online marketplace. "
                f"No text or watermarks."
            )

            with st.spinner("Gerando imagem com DALL-E 3…"):
                try:
                    client   = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        response_format="b64_json",
                        n=1,
                    )
                    img_bytes = base64.b64decode(response.data[0].b64_json)
                    img       = Image.open(io.BytesIO(img_bytes))
                except Exception as e:
                    st.error(f"Erro ao chamar DALL-E: {e}")
                    st.stop()

            st.divider()
            st.subheader(f"📦 Apresentação — {nome_produto}")

            col_img, col_info = st.columns([1, 1])

            with col_img:
                st.image(img, use_container_width=True)

            with col_info:
                diferenciais_lista = [d.strip() for d in diferenciais.splitlines() if d.strip()]

                st.markdown(f"**Categoria:** {categoria}")
                st.markdown(f"**Público-alvo:** {publico}")

                if diferenciais_lista:
                    st.markdown("**Diferenciais:**")
                    for d in diferenciais_lista:
                        st.markdown(f"- ✅ {d}")

                st.divider()
                st.markdown("**Desempenho no marketplace:**")
                st.markdown(f"- 💰 Receita total: R$ {stats['receita']:,.2f}")
                st.markdown(f"- 📦 Pedidos: {int(stats['pedidos']):,}")
                st.markdown(f"- 💵 Preço médio: R$ {stats['preco_medio']:.2f}")
                st.markdown(f"- 🚚 Frete médio: R$ {stats['frete_medio']:.2f}")

            with st.expander("🔍 Prompt utilizado (DALL-E 3)"):
                st.code(prompt, language="text")
