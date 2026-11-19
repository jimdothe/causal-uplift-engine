{% test smd_below(model, threshold) %}
select * from {{ model }} where abs(smd) >= {{ threshold }}
{% endtest %}
