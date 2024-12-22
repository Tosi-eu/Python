SELECT 
    orders.*,
    order_items_summary.sales_amount,
    order_items_summary.item_discount_amount,
    {{ mean_ticket('order_items_summary.sales_amount', 'order_items_summary.n_lines') }} as mean_ticket
FROM 
    {{ 'stg_tpch_orders' }} as orders
JOIN    
    {{ ref('int_order_items_summary') }} as order_items_summary
ON  
    orders.order_key = order_items_summary.order_key
ORDER BY
    order_date
