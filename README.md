# ATHOS_JOHANN_DDF_TECH_042026

Case Técnico — Dadosfera | Athos Johann | Abril 2026

## Objetivo

Construir uma POC de plataforma de dados para uma empresa de e-commerce, centralizando dados de catálogo de produtos para análises descritivas e geração de features com IA, utilizando a Dadosfera como plataforma central.

## Dataset

**[Olist E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** — base pública com 112.650 registros de pedidos, itens, vendedores e avaliações do marketplace brasileiro Olist.

## Narrativa de negócio

O cliente possui grande volume de dados de produtos com descrições não padronizadas. Isso impacta a qualidade do catálogo, busca, categorização e análises. A proposta é integrar os dados na Dadosfera, catalogá-los, medir a qualidade, modelar em Star Schema, disponibilizar dashboards e um data app com geração de imagens via IA.

## Entregas

| Item | Descrição | Status |
|------|-----------|--------|
| [0 - Planejamento](entregas/item_0_planejamento.md) | Gantt, fluxograma de dependências, análise de risco, custos e recursos (PMBOK) | ✅ Concluído |
| [1 - Dataset](entregas/item_1_dataset.md) | Seleção e documentação da base Olist | ✅ Concluído |
| [2.1 - Integração](entregas/item_2.1_integracao.md) | Pipeline PostgreSQL → Dadosfera + microtransformação (Encrypt seller_id) | ✅ Concluído |
| [3 - Catalogação](entregas/item_3_catalogacao.md) | Catalogação via API REST da Dadosfera + documentação do data asset | ✅ Concluído |
| [4 - Qualidade](entregas/item_4_qualidade.md) | Great Expectations (8/8 regras) + mapeamento CDM (SalesOrderLine) | ✅ Concluído |
| [6 - Modelagem](entregas/item_6_modelagem.md) | Star Schema Kimball: 3 dims + fato + 2 views + diagramas Mermaid | ✅ Concluído |
| [7 - Visualização](entregas/item_7_visualizacao.md) | Dashboard Metabase com 5 tipos de visualização + notificação Slack | ✅ Concluído |
| [8 - Pipeline](entregas/item_8_pipeline.md) | ETL Bronze→Silver→Gold com Apache Spark (bônus Spark) | ✅ Concluído |
| [9 - Data App](entregas/item_9_data_app.md) | Streamlit: EDA + Análise por Seller + Similaridade de Produtos | ✅ Concluído |
| [Bônus - GenAI](entregas/item_bonus_genai.md) | Gerador de apresentação de produto com DALL-E 3 integrado ao Data App | ✅ Concluído |

## Data App

**[athosjohannddftech042026.streamlit.app](https://athosjohannddftech042026-bhnzunzfetvedwqddt4qnz.streamlit.app/)**

## Estrutura do repositório

```
.
├── entregas/          # Documentação de cada item em Markdown
├── assets/            # Screenshots e evidências por item
│   ├── item_2.1/
│   ├── item_3/
│   ├── item_4/
│   ├── item_7/
│   ├── item_8/
│   ├── item_9/
│   └── item_bonus/
├── notebooks/         # Notebooks Google Colab por item
│   ├── item_3/
│   ├── item_4/
│   ├── item_8/
│   └── item_bonus/
├── sql/               # Queries SQL do dashboard Metabase
│   └── item_7/
├── item_9_data_app/   # Código-fonte do Streamlit Data App
│   ├── app.py
│   ├── requirements.txt
│   └── data/
└── README.md
```
