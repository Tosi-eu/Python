{% macro discounted_amount(extended_price, discount_percentage, scale=2) %}
    ({{extended_price}} * {{discount_percentage}})::numeric(16, {{ scale }})
{% endmacro %}

{% macro calculate_subtotal(total_price, discount_percentage, scale=2) %}
    ({{total_price}} - {{total_price}} * {{discount_percentage}})::numeric(16, {{ scale }})
{% endmacro %}

{% macro mean_ticket(total_money, n_items, scale=2) %}
    ({{ total_money }} / {{ n_items }})::numeric(16, {{ scale }})
{% endmacro %}