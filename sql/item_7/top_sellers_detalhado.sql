SELECT
    "SELLER_ID",
    COUNT(*) AS total_items,
    COUNT(DISTINCT "ORDER_ID") AS total_orders,
    SUM("PRICE") AS total_sales,
    AVG("PRICE") AS avg_price,
    SUM("FREIGHT_VALUE") AS total_freight,
    AVG("FREIGHT_VALUE") AS avg_freight
FROM PUBLIC.TB__T4K4EC__OLIST_ORDER_ITEMS_DATASET_ATHOS_JOHANN
GROUP BY "SELLER_ID"
ORDER BY total_sales DESC
LIMIT 10