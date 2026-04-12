# Data App — E-commerce Analytics Olist

Aplicação Streamlit para exploração interativa dos dados de order items do e-commerce Olist.

## Páginas

| Página | Descrição |
|---|---|
| Visão Geral | KPIs globais, série temporal, distribuição de preços, top sellers, scatter preço × frete |
| Análise por Seller | Filtro por seller e período, KPIs individuais, comparação com média geral, top produtos |
| Similaridade de Produtos | Scatter de produtos no espaço de features + heatmap de cosine similarity |

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy — Streamlit Community Cloud

1. Fork ou push deste repositório para o seu GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repositório, branch `main`
4. Main file path: `item_9_data_app/app.py`
5. Clique em **Deploy**

## Estrutura

```
item_9_data_app/
├── app.py              # aplicação principal
├── requirements.txt    # dependências
└── data/
    └── olist_order_items_dataset.csv
```
