# ATHOS_JOHANN_DDF_TECH_042026

Case Técnico — Dadosfera | Athos Johann | Abril 2026

## Objetivo

Construir uma POC de plataforma de dados para uma empresa de e-commerce, centralizando dados de catálogo de produtos para análises descritivas e geração de features com IA, utilizando a Dadosfera como plataforma central.

## Dataset

**[Olist E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** — base pública com mais de 100.000 registros de pedidos, itens, vendedores e avaliações do marketplace brasileiro Olist.

## Narrativa de negócio

O cliente possui grande volume de dados de produtos com descrições não padronizadas. Isso impacta a qualidade do catálogo, busca, categorização e análises. A proposta é integrar os dados na Dadosfera, catalogá-los, medir a qualidade, enriquecer os textos com IA e disponibilizar dashboards e um data app.

## Entregas

| Item | Descrição | Status |
|------|-----------|--------|
| [0 - Planejamento](entregas/item_0_planejamento.md) | Planejamento ágil (Gantt / Kanban / PMBOK) | Em desenvolvimento |
| [1 - Dataset](entregas/item_1_dataset.md) | Seleção e preparação da base de dados | Em desenvolvimento |
| [2.1 - Integração](entregas/item_2.1_integracao.md) | Carga na Dadosfera via pipeline PostgreSQL + microtransformação | Concluído |
| [3 - Catalogação](entregas/item_3_catalogacao.md) | Catalogação no data lake (raw / processed / analytics) | Em desenvolvimento |
| [4 - Qualidade](entregas/item_4_qualidade.md) | Relatório de qualidade com great-expectations ou soda-core | Em desenvolvimento |
| [5 - IA Generativa](entregas/item_5_ia_generativa.md) | Extração de features de textos com LLM | Em desenvolvimento |
| [6 - Modelagem](entregas/item_6_modelagem.md) | Modelagem do data warehouse (Kimball / Data Vault) | Em desenvolvimento |
| [7 - Visualização](entregas/item_7_visualizacao.md) | Dashboards com mínimo 5 tipos de visualização | Em desenvolvimento |
| [8 - Pipeline](entregas/item_8_pipeline.md) | Pipeline de dados no módulo de inteligência da Dadosfera | Em desenvolvimento |
| [9 - Data App](entregas/item_9_data_app.md) | Aplicação Streamlit para exploração dos dados | Em desenvolvimento |
| [10 - Apresentação](entregas/item_10_apresentacao.md) | POC demonstrando a arquitetura na Dadosfera | Em desenvolvimento |

## Estrutura do repositório

```
.
├── entregas/          # Documentação de cada item do case em Markdown
├── assets/            # Prints e evidências por item
│   └── item_2.1/      # Screenshots da pipeline de integração
└── README.md
```
