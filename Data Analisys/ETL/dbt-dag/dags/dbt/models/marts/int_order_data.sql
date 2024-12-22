SELECT
    line_item.order_item_key,
    line_item.part_key,
    line_item.line_number,
    line_item.extended_price,   
    line_item.discount_percentage,
    orders.order_key,
    orders.customer_key,
    orders.order_date,
    {{ discounted_amount('line_item.extended_price', 'line_item.discount_percentage') }} as item_discount,
    {{ calculate_subtotal('line_item.extended_price', 'line_item.discount_percentage')}} as total_after_discount,
    RANK() OVER (
    PARTITION BY orders.order_date 
    ORDER BY {{ calculate_subtotal('line_item.extended_price', 'line_item.discount_percentage') }} DESC
    ) AS sales_rank
FROM
    {{ ref('stg_tpch_orders') }} as orders
JOIN
    {{ref('stg_tpch_line_items') }} as line_item
    ON orders.order_key = line_item.order_key
ORDER BY sales_rank DESC