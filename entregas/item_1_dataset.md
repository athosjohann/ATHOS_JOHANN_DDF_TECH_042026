# Item 1 - Seleção do Dataset

## Dataset escolhido

**[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

Fonte pública disponível no Kaggle.

## Sobre o dataset

O dataset contém dados reais anonimizados de pedidos realizados na plataforma Olist, o maior marketplace do Brasil, entre 2016 e 2018. Cobre todo o ciclo de uma transação de e-commerce: pedido, itens, pagamento, entrega e avaliação do cliente.

## Tabela utilizada: `olist_order_items_dataset`

Para este case foi utilizada a tabela **`olist_order_items_dataset`**, que registra os itens individuais de cada pedido — unidade central de análise de um e-commerce.

### Volume

 `olist_order_items_dataset` | > 112.000 |

Atende ao requisito mínimo de **100.000 registros** estabelecido no case.

### Schema

| Coluna | Tipo | Descrição |
|---|---|---|
| `order_id` | string | Identificador único do pedido |
| `order_item_id` | integer | Sequencial do item dentro do pedido (1, 2, 3...) |
| `product_id` | string | Identificador único do produto |
| `seller_id` | string | Identificador único do vendedor (PII — criptografado na ingestão) |
| `shipping_limit_date` | timestamp | Data limite para envio pelo vendedor |
| `price` | float | Preço unitário do item (R$) |
| `freight_value` | float | Valor do frete do item (R$) |

### Aderência ao cenário proposto

A tabela `olist_order_items_dataset` é aderente ao cenário de e-commerce do case pois permite:

- análise de **volume de vendas** por produto e vendedor;
- análise de **precificação e frete** com dados reais de mercado;
- identificação de **padrões temporais** via `shipping_limit_date`;
- geração de **métricas de negócio** como ticket médio, participação por seller e composição dos pedidos.

## Justificativa da escolha

O Olist dataset é amplamente utilizado na comunidade de dados brasileira, possui documentação consolidada e schema limpo. A tabela de itens de pedidos foi escolhida por concentrar as dimensões mais relevantes para análise de catálogo e comportamento de vendas em e-commerce, sendo suficiente para cobrir todas as etapas do case: ingestão, catalogação, qualidade, modelagem e visualização.
