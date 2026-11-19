{% test row_count_equals(model, expected) %}
-- Fails (returns a row) when the model's row count differs from `expected`.
select count(*) as actual_rows
from {{ model }}
having count(*) != {{ expected }}
{% endtest %}
