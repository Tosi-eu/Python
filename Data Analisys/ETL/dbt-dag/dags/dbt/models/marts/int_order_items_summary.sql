    SELECT
        order_key,
        sum(extended_price) as sales_amount,
        sum(item_discount) as item_discount_amount
    FROM
        {{ ref('int_order_data') }}
    GROUP BY order_key